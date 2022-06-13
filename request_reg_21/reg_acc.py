from modules.img_captcha import ImgCaptcha
from config import Config
import time
from contextlib import suppress
from modules.email_manager import EmailManager, NotFindMail
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from random import randint

class RegAcc:
    def __init__(self):
        self.img_captcha = ImgCaptcha(service="anticaptcha")
        self.url_site = 'https://eosago21-vek.ru/personal/?register=yes&backurl=%2Fpersonal%2Findex.php'
        self.url_reg = "https://eosago21-vek.ru/local/tools/webslon/elpolis.api/"

        self.headers_site = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9', 'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'eosago21-vek.ru', 'Referer': 'https://eosago21-vek.ru/personal/',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"', 'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
        self.headers_reg = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host': 'eosago21-vek.ru',
            'Origin': 'https://eosago21-vek.ru',
            'Referer': 'https://eosago21-vek.ru/personal/index.php?register=yes',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }

    def run(self, reg_data=None, json_table=None):
        self.mail_google = EmailManager(login=reg_data.email_login, password=reg_data.email_password)
        self.session = requests.Session()

        # ---------------------------------Ставим прокси----------------------------------------------------------------
        if Config.proxies != None:
            self.proxies = Config.proxies
            self.session.proxies = self.proxies
        else:
            self.proxies = None
        # --------------------------------------------------------------------------------------------------------------

        self.r = self.session.get(self.url_site, headers=self.headers_site)

        self.api_key = self.r.text.split("window.api_key = ")[1].split(";")[0].replace("'", "")
        if self.r.status_code != 200:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: сайт недоступен')
            raise LagSite
        self.bs = BeautifulSoup(self.r.text)
        self.captcha_sid = parse_qs(urlparse(self.bs.find('input', {"name": 'captcha_sid'}).parent.find("img")["src"]).query)["captcha_sid"][0]
        print(self.captcha_sid)
        print(self.session.cookies.get_dict())
        print(self.api_key)

        self.captcha_word = self.img_captcha.get_solve(
            img_url=f"https://eosago21-vek.ru/local/modules/webslon.elpolis/options/captcha_preview.php?Preview=Y&captcha_sid={self.captcha_sid}&site_id=r1"
        )
        self.email = reg_data.email_login
        self.phone = str(randint(89680000000, 89689999999))[1:]
        self.ugsk_password = "_Z+zs9u65@"
        self.name = reg_data.name
        self.surname = reg_data.surname
        self.otchestvo = reg_data.otchestvo
        self.pass_seriya = reg_data.pass_seriya
        self.pass_number = reg_data.pass_number
        self.birthday = datetime.strptime(reg_data.birthday, "%Y-%m-%d").strftime("%d.%m.%Y")
        self.body = """{
            "email": "%s",
            "phone": "%s",
            "isSlingshot": 1,
            "method": "register",
            "middlename": "",
            "password": "%s",
            "confirm_password": "%s",
            "captcha_sid": "%s",
            "captcha_word": "%s",
            "backurl": "",
            "checkCode": false,
            "registration_confirm_user_sms": false,
            "nazvanie": "",
            "datte": "",
            "kod": "",
            "startLimitTimeRegister": %s,
            "ergoByAgent": false,
            "contractor": {
            "id": "",
            "status": "ФизЛицо",
            "foreign": false,
            "document": {
              "type": "RussianPassport",
              "series": "%s",
              "number": "%s"
            },
            "defDocument": "RussianPassport",
            "registrationAddress": {
              "flat_number": null,
              "fullAdress": "",
              "flatType": "кв"
            },
            "postAddress": {
              "flat_number": null,
              "fullAdress": "",
              "flatType": "кв"
            },
            "AgreementForReceiveSMS": false,
            "sentSms": false,
            "snils": "%s",
            "checkCode": false,
            "confirmationCode": "",
            "nationality": "РОССИЯ",
            "name": "%s",
            "lastname": "%s",
            "middlename": "%s",
            "documentType": "RussianPassport",
            "documents": {
              "RussianPassport": {
                "type": "RussianPassport",
                "series": "%s",
                "number": "%s"
              }
            },
            "birthday": "%s"
            },
            "checkCaptcha": true,
            "api_key": "%s"
            }""" % (
            self.email,
            self.phone,
            self.ugsk_password,
            self.ugsk_password,
            self.captcha_sid,
            self.captcha_word,
            int((datetime.now()-timedelta(minutes=3)).timestamp() * 1000),
            self.pass_seriya,
            self.pass_number,
            13062234104,
            self.name,
            self.surname,
            self.otchestvo,
            self.pass_seriya,
            self.pass_number,
            self.birthday,
            self.api_key
        )
        self.r = self.session.post(self.url_reg, data=self.body.encode('utf-8'), headers=self.headers_reg)

        print(self.r.text)
        if self.r.status_code != 200:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: сайт недоступен')
            raise LagSite
        elif self.r.json()["error"] == 101:
            raise WrongCaptchaWord
        elif self.r.json()["error"] == 103:
            json_table.change_email_address()
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} На указанную почту уже зарегистрирован аккаунт. Меняем')
            raise AccAlreadyReg
        elif self.r.json()["error"] != 0:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: {self.r.json()["msg"]}')
            raise LagSite
        print(self.r.json())

        self.start_wait_mail = datetime.now()
        while True:
            if (datetime.now() - self.start_wait_mail) > timedelta(minutes=5):
                json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: не приходит сообшение на почту(Ожидали 5 минут)')
                raise LongWaitEmailCode
            try:
                self.email_code = self.mail_google.get_last_mail_21_code()
                time.sleep(2)
                break
            except NotFindMail:
                time.sleep(2)
            except Exception:
                pass
        self.body = """
            {
                "phone":"%s",
                "code":"%s",
                "backurl":"/personal/index.php",
                "error":[],
                "confirm":[],
                "api_key":"%s",
                "method":"userActivate"
            }""" % (self.phone, self.email_code, self.api_key)
        self.r = self.session.post(self.url_reg, data=self.body.encode('utf-8'), headers=self.headers_reg)
        if self.r.status_code != 200:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: сайт недоступен')
            raise LagSite
        elif self.r.json()["error"] != 0:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: {self.r.json()["msg"]}')
            raise LagSite

        json_table.set_value("login_osk", reg_data.email_login)
        json_table.set_value("password_osk", self.ugsk_password)
        return [reg_data.email_login, self.ugsk_password]

class LagSite(Exception):
    pass
class LongWaitEmailCode(Exception):
    pass
class WrongCaptchaWord(Exception):
    pass
class AccAlreadyReg(Exception):
    pass