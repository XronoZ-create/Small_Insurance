from modules.img_captcha import ImgCaptchaAnticaptcha
from config import Config
import time
from contextlib import suppress
from modules.email_manager import EmailManager, NotFindMail
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from random import randint

import random
from modules.telephone import Telephone


class RegAcc:
    def __init__(self):
        self.img_captcha = ImgCaptchaAnticaptcha()
        self.url_site = "https://b2c.armeec.ru/personal/index.php?register=yes"
        self.url_reg = "https://b2c.armeec.ru/local/tools/webslon/elpolis.api/"
        self.headers = {
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://b2c.armeec.ru',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
        }

    def run(self, reg_data=None, json_table=None):
        self.telephone = Telephone(service=json_table.telephone_service)
        self.mail_google = EmailManager(login=reg_data.email_login, password=reg_data.email_password)
        self.email = reg_data.email_login
        self.json_table = json_table
        self.session = requests.Session()
        self.session.headers = self.headers
        # ---------------------------------Ставим прокси----------------------------------------------------------------
        if Config.proxies != None:
            self.proxies = Config.proxies
            self.session.proxies = self.proxies
        else:
            self.proxies = None
        # --------------------------------------------------------------------------------------------------------------

        self.r = self.session.get(self.url_site)
        if self.r.status_code != 200:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: сайт недоступен')
            raise LagSite
        self.bs = BeautifulSoup(self.r.text)
        self.captcha_sid = parse_qs(urlparse(self.bs.find('input', {"name": 'captcha_sid'}).parent.find("img")["src"]).query)["captcha_sid"][0]
        print(self.captcha_sid)

        self.captcha_word = self.img_captcha.get_solve(
            img_url=f"https://b2c.armeec.ru/local/modules/webslon.elpolis/options/captcha_preview.php?Preview=Y&captcha_sid={self.captcha_sid}&site_id=r1"
        )

        # self.phone = str(randint(89680000000, 89689999999))[1:]
        self.phone = self.telephone.get_number()["tel"][1:]
        self.ugsk_password = "_Z+zs9u65@"
        self.name = reg_data.name
        self.surname = reg_data.surname
        self.otchestvo = reg_data.otchestvo
        self.pass_seriya = reg_data.pass_seriya
        self.pass_number = reg_data.pass_number
        self.birthday = datetime.strptime(reg_data.birthday, "%Y-%m-%d").strftime("%d.%m.%Y")
        self.body = """
            {"email":"%s",

            "phone":"%s",
            "isActivityOnPage": "isActive",
            "startLimitTimeRegister": "%s",
            "isSlingshot":1,
            "method":"register",
            "middlename":"",
            "password":"%s",
            "confirm_password":"%s",

            "captcha_sid":"%s",
            "captcha_word":"%s",

            "backurl":"",
            "checkCode":false,
            "registration_confirm_user_sms":false,
            "ergoByAgent":false,
            "contractor":
                {
                    "id":"",
                    "status":"ФизЛицо",
                    "foreign":false,
                    "document":{
                        "type":"RussianPassport",
                        "series":"%s",
                        "number":"%s",
                        "divisionCode": "510005"
                    },
                    "defDocument":"RussianPassport",
                    "registrationAddress":{"flat_number":null,"fullAdress":"","flatType":"кв"},
                    "postAddress":{"flat_number":null,"fullAdress":"","flatType":"кв"},
                    "AgreementForReceiveSMS":false,
                    "sentSms":false,
                    "checkCode":false,
                    "confirmationCode":"",
                    "nationality":"РОССИЯ",
                    "name":"%s",
                    "lastname":"%s",
                    "middlename":"%s",
                    "documentType":"RussianPassport",
                    "documents":{
                        "RussianPassport":{
                            "type":"RussianPassport",
                            "series":"%s",
                            "number":"%s",
                            "divisionCode": "510005"
                        }
                    },
                    "birthday":"%s"
                }
            }""" % (
            self.email,
            self.phone, int((datetime.now()-timedelta(minutes=3)).timestamp() * 1000), self.ugsk_password, self.ugsk_password,
            self.captcha_sid, self.captcha_word,
            self.pass_seriya, self.pass_number,
            self.name, self.surname, self.otchestvo,
            self.pass_seriya, self.pass_number,
            self.birthday
        )

        self.r = self.session.post(self.url_reg, data=self.body.encode('utf-8'))
        print(self.r.text)
        if self.r.status_code != 200:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: сайт недоступен')
            raise LagSite
        elif self.r.json()["error"] == 101:
            raise WrongCaptchaWord
        elif self.r.json()["error"] == 103:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} На указанную почту уже зарегистрирован аккаунт. Меняем')
            json_table.change_email_address()
            raise AccAlreadyRegArm
        elif self.r.json()["error"] != 0:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: {self.r.json()["msg"]}')
            raise LagSite

        self.start_wait_mail = datetime.now()
        while True:
            if (datetime.now() - self.start_wait_mail) > timedelta(minutes=15):
                json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: не приходит сообшение на почту(Ожидали 5 минут). Почта: {self.email}')
                raise LongWaitEmailCode
            try:
                self.email_code = self.mail_google.get_last_mail_arm_code()
                break
            except NotFindMail:
                print("Ожидаем сообщения с кодом")
                time.sleep(random.randrange(5, 50) / 10)
            except Exception:
                time.sleep(random.randrange(5, 50) / 10)
        self.body = """{"phone":"%s","code":"%s","error":[],"confirm":[],"method":"userActivate"}""" % (self.phone, self.email_code)
        self.r = self.session.post(self.url_reg, data=self.body.encode('utf-8'))
        print(self.r.text)
        if self.r.status_code != 200:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: сайт недоступен')
            raise LagSite
        elif self.r.json()["error"] != 0:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: {self.r.json()["msg"]}')
            raise LagSite

        json_table.set_value("login_osk", self.email)
        json_table.set_value("password_osk", self.ugsk_password)
        return [self.email, self.ugsk_password, self.telephone]

class LagSite(Exception):
    pass
class LongWaitEmailCode(Exception):
    pass
class WrongCaptchaWord(Exception):
    pass
class AccAlreadyRegArm(Exception):
    pass