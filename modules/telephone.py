import requests
from datetime import datetime, timedelta
import time
from contextlib import suppress
from config import Config

class Telephone:
    def __init__(self, service, id_num=None, date=None, tel=None):
        self.service = service
        self.client_vak = TelephoneVakSms(id_num=id_num, date=date, tel=tel)
        self.client_onlinesim = TelephoneOnlineSim(id_num=id_num, date=date, tel=tel)
        self.client_activate = TelephoneActivateSms(id_num=id_num, date=date, tel=tel)

        if id_num != None:
            if self.service == "onlinesim":
                self.active_client = self.client_onlinesim
            elif self.service == "vak":
                self.active_client = self.client_vak
            elif self.service == "activate":
                self.active_client = self.client_activate

    def get_number(self):
        try:
            self.count_free_num_vak = self.client_vak.check_free_num()
        except:
            self.count_free_num_vak = 0
        try:
            self.count_free_num_onlinesim = self.client_onlinesim.check_free_num()
        except:
            self.count_free_num_onlinesim = 0
        try:
            self.count_free_num_activate = self.client_activate.check_free_num()
        except:
            self.count_free_num_activate = 0


        if self.service == "any":
            if self.count_free_num_vak != 0:
                self.active_client = self.client_vak
            elif self.count_free_num_activate != 0:
                self.active_client = self.client_activate
            elif self.count_free_num_onlinesim != 0:
                self.active_client = self.client_onlinesim
            else:
                raise GetNumberFailed
        elif self.service == "onlinesim":
            self.active_client = self.client_onlinesim
        elif self.service == "vak":
            self.active_client = self.client_vak
        elif self.service == "activate":
            self.active_client = self.client_activate

        self.resp_client = self.active_client.get_number()
        return self.resp_client

    def get_sms_code(self):
        self.resp_client = self.active_client.get_sms_code()
        return self.resp_client

    def end_number(self):
        with suppress(Exception):
            self.active_client.end_number()

    def check_lifetime(self):
        self.resp_client = self.active_client.check_lifetime()
        return self.resp_client

    def update_service(self, site_service):
        if site_service == "any":
            try:
                self.count_free_num_vak = self.client_vak.check_free_num()
            except:
                self.count_free_num_vak = 0
            try:
                self.count_free_num_onlinesim = self.client_onlinesim.check_free_num()
            except:
                self.count_free_num_onlinesim = 0
            try:
                self.count_free_num_activate = self.client_activate.check_free_num()
            except:
                self.count_free_num_activate = 0
            if self.count_free_num_vak != 0:
                self.active_client = self.client_vak
            elif self.count_free_num_activate != 0:
                self.active_client = self.client_activate
            elif self.count_free_num_onlinesim != 0:
                self.active_client = self.client_onlinesim
            else:
                raise GetNumberFailed
        elif site_service == "onlinesim":
            self.active_client = self.client_onlinesim
        elif site_service == "vak":
            self.active_client = self.client_vak
        elif site_service == "activate":
            self.active_client = self.client_activate

    @property
    def tel(self):
        return self.active_client.tel

    @property
    def sms_codes(self):
        return self.active_client.sms_codes


class TelephoneVakSms:
    def __init__(self, id_num=None, date=None, tel=None):
        self.name = 'vak'
        self.api_key = Config.vak_sms_api_key
        self.tel = tel
        self.sms_codes = None
        self.id_num = id_num
        self.date = date

    def get_number(self):
        self.url = "https://vak-sms.com/api/getNumber/?apiKey={apiKey}&service={service}&operator={operator}".format(
            apiKey=self.api_key,
            service="strh",
            operator="beeline"
        )
        self.r = requests.get(self.url)
        self.r_json = self.r.json()
        if self.r_json.get("idNum") == None:
            raise GetNumberFailed
        self.id_num = self.r_json["idNum"]
        self.tel = str(self.r_json["tel"])
        self.date = datetime.now()
        return {'tel': self.tel}

    def get_sms_code(self):
        self.url = "https://vak-sms.com/api/getSmsCode/?apiKey={apiKey}&idNum={idNum}&all".format(
            apiKey=self.api_key,
            idNum=self.id_num
        )
        self.start_wait_sms = datetime.now()
        while True:
            if (datetime.now() - self.start_wait_sms) > timedelta(minutes=5):
                self.end_number()
                raise LongWaitSmsCode
            with suppress(Exception):
                self.r = requests.get(self.url)
                self.r_json = self.r.json()
                if self.r_json.get('error') != None:
                    raise GetNumberFailed
                self.sms_codes = self.r_json['smsCode']
                if self.sms_codes == None:
                    print(f'Еще не пришло sms:{self.r_json}')
                elif self.sms_codes[-1] != None:
                    return self.sms_codes[-1]
                time.sleep(5)

    def end_number(self):
        self.url = "https://vak-sms.com/api/setStatus/?apiKey={apiKey}&idNum={idNum}&status={status}".format(
            apiKey=self.api_key,
            idNum = self.id_num,
            status="end"
        )
        self.r = requests.get(self.url)

    def check_lifetime(self):
        if (datetime.now() - self.date) >= timedelta(minutes=50):
            print("Старый номер")
            self.end_number()
            raise OldNumberFailed
        else:
            return True

    def check_free_num(self):
        self.url = "https://vak-sms.com/api/getCountNumber/?apiKey={apiKey}&service={service}&operator={operator}".format(
            apiKey=self.api_key,
            service="strh",
            operator="beeline"
        )
        self.r = requests.get(self.url)
        self.r_json = self.r.json()
        self.count_free_num = self.r_json["strh"]

class TelephoneOnlineSim:
    def __init__(self, id_num=None, date=None, tel=None):
        self.name = 'onlinesim'
        self.api_key = Config.online_sim_api_key
        self.tel = tel
        self.sms_codes = None
        self.id_num = id_num
        self.date = date

    def get_number(self, service="e-garant"):
        self.url = "https://onlinesim.ru/api/getNum.php?apikey={apiKey}&service={service}".format(
            apiKey=self.api_key,
            service=service
        )
        self.r = requests.get(self.url)
        self.r_json = self.r.json()
        print(self.r_json)
        if self.r_json["response"] != 1:
            raise GetNumberFailed
        self.id_num = self.r_json["tzid"]

        self.start_wait_sms = datetime.now()
        while True:
            if (datetime.now() - self.start_wait_sms) > timedelta(minutes=5):
                raise GetNumberFailed
            self.get_state()
            if self.tel != None:
                self.date = datetime.now()
                return {'tel': self.tel}

    def get_state(self):
        self.url = "https://onlinesim.ru/api/getState.php?apikey={apiKey}&tzid={tzid}&message_to_code=1&msg_list=0".format(
            apiKey=self.api_key,
            tzid=self.id_num
        )
        self.r = requests.get(self.url)
        self.r_json = self.r.json()[0]
        # print(self.r_json)

        if self.r_json["response"] == "TZ_NUM_ANSWER":
            self.tel = self.r_json["number"][1:]
            self.sms_codes = self.r_json["msg"]
        elif self.r_json["response"] == "TZ_NUM_WAIT":
            self.tel = self.r_json["number"][1:]
            print(f'Еще не пришло sms:{self.r_json}')
        else:
            raise GetNumberFailed

    def get_sms_code(self):
        self.start_wait_sms = datetime.now()
        while True:
            if (datetime.now() - self.start_wait_sms) > timedelta(minutes=5):
                raise LongWaitSmsCode
            self.get_state()
            if self.sms_codes != None:
                return self.sms_codes
            time.sleep(5)

    def check_lifetime(self):
        if (datetime.now() - self.date) >= timedelta(minutes=25):
            print("Старый номер")
            raise OldNumberFailed
        else:
            return True

    def check_free_num(self):
        self.url = "https://onlinesim.ru/api/getNumbersStats.php?apikey={apiKey}".format(apiKey=self.api_key)
        self.r = requests.get(self.url)
        self.r_json = self.r.json()

        self.count_free_num = self.r_json["services"]["service_e-garant"]["count"]

class TelephoneActivateSms:
    def __init__(self, id_num=None, date=None, tel=None):
        self.name = 'activate'
        self.api_key = Config.activate_sms_api_key
        self.tel = tel
        self.sms_codes = None
        self.id_num = id_num
        self.date = date

    def get_number(self, service="cy"):
        self.url = "https://api.sms-activate.org/stubs/handler_api.php?api_key={apiKey}&action=getNumber&service={service}&operator={operator}&country={country}".format(
            apiKey=self.api_key,
            service=service,
            operator="beeline",
            country="0"
        )
        self.r = requests.get(self.url)
        self.r_split = self.r.text.split(":")
        print(self.r_split)
        if self.r_split[0] == "ACCESS_NUMBER":
            self.id_num = self.r_split[1]
            self.tel = str(self.r_split[2])
            self.date = datetime.now()

            self.url = "https://api.sms-activate.org/stubs/handler_api.php?api_key={apiKey}&action=setStatus&status={status}&id={idNum}".format(
                apiKey=self.api_key,
                idNum=self.id_num,
                status="1"
            )
            self.r = requests.get(self.url)

            return {'tel': self.tel}
        else:
            print(f"Ошибка при получении номера: {self.r_split}")
            raise GetNumberFailed

    def get_sms_code(self):
        self.url = "https://api.sms-activate.org/stubs/handler_api.php?api_key={apiKey}&action=getStatus&id={idNum}".format(
            apiKey=self.api_key,
            idNum=self.id_num
        )
        self.start_wait_sms = datetime.now()
        while True:
            if (datetime.now() - self.start_wait_sms) > timedelta(minutes=5):
                self.end_number()
                raise LongWaitSmsCode

            self.r = requests.get(self.url)
            self.r_split = self.r.text.split(":")
            print(self.r_split)
            if self.r_split[0] == "STATUS_WAIT_CODE" or self.r_split[0] == "" or self.r_split[0] == "STATUS_WAIT_RESEND" or self.r_split[0] == "STATUS_WAIT_RETRY":
                print(f'Еще не пришло sms:{self.r_split}')
            elif self.r_split[0] == "STATUS_OK":
                if "Югория" in self.r_split[1]:
                    self.sms_codes = self.r_split[1].split("Ваш код ")[1].split(".")[0]
                    print("Пришел код:", self.sms_codes)
                elif len(self.r_split) == 3 and "Просьба соблюдать конфиденциальность" in self.r_split[2]:
                    self.sms_codes = self.r_split[2].replace("\n\nПросьба соблюдать конфиденциальность информации", "").replace(" ", "")
                    print("Пришел код:", self.sms_codes)
                else:
                    self.sms_codes = ":".join(self.r_split[1:]).split(": ")[1].split('.')[0].replace(" ", '')
                    print("Пришел код:", self.sms_codes)
                return self.sms_codes
            else:
                raise GetNumberFailed

            time.sleep(5)

    def end_number(self):
        pass
        # self.url = "https://api.sms-activate.org/stubs/handler_api.php?api_key={apiKey}&action=setStatus&status={status}&id={idNum}".format(
        #     apiKey=self.api_key,
        #     idNum = self.id_num,
        #     status="8"
        # )
        # self.r = requests.get(self.url)

    def check_lifetime(self):
        if (datetime.now() - self.date) >= timedelta(minutes=50):
            print("Старый номер")
            self.end_number()
            raise OldNumberFailed
        else:
            return True

    def check_free_num(self):
        self.url = "https://api.sms-activate.org/stubs/handler_api.php?api_key={apiKey}&action=getNumbersStatus&country={country}&operator={operator}".format(
            apiKey=self.api_key,
            country="0",
            operator="beeline"
        )
        self.r = requests.get(self.url)
        self.r_json = self.r.json()
        print(self.r_json)
        self.count_free_num = int(self.r_json["cy_0"])

    def retry_sms(self):
        self.url = "https://api.sms-activate.org/stubs/handler_api.php?api_key={apiKey}&action=setStatus&status={status}&id={idNum}".format(
            apiKey=self.api_key,
            idNum=self.id_num,
            status="3"
        )
        self.r = requests.get(self.url)

class GetNumberFailed(Exception):
    pass
class ServiceWaitSms(Exception):
    pass
class OldNumberFailed(Exception):
    pass
class LongWaitSmsCode(Exception):
    pass