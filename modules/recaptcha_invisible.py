import requests
import time

class GoogleV2CaptchaAntiCaptcha:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_solve(self, google_key, site_url, proxy, useragent, cookies):
        self.url = "https://api.anti-captcha.com/createTask"

        if proxy != None:
            self.proxy_type = proxy['https'].split('://')[0]
            self.proxy_ip = proxy['https'].split('@')[1].split(':')[0]
            self.proxy_port = proxy['https'].split(':')[-1]
            self.proxy_login = proxy['https'].split('://')[1].split(':')[0]
            self.proxy_password = proxy['https'].split('://')[1].split(':')[1].split('@')[0]

            self.cookies = ""
            for self._key, self._val in cookies.items():
                self.cookies += f"{self._key}={self._val};"

            self.data = {
                "clientKey": self.api_key,
                "task": {
                    "type": "RecaptchaV2Task",
                    "websiteURL": site_url,
                    "websiteKey": google_key,
                    "isInvisible": True,
                    "userAgent": useragent,
                    "proxyType": self.proxy_type,
                    "proxyAddress": self.proxy_ip,
                    "proxyPort": self.proxy_port,
                    "proxyLogin": self.proxy_login,
                    "proxyPassword": self.proxy_password,
                    "cookies": self.cookies
                }
            }
        else:
            self.data = {
                "clientKey": self.api_key,
                "task": {
                    "type": "RecaptchaV2TaskProxyless",
                    "websiteURL": site_url,
                    "websiteKey": google_key,
                    "isInvisible": True,
                    "userAgent": useragent
                }
            }
        self.r = requests.post(self.url, json=self.data)
        self.r_json = self.r.json()
        print(self.r_json)
        self.task_id = self.r_json["taskId"]

        self.url = "https://api.anti-captcha.com/getTaskResult"
        self.data = {
            "clientKey": self.api_key,
            "taskId": self.task_id
        }
        while True:
            self.r = requests.post(self.url, json=self.data)
            self.r_json = self.r.json()
            print(self.r_json)
            if self.r_json["errorId"] != 0:
                raise Exception
            elif self.r_json["status"] == "ready":
                return str(self.r_json["solution"]["gRecaptchaResponse"])
            time.sleep(5)
