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
from modules.telephone import TelephoneOnlineSim, TelephoneActivateSms


class RegAcc:
    def __init__(self):
        self.img_captcha = ImgCaptcha(service="anticaptcha")
        self.url_site = "https://e-osago.ugsk.ru/personal/index.php?register=yes"
        self.url_reg = "https://e-osago.ugsk.ru/local/tools/webslon/elpolis.api/"
        self.headers = {
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://e-osago.ugsk.ru',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        # self.telephone_client = TelephoneOnlineSim()
        self.telephone_client = TelephoneActivateSms()

    def run(self, reg_data=None, json_table=None):
        self.mail_google = EmailManager(login=reg_data.email_login, password=reg_data.email_password)
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
        # print(self.r.text)
        if self.r.status_code != 200:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: сайт недоступен')
            raise LagSite
        self.bs = BeautifulSoup(self.r.text)
        self.captcha_sid = parse_qs(urlparse(self.bs.find('input', {"name": 'captcha_sid'}).parent.find("img")["src"]).query)["captcha_sid"][0]
        print(self.captcha_sid)

        self.captcha_word = self.img_captcha.get_solve(
            img_url=f"https://e-osago.ugsk.ru/local/modules/webslon.elpolis/options/captcha_preview.php?Preview=Y&captcha_sid={self.captcha_sid}&site_id=r1"
        )
        self.email = reg_data.email_login
        # self.phone = self.telephone_client.get_number(service="rsa")["tel"]  # onlinesim
        self.phone = self.telephone_client.get_number()["tel"]  # activate
        self.ugsk_password = "_Z+zs9u65@"
        self.name = reg_data.name
        self.surname = reg_data.surname
        self.otchestvo = reg_data.otchestvo
        self.pass_seriya = reg_data.pass_seriya
        self.pass_number = reg_data.pass_number
        self.birthday = datetime.strptime(reg_data.birthday, "%Y-%m-%d").strftime("%d.%m.%Y")
        self.body = """
            {"email":"%s",

            "phone":"%s","isSlingshot":1,"method":"register","middlename":"","password":"%s","confirm_password":"%s",

            "captcha_sid":"%s","captcha_word":"%s",

            "backurl":"","checkCode":false,"registration_confirm_user_sms":false,"ergoByAgent":false,"contractor":{"id":"","status":"ФизЛицо","foreign":false,

            "document":{
                "type":"RussianPassport",
                "series":"%s","number":"%s"
            },
            "defDocument":"RussianPassport",
            "registrationAddress":
                {"flat_number":null,"fullAdress":"","flatType":"кв"},
            "postAddress":
                {"flat_number":null,"fullAdress":"","flatType":"кв"},
            "AgreementForReceiveSMS":false,"sentSms":false,"snils": %s,"checkCode":false,"confirmationCode":"","nationality":"РОССИЯ",
            "name":"%s","lastname":"%s","middlename":"%s",
            "documentType":"RussianPassport","documents":{"RussianPassport":{"type":"RussianPassport","series":"%s","number":"%s"}},
            "birthday":"%s"}}""" % (
            self.email,
            self.phone, self.ugsk_password, self.ugsk_password,
            self.captcha_sid, self.captcha_word,
            self.pass_seriya, self.pass_number,
            13062234104,
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
                self.verif_url = self.mail_google.get_last_mail_ugsk_verif()
                time.sleep(2)
                break
            except NotFindMail:
                time.sleep(2)
            except Exception:
                pass

        self.sms_code = self.telephone_client.get_sms_code()
        self.body = """{"hash":"%s","smsCode":"%s","codeRequestId":"%s"}""" % (
            parse_qs(self.verif_url)["https://pro.ugsk.ru/verification/?hash"][0],
            self.sms_code,
            parse_qs(self.verif_url)["id"][0]
        )
        self.r = self.session.post("https://pro.ugsk.ru/pvsnew/email-verification/verify-email", data=self.body.encode('utf-8'))
        if self.r.status_code != 200:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: сайт недоступен')
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