import requests
import time
import urllib3
from config import Config
import base64
from contextlib import suppress
import random
from datetime import datetime, timedelta

class ImgCaptcha:
    def __init__(self, service):
        self.service = service
        self.client_guru = ImgCaptchaGuru()
        self.client_rucaptcha = ImgCaptchaRucaptcha()
        self.client_anticaptcha = ImgCaptchaAnticaptcha()

    def get_solve(self, img_url, wait=True):
        if self.service == "rucaptcha":
            self.active_client = self.client_rucaptcha
        elif self.service == "guru":
            self.active_client = self.client_guru
        elif self.service == "anticaptcha":
            self.active_client = self.client_anticaptcha

        self.start_while_true = datetime.now()
        while True:
            if (datetime.now() - self.start_while_true) > timedelta(minutes=2):
                raise TxtCaptchaRegFailed

            try:
                self.resp_client = self.active_client.get_solve(img_url=img_url)
                return self.resp_client
            except TxtCaptchaRegFailed:
                if wait == False:
                    raise TxtCaptchaRegFailed
                else:
                    print("TxtCaptchaRegFailed")
            except TxtCaptchaSolveFailed:
                if wait == False:
                    raise TxtCaptchaSolveFailed
                else:
                    print("TxtCaptchaSolveFailed")

    def bad(self):
        self.resp_client = self.active_client.bad()
        return self.resp_client

class ImgCaptchaGuru:
    def __init__(self):
        self.api_key = Config.guru_captcha_api_key

    def get_solve(self, img_url):
        self.img = requests.get(img_url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}).content

        self.url = "http://api.captcha.guru/in.php"
        self.data = {
            "method": "post",
            "key": self.api_key,
            "min_len": 5,
            "max_len": 5
        }
        self.files = {
            "file": self.img
        }
        self.r = requests.post(url=self.url, data=self.data, files=self.files)
        if self.r.text.split("|")[0] != "OK":
            raise TxtCaptchaRegFailed
        else:
            self.id_captcha = self.r.text.split("|")[1]
        self.url = "http://api.captcha.guru/res.php?key={api_key}&action=get&id={id_captcha}".format(
            api_key=self.api_key,
            id_captcha=self.id_captcha
        )
        while True:
            self.r = requests.get(self.url)
            self.r_text = self.r.text
            if self.r_text == "CAPCHA_NOT_READY":
                time.sleep(5)
            elif self.r_text.split("|")[0] == "OK":
                self.solve = self.r_text.split("|")[1]
                return self.solve
            else:
                raise TxtCaptchaSolveFailed

    def bad(self):
        self.url = f"http://api.captcha.guru/res.php?key={self.api_key}&action=reportbad&id={self.id_captcha}"
        self.r = requests.get(self.url)
        self.r_text = self.r.text
        print(self.r_text)

class ImgCaptchaRucaptcha:
    def __init__(self):
        self.api_key = Config.rucaptcha_captcha_api_key

    def get_solve(self, img_url):
        self.img = requests.get(img_url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}).content

        self.url = "http://rucaptcha.com/in.php"
        self.data = {
            "method": "post",
            "key": self.api_key,
            "min_len": 5,
            "max_len": 5
        }
        self.files = {
            "file": self.img
        }
        self.r = requests.post(url=self.url, data=self.data, files=self.files)
        if self.r.text.split("|")[0] != "OK":
            raise TxtCaptchaRegFailed
        else:
            self.id_captcha = self.r.text.split("|")[1]
        self.url = "http://rucaptcha.com/res.php?key={api_key}&action=get&id={id_captcha}".format(
            api_key=self.api_key,
            id_captcha=self.id_captcha
        )
        while True:
            self.r = requests.get(self.url)
            self.r_text = self.r.text
            if self.r_text == "CAPCHA_NOT_READY":
                time.sleep(5)
            elif self.r_text.split("|")[0] == "OK":
                self.solve = self.r_text.split("|")[1]
                return self.solve
            else:
                raise TxtCaptchaSolveFailed

    def bad(self):
        self.url = f"http://rucaptcha.com/res.php?key={self.api_key}&action=reportbad&id={self.id_captcha}"
        self.r = requests.get(self.url)
        self.r_text = self.r.text
        print(self.r_text)

class ImgCaptchaAnticaptcha:
    def __init__(self):
        self.api_key = Config.anticaptcha_captcha_api_key

    def get_solve(self, img_url):
        self.img = requests.get(img_url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}).content

        while True:
            try:
                self.url = "https://api.anti-captcha.com/createTask"
                self.data = {
                    "clientKey": self.api_key,
                    "task": {
                        "type": "ImageToTextTask",
                        "body": base64.b64encode(self.img).decode('utf-8'),
                        "minLength": 5,
                        "maxLength": 5
                    }
                }
                self.r = requests.post(url=self.url, json=self.data)
                self.r_json = self.r.json()
                print(self.r_json)
                print(self.data)
                if self.r_json["errorId"] != 0:
                    raise TxtCaptchaRegFailed
                else:
                    self.id_captcha = self.r_json["taskId"]
                    break
            except requests.exceptions.SSLError:
                time.sleep(random.randrange(10,50) / 10)
            except urllib3.exceptions.MaxRetryError:
                time.sleep(random.randrange(10,50) / 10)
            except requests.exceptions.ConnectionError:
                time.sleep(random.randrange(10, 50) / 10)
            except urllib3.exceptions.ProtocolError:
                time.sleep(random.randrange(10, 50) / 10)

        while True:
            try:
                self.url = "https://api.anti-captcha.com/getTaskResult"
                self.data = {
                    "clientKey": self.api_key,
                    "taskId": self.id_captcha
                }
                self.r = requests.post(self.url, json=self.data)
                self.r_json = self.r.json()
                print(self.r_json)
                if self.r_json["errorId"] != 0:
                    raise TxtCaptchaSolveFailed
                elif self.r_json["status"] == "ready":
                    self.solve = self.r_json["solution"]["text"]
                    return self.solve
                elif self.r_json["status"] == "processing":
                    time.sleep(5)
            except requests.exceptions.SSLError:
                time.sleep(random.randrange(10,50) / 10)
            except urllib3.exceptions.MaxRetryError:
                time.sleep(random.randrange(10,50) / 10)
            except requests.exceptions.ConnectionError:
                time.sleep(random.randrange(10, 50) / 10)
            except urllib3.exceptions.ProtocolError:
                time.sleep(random.randrange(10, 50) / 10)


    def bad(self):
        pass

class TxtCaptchaRegFailed(Exception):
    pass

class TxtCaptchaSolveFailed(Exception):
    pass