import seleniumwire.undetected_chromedriver.v2 as uc
import requests
import json
import time
from modules.telephone import Telephone
from config import Config
from modules.email_manager import EmailManager, NotFindMail
from datetime import datetime, timedelta
import random
from .json.osago_data import OsagoData
from modules.recaptcha_invisible import GoogleV2CaptchaAntiCaptcha
from contextlib import suppress
import re

def cookies_selenium_to_requests(driver, session):
    cookies_dict = {}
    all_cookies = driver.get_cookies()
    for cookie in all_cookies:
        cookies_dict[cookie['name']] = cookie['value']
    cookies_dict['tmr_reqNum'] = str(int(cookies_dict['tmr_reqNum']) + random.randint(20, 100))
    print(cookies_dict)
    requests.utils.add_dict_to_cookiejar(session.cookies, cookies_dict)

class VskRequestsSession(requests.Session):
    def request(self, method, url,
                params=None, data=None, headers=None, cookies=None, files=None,
                auth=None, timeout=None, allow_redirects=True, proxies=None,
                hooks=None, stream=None, verify=None, cert=None, json=None):
        req = requests.Request(
            method=method.upper(),
            url=url,
            headers=headers,
            files=files,
            data=data or {},
            json=json,
            params=params or {},
            auth=auth,
            cookies=cookies,
            hooks=hooks,
        )
        prep = self.prepare_request(req)

        proxies = proxies or {}

        settings = self.merge_environment_settings(
            prep.url, proxies, stream, verify, cert
        )

        # Send the request.
        send_kwargs = {
            'timeout': timeout,
            'allow_redirects': allow_redirects,
        }
        send_kwargs.update(settings)
        resp = self.send(prep, **send_kwargs)

        # --------------------------------- Inject ---------------------------------------------------------------------
        if self.cookies.get('tmr_reqNum') != None:
            self.req_num = str(int(self.cookies['tmr_reqNum'])+1)
            self.cookies.set('tmr_reqNum', self.req_num)

        # --------------------------------------------------------------------------------------------------------------

        return resp

class CreateInsurance:
    def __init__(self, json_table):
        self.json_table = json_table
        self.client_data = json_table.data

        self.session = requests.Session()
        self.chrome_options = uc.ChromeOptions()
        self.seleniumwire_options = {}
        # ---------------------------------Ставим прокси----------------------------------------------------------------
        if Config.proxies != None:
            self.proxies = Config.proxies
            self.session.proxies = self.proxies
            self.seleniumwire_options['proxy'] = Config.proxies
        else:
            self.proxies = None
        # --------------------------------------------------------------------------------------------------------------
        self.driver = uc.Chrome(
            options=self.chrome_options,
            seleniumwire_options=self.seleniumwire_options,
            version_main=Config.selenium_version,  # 98
            headless=True
        )

        if self.client_data.telephone != "":
            self.telephone = Telephone(
                service="activate",
                id_num=self.client_data.id_num_telephone,
                date=datetime.strptime(self.client_data.reg_date_telephone, "%d.%m %H:%M %Y"),
                tel=self.client_data.telephone
            )
        else:
            self.telephone = Telephone(service="activate")
        self.mail_google = EmailManager(login=self.json_table.data.email_login, password=self.json_table.data.email_password)
        self.point_email_confirmed = False

    def auth(self):
        if self.json_table.data.session_cookies != '' and ((datetime.now() - datetime.strptime(self.json_table.data.session_cookies_date, "%d.%m %H:%M %Y")) <= timedelta(minutes=60)):
            self.session_id = self.json_table.data.session_id
            self.cookies_dict = json.loads(self.json_table.data.session_cookies)
            requests.utils.add_dict_to_cookiejar(self.session.cookies, self.cookies_dict)
            self.driver.quit()
            return
        # self.session_id = '404e12f06b28aad34edcd310ce3c318e'
        # self.cookies_dict = {'roistat_is_need_listen_requests': '0', 'roistat_is_save_data_in_cookie': '1', '__ddg1_': '9AUmrV4VJ7sbsp78msPq', '_gcl_au': '1.1.680864529.1650543617', 'tmr_lvid': 'df91b0646c23d65065eb01c56869f8ca', 'tmr_lvidTS': '1650543617497', '_ym_uid': '1650543618334404403', '_ym_d': '1650543618', 'advcake_trackid': '86b166a5-5a05-ca64-cf61-fd5f37f3f559', 'advcake_session_id': '9fe31eb9-2d49-1f6a-e74f-22001aa5ad55', 'roistat_first_visit': '1942578', '___dc': '7410f7d0-2408-4dd3-b2a0-520e8bbc298e', 'roistat_call_tracking': '1', 'roistat_emailtracking_email': 'null', 'roistat_emailtracking_tracking_email': 'null', 'roistat_emailtracking_emails': '%5B%5D', 'confidentialityPolicy': 'true', 'uxs_uid': '7688a830-c173-11ec-9cb7-e9969d2ea3b7', 'aprt_last_apsource': '1', 'aprt_last_partner': 'actionpay', 'aprt_last_apclick': '', 'site_referer': 'direct', 'utm_source': 'none', 'utm_medium': 'none', 'utm_campaign': 'none', 'utm_term': 'none', 'utm_content': 'none', '_ref': 'none', '_gid': 'GA1.2.741358930.1651666143', 'sessionId': 's%3A62726d46a927142a4eaaeadb.ZP7O023jHHvfUXd4RrPc1bl3f%2BQaiNLaDhg%2FFcWhn6w', '_ym_isad': '1', 'PHPSESSID': 'd9d997172644ab382f1b93982262f61b', 'cto_bundle': '-z9SeF9TM0lpZzFGcXBXaU1lVEg3Z2dRSXdRa0dVWGw2dmYxQkxLb2h1JTJGRHBTQ0VzQ0taMHAzNFRCOW1iY09IJTJGOGM5JTJCelNzcW5kN0xEbzJTRDNqeFA3JTJCMEwlMkI1eHd6amZsOFNFTG1ldHM1bDJJNTlldkdWOSUyQnl1NnZ3OHpDdGpnOFdZeDNTb0duT082JTJCYzRqbjRtdWVUTDc1USUzRCUzRA', '_ym_visorc': 'w', '_sp_ses.e248': '*', 'roistat_visit': '2172562', '_ga_Z2NHCL79R0': 'GS1.1.1651753969.14.1.1651753974.55', '_ga': 'GA1.2.551296722.1650543617', '_ubtcuid': 'b789d75a-e13a-4104-9b54-0cdf3c8d4f41', 'tmr_detect': '1%7C1651753974619', '_sp_id.e248': 'fd318203-cdf1-4e53-a72b-017c4cacacf6.1650543619.14.1651755015.1651751598.600f53d1-e37b-468f-bf12-514b22d33173', 'dimension5': 'Yes', 'app_user_id': '5ee8cee247d8c7dc44c1822e21de3b6b', 'ccui': '22008496', '_dc_gtm_UA-81630080-1': '1', 'tmr_reqNum': '277'}
        # requests.utils.add_dict_to_cookiejar(self.session.cookies, self.cookies_dict)
        # self.driver.quit()
        # return

        self.driver.get("https://shop.vsk.ru/auth?location=%2Fpersonal")

        self.captcha_client = GoogleV2CaptchaAntiCaptcha(api_key=Config.anticaptcha_captcha_api_key)
        if self.client_data.telephone == "" or ((datetime.now() - datetime.strptime(self.client_data.reg_date_telephone, "%d.%m %H:%M %Y")) > timedelta(minutes=55)):
            self.telephone.get_number()
            self.json_table.set_value('reg_date_telephone', self.telephone.active_client.date.strftime("%d.%m %H:%M %Y"))
            self.json_table.set_value('telephone', self.telephone.active_client.tel)
            self.json_table.set_value('id_num_telephone', self.telephone.active_client.id_num)
            self.json_table.set_value('telephone_service', self.telephone.active_client.name)
            self.json_table.set_value("login_parea", self.telephone.active_client.tel)
        else:
            self.telephone.active_client.retry_sms()

        self.start_while_true = datetime.now()
        while True:
            if (datetime.now() - self.start_while_true) > timedelta(minutes=4):
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} ОСАГО долго проверяется сайтом(4 мин.)')
                raise CreateErrorVsk

            self.cookies_dict = {}
            self.all_cookies = self.driver.get_cookies()
            for self.cookie in self.all_cookies:
                self.cookies_dict[self.cookie['name']] = self.cookie['value']
            self.token = self.captcha_client.get_solve(
                google_key='6LcqL9wUAAAAAEo22VFsBNyiK8S-jQrNdWTK2gD4',
                site_url="https://shop.vsk.ru/auth?location=%2Fpersonal",
                useragent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                proxy=Config.proxies,
                cookies=self.cookies_dict
            )

            cookies_selenium_to_requests(driver=self.driver, session=self.session)
            self.headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://shop.vsk.ru',
                'referer': 'https://shop.vsk.ru/personal/',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            self.url = 'https://shop.vsk.ru/ajax/auth/postSmsX/'
            self.data = {
                'phone': f'+7 ({self.telephone.active_client.tel[1:4]}) {self.telephone.active_client.tel[4:7]}-{self.telephone.active_client.tel[7:9]}-{self.telephone.active_client.tel[9:]}',
                'token': self.token
            }
            print(self.data)
            try:
                self.r = self.session.post(self.url, data=self.data, headers=self.headers)
            except:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка создания запроса на отправление кода')
                raise CreateErrorVsk
            if self.r.status_code != 200 :
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка создания запроса на отправление кода')
                raise CreateErrorVsk
            print(self.r.json())
            if self.r.json()["status"] == 'OK':
                break
            else:
                time.sleep(15)
                self.driver.get("https://shop.vsk.ru/auth?location=%2Fpersonal")

        self.driver.get("https://shop.vsk.ru/personal/")
        self.result = self.r.json()
        print(self.result)
        self.token = self.result['token']

        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://shop.vsk.ru',
            'referer': 'https://shop.vsk.ru/personal/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'host': 'shop.vsk.ru',
        }
        self.url = 'https://shop.vsk.ru/ajax/auth/checkPostSms/'
        self.data = {
            'token': self.token
        }
        try:
            self.r = self.session.post(self.url, data=self.data, headers=self.headers)
        except:
            self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка проверки создания запроса на отправление кода')
            raise CreateErrorVsk
        if self.r.status_code != 200:
            self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка проверки создания запроса на отправление кода')
            raise CreateErrorVsk
        elif self.r.json()["status"] != 'OK':
            print(self.r.json())
            self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка проверки создания запроса на отправление кода')
            raise CreateErrorVsk
        self.result = self.r.json()
        print(self.result)

        self.sms_code = self.telephone.get_sms_code()
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://shop.vsk.ru',
            'referer': 'https://shop.vsk.ru/personal/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'host': 'shop.vsk.ru',
        }
        self.url = 'https://shop.vsk.ru/ajax/auth/postCode/'
        self.data = {
            'pass': self.sms_code
        }
        try:
            self.r = self.session.post(self.url, data=self.data, headers=self.headers)
        except:
            self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка отправки кода с телефона')
            raise CreateErrorVsk
        if self.r.status_code != 200:
            self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка отправки кода с телефона')
            raise CreateErrorVsk
        elif self.r.json()["status"] != 'OK':
            print(self.r.json())
            self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка отправки кода с телефона')
            raise CreateErrorVsk
        self.result = self.r.json()
        self.token = self.result['token']
        print(self.result)

        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://shop.vsk.ru',
            'referer': 'https://shop.vsk.ru/personal/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'host': 'shop.vsk.ru',
        }
        self.url = 'https://shop.vsk.ru/ajax/auth/checkPostCode/'
        self.data = {
            'token': self.token
        }
        try:
            self.r = self.session.post(self.url, data=self.data, headers=self.headers)
        except:
            self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка проверки кода с телефона')
            raise CreateErrorVsk
        if self.r.status_code != 200 or self.r.json()["status"] != 'OK':
            self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка проверки кода с телефона')
            raise CreateErrorVsk
        self.result = self.r.json()
        print(self.result)

        self.driver.get('https://shop.vsk.ru/personal/')
        self.cookies_dict = {}
        self.all_cookies = self.driver.get_cookies()
        for self.cookie in self.all_cookies:
            self.cookies_dict[self.cookie['name']] = self.cookie['value']

        self.driver.get('https://shop.vsk.ru/osago/calculation/?')
        self.session_id = self.driver.execute_script("return window.VSK.additionalData.sessid")
        requests.utils.add_dict_to_cookiejar(self.session.cookies, self.cookies_dict)
        print(self.session_id)
        print(self.cookies_dict)
        self.driver.quit()

        self.json_table.set_value('session_cookies', json.dumps(self.cookies_dict))
        self.json_table.set_value('session_cookies_date', datetime.now().strftime("%d.%m %H:%M %Y"))
        self.json_table.set_value('session_id', self.session_id)

    def create(self):
        self.url = 'https://shop.vsk.ru/osago/ajax/calculation/update'
        self.data = OsagoData(client_data=self.client_data, session_id=self.session_id)
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://shop.vsk.ru',
            'referer': 'https://shop.vsk.ru/osago/calculation/?',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'x-ajax-api-version': '1.3',
            'host': 'shop.vsk.ru',
        }
        print(self.data())

        self.start_while_true = datetime.now()
        while True:
            if (datetime.now() - self.start_while_true) > timedelta(minutes=4):
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} ОСАГО долго проверяется сайтом(4 мин.)')
                raise CreateErrorVsk
            try:
                self.r = self.session.put(self.url, data=self.data(), headers=self.headers)
            except:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка заполнения данных ОСАГО')
                raise CreateErrorVsk
            print(self.r.text)
            if self.r.json()["status"] == 'error':
                print(self.r.json())
                if self.r.json().get('errors') != None:
                    self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка заполнения данных ОСАГО: {self.r.json()["errors"]}')
                else:
                    self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка заполнения данных ОСАГО')
                raise CreateErrorVsk
            elif self.r.json()["status"] == 'validationError':
                print(self.r.json())
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка заполнения данных ОСАГО: {self.r.json()["errors"]}')
                raise CreateErrorVsk
            elif self.r.json()["status"] == 'wait':
                print('Ждём')
                time.sleep(2)
                continue
            elif self.r.json()["status"] == 'success':
                break
            else:
                print(self.r.json())
        # --------------------------------- Подтверждение почты --------------------------------------------------------
        if not self.point_email_confirmed:
            self.url = 'https://shop.vsk.ru/personal/profile/email/confirm/send'
            self.headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://shop.vsk.ru',
                'referer': 'https://shop.vsk.ru/osago/calculation/?',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                'x-ajax-api-version': '1.3',
                'host': 'shop.vsk.ru',
            }
            self.data = {
                "email": self.json_table.data.email_login
            }
            try:
                self.r = self.session.post(self.url, data=json.dumps(self.data), headers=self.headers)
            except:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка сохранения почты')
                raise CreateErrorVsk
            if self.r.status_code != 200:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка сохранения почты')
                raise CreateErrorVsk
            print(self.r.json())
            if self.r.json()['status'] == 'error' and self.r.json()['message'] == 'Адрес электронной почты был ранее подтвержден':
                print('Меняем адрес эл.почты')
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Меняем адрес эл.почты')
                self.json_table.change_email_address()
                self.mail_google = EmailManager(login=self.json_table.data.email_login, password=self.json_table.data.email_password)
                raise CreateErrorVsk
            elif self.r.json()["status"] == 'error' and self.r.json()["message"].find('выслан повторно') != -1:
                print('Ждем паузу, которую просит сайт')
                time.sleep(self.r.json()["secondsLeftToSend"])
                raise CreateErrorVsk
            elif self.r.json()["status"] != 'success':
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка сохранения почты')
                raise CreateErrorVsk
            self.r_json = self.r.json()
            print(self.r_json)

            self.start_while_true = datetime.now()
            while True:
                if (datetime.now() - self.start_while_true) > timedelta(minutes=4):
                    self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} ОСАГО долго проверяется сайтом(4 мин.)')
                    raise CreateErrorVsk
                try:
                    self.email_code = self.mail_google.get_last_mail_vsk_code()
                    break
                except NotFindMail:
                    print('Письмо не пришло. Ждём...')

            self.url = f'https://shop.vsk.ru/personal/email/confirm/{self.email_code}'
            self.headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
                'referer': 'https://shop.vsk.ru/osago/calculation/?',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                'host': 'shop.vsk.ru',
            }
            try:
                self.r = self.session.get(self.url, headers=self.headers)
            except:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка проверки кода с почты')
                raise CreateErrorVsk
            if self.r.status_code != 200:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка проверки кода с почты')
                raise CreateErrorVsk
            print(self.r.json())
            if self.r.json()["status"] == 'error' and self.r.json()["message"].find('уже') != -1:
                print('Меняем адрес эл.почты')
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Меняем адрес эл.почты')
                self.json_table.change_email_address()
                self.mail_google = EmailManager(login=self.json_table.data.email_login, password=self.json_table.data.email_password)
                raise CreateErrorVsk
            elif self.r.json()["status"] != 'success':
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка проверки кода с почты')
                raise CreateErrorVsk
            self.r_json = self.r.json()
            print(self.r_json)
            self.point_email_confirmed = True
            self.json_table.change_email_address()  # Меняем, чтобы в следующей попытке была новая почта

        self.url = 'https://shop.vsk.ru/osago/ajax/calculation/check'
        self.data = OsagoData(client_data=self.client_data, session_id=self.session_id)
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://shop.vsk.ru',
            'referer': 'https://shop.vsk.ru/osakgo/calculation/?step=1',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'x-ajax-api-version': '1.3',
            'host': 'shop.vsk.ru',
        }
        self.start_while_true = datetime.now()
        while True:
            if (datetime.now() - self.start_while_true) > timedelta(minutes=4):
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} ОСАГО долго проверяется сайтом(4 мин.)')
                raise CreateErrorVsk
            try:
                self.r = self.session.put(self.url, data=self.data(), headers=self.headers)
            except:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка в заполненных данных')
                raise CreateErrorVsk
            if self.r.status_code != 200:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при загрузке заполненных данных')
                raise CreateErrorVsk
            elif self.r.json()["status"] == 'wait':
                print("Ждем...")
                time.sleep(2)
            elif self.r.json()["status"] == 'success' or self.r.json()["status"] == 'replacement':
                break
            elif self.r.json()["status"] == 'rsaError' or self.r.json()["status"] == 'cant_replacement':
                self.r_json = self.r.json()
                print(self.r_json)
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка в заполненных данных: {re.sub(re.compile("<.*?>"), "", bytes(self.r_json["message"], "ascii").decode("unicode-escape"))}')
                raise CreateErrorVsk
            elif self.r.json()["status"] == 'userError':
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка ВСК при редиректе')
                raise CreateErrorVsk
            else:
                self.r_json = self.r.json()
                print(self.r_json)
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка в заполненных данных')
                raise CreateErrorVsk

        self.start_while_true = datetime.now()
        while True:
            if (datetime.now() - self.start_while_true) > timedelta(minutes=4):
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} ОСАГО долго проверяется сайтом(4 мин.)')
                raise CreateErrorVsk
            self.url = 'https://shop.vsk.ru/osago/ajax/calculation/create'
            self.data = OsagoData(client_data=self.client_data, session_id=self.session_id)
            self.headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://shop.vsk.ru',
                'referer': 'https://shop.vsk.ru/osago/calculation/?step=1',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                'x-ajax-api-version': '1.3',
                'host': 'shop.vsk.ru',
            }
            try:
                self.r = self.session.post(self.url, data=self.data(), headers=self.headers)
            except:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка создания запроса на редирект')
                raise CreateErrorVsk
            if self.r.status_code != 200:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка создания запроса на редирект')
                raise CreateErrorVsk
            print(self.r.json())
            if self.r.json()["status"] == 'success':
                self.json_table.set_value("url_pay", self.r.json()["redirect"])
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Контракт успешно зарезервирован. СК: ВСК')
                break
            elif self.r.json()["status"] == 'error':
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка создания запроса на редирект')
                raise CreateErrorVsk
            elif self.r.json()["status"] == 'userError':
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка ВСК при редиректе')
                raise CreateErrorVsk
            else:
                time.sleep(10)


class CreateErrorVsk(Exception):
    pass