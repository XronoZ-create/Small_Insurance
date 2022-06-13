import requests
import time
from datetime import datetime, timedelta

class RCA:
    def __init__(self, url_token, json_table):
        self.json_table = json_table
        self.token = url_token.split('/')[-1]
        self.session = requests.Session()
        self.session.headers = {
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Host': 'e-garant.autoins.ru',
            'Origin': 'https://e-garant.autoins.ru',
            'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        }

    def login(self, login_phone, password):
        self.login_phone = login_phone
        self.password = password

        self.session.headers.update({"Referer": f"https://e-garant.autoins.ru/rgs/login/{self.token}"})
        self.url = f"https://e-garant.autoins.ru/api/v1/egarant-lk/ui/{self.token}/authorize"
        self.data = {"login": self.login_phone, "password": self.password}

        self.start_while_true = datetime.now()
        while True:
            if (datetime.now() - self.start_while_true) > timedelta(minutes=3):
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: Не удалось войти в созданный акк РСА в течение 3 минут(Логин:{self.login_phone}, Пароль: {self.password}). Пробуем снова создать.')
                raise AuthFailed
            self.r = self.session.post(self.url, json=self.data, verify=False)
            if self.r.status_code == 200:
                self.r_json = self.r.json()
                try:
                    if self.r_json['status'] != "ACTIVE":
                        self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: Ошибка аутентификации в РСА')
                    else:
                        return
                except:
                    self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: Ошибка аутентификации в РСА')
            else:
                time.sleep(0.2)

    def logout(self):
        self.url = f"https://e-garant.autoins.ru/api/v1/egarant-lk/ui/logout"
        self.start_while_true = datetime.now()
        while True:
            if (datetime.now() - self.start_while_true) > timedelta(minutes=2):
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: Не удалось выйти из аккаунта РСА')
                break  # Ошибка не нужна
            self.r = self.session.post(self.url)
            if self.r.status_code == 200:
                return
            else:
                time.sleep(0.2)

    def reg(self):
        self.start_while_true = datetime.now()
        while True:
            if (datetime.now() - self.start_while_true) > timedelta(minutes=3):
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: Сайт РСА не отвечает. Осаго не удалось зарегистрировать в течение 1 минуты. Пробуем снова')
                raise RegFailed
            self.session.headers.update({"Referer": f"https://e-garant.autoins.ru/rgs/registration/{self.token}"})
            self.url = f"https://e-garant.autoins.ru/api/v1/egarant-lk/ui/{self.token}/register"
            self.r = self.session.post(self.url, verify=False)
            if self.r.status_code == 200:
                return
            else:
                time.sleep(0.2)

    def check_data(self):
        self.session.headers.update({"Referer": f"https://e-garant.autoins.ru/rgs/contract/{self.token}/step4"})
        self.url = f"https://e-garant.autoins.ru/api/v1/egarant-contract/ui/{self.token}/validation"

        self.start_while_true = datetime.now()
        while True:
            if (datetime.now() - self.start_while_true) > timedelta(minutes=2):
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: Сайт РСА не отвечает. Не удалось нажатьт на кнопку подтверждения')
                raise RegFailed
            self.r = self.session.put(self.url)
            print(self.r.status_code)
            if self.r.status_code == 200 or self.r.status_code == 202:
                break
            else:
                time.sleep(0.2)


class RegFailed(Exception):
    pass
class AuthFailed(Exception):
    pass
class LogoutFailed(Exception):
    pass