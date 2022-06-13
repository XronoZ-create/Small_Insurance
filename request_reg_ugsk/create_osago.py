from modules.img_captcha import ImgCaptcha
from modules.telephone import Telephone
from config import Config
from bs4 import BeautifulSoup
import time
from contextlib import suppress
from modules.email_manager import EmailManager
from datetime import datetime, timedelta
from modules.rca_methods import RCA

import requests
import json
from request_reg_ugsk.json.save_policy import SavePolicyJson
from request_reg_ugsk.json.save_voditel import SaveVoditelJson
from request_reg_ugsk.json.save_contractor import SaveStrahJson, SaveSobstvJson
from request_reg_ugsk.json.save_vehicle import SaveVehicleJson
from request_reg_ugsk.json.get_contractor import GetContractorJson
from request_reg_ugsk.json.check_policy_osago import CheckPolicyOsagoJson
from request_reg_ugsk.json.osago_start_redirect import OsagoStartRedirectJson
import random


target_dict = {
    "Личная": "Личная",
    "Учебная езда": "УчебнаяЕзда",
    "Регулярные пассажирские перевозки / перевозки пассажиров по заказам":"ПассажирскиеПеревозки",
    "Такси":"Такси",
    "Прокат / краткосрочная аренда": "СдачаВАренду",
    "Перевозка опасных и легко воспламеняющихся грузов": "ОпасныйГруз",
    "Прочее": "Прочее",
    "Дорожные и специальные ТС": "ДорожныеИСпециальныеТС"
}
document_type_dict = {"СТС": "certificate", "ПТС": "passport", "ЭПТС": "ePassport", "ПСМ": "tractorPassport"}

class CreateInsurance:
    def __init__(self, json_table):
        self.session = requests.Session()
        self.session.headers = {
            "Host": "e-osago.ugsk.ru",
            "Connection": "keep-alive",
            "Content-Length": "1515",
            "sec-ch-ua": "\"Chromium\";v=\"94\", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
            "sec-ch-ua-platform": "\"Windows\"",
            "Origin": "https://e-osago.ugsk.ru",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        # ---------------------------------Ставим прокси----------------------------------------------------------------
        if Config.proxies != None:
            self.proxies = Config.proxies
            self.session.proxies = self.proxies
        else:
            self.proxies = None
        # --------------------------------------------------------------------------------------------------------------

        self.json_table = json_table
        self.client_data = json_table.data
        if self.client_data.telephone != "":
            self.telephone = Telephone(
                service=self.client_data.telephone_service,
                id_num=self.client_data.id_num_telephone,
                date=datetime.strptime(self.client_data.reg_date_telephone, "%d.%m %H:%M %Y")
            )
        else:
            self.telephone = Telephone(service=json_table.telephone_service)
        self.mail_google = EmailManager(login=self.client_data.email_login, password=self.client_data.email_password)
        self.img_captcha = ImgCaptcha(service="anticaptcha")

    def auth(self):
        self.session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'Upgrade-Insecure-Requests': '1'
        })

        self.body = {
            'AUTH_FORM': 'Y',
            'TYPE': 'AUTH',
            'backurl': '/osago/policy/index.php',
            'radio-inline': 'email',
            'USER_LOGIN': self.client_data.login_osk,
            'USER_PASSWORD': self.client_data.password_osk,
            'Login': ''
        }
        # self.body = """AUTH_FORM=Y&TYPE=AUTH&backurl=%2Fosago%2Fpolicy%2Findex.php&radio-inline=email&USER_LOGIN=osagoosagoosago777777.7%40gmail.com&USER_PASSWORD=_Z%2Bzs9u65%40&Login="""
        self.r = self.session.post("https://e-osago.ugsk.ru/osago/policy/index.php?login=yes", data=self.body)
        print(self.r.status_code)

        self.r = self.session.post("https://e-osago.ugsk.ru/local/tools/webslon/elpolis.api/", json={"method":"isAuthorized"})
        print(self.r.json())
        if self.r.json()["error"] != 0 or self.r.json()["data"]["isAuthorized"] != True:
            self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при аутентификации')
            raise AuthErrorUGSK
        self.session.headers.pop("Upgrade-Insecure-Requests")
        self.session.headers.update({"Content-Type": "application/json;charset=UTF-8"})

    def create(self):
        # self.tel_number = str(random.randint(8800000000, 8999999999))
        if self.client_data.telephone == "" or \
                (
                    (self.client_data.telephone_service == 'onlinesim' and (datetime.now() - datetime.strptime(self.client_data.reg_date_telephone, "%d.%m %H:%M %Y")) > timedelta(minutes=30)) or
                    ((datetime.now() - datetime.strptime(self.client_data.reg_date_telephone, "%d.%m %H:%M %Y")) > timedelta(minutes=50))
                ):
            self.telephone.update_service(site_service=self.json_table.telephone_service)
            self.tel_number = self.telephone.get_number()["tel"][1:]
            self.json_table.set_value('reg_date_telephone', self.telephone.active_client.date.strftime("%d.%m %H:%M %Y"))
            self.json_table.set_value('telephone', self.tel_number)
            self.json_table.set_value('id_num_telephone', self.telephone.active_client.id_num)
            self.json_table.set_value('telephone_service', self.telephone.active_client.name)
        else:
            self.tel_number = self.client_data.telephone

        # -------------------------------------------Страхователь-------------------------------------------------------
        self.s = SaveStrahJson(
            pass_series=self.client_data.pass_seriya, pass_number=self.client_data.pass_number, name=self.client_data.name,
            lastname=self.client_data.surname, middlename=self.client_data.otchestvo,
            email=self.client_data.email_login, birthday=datetime.strptime(self.client_data.birthday, "%Y-%m-%d").strftime("%d.%m.%Y"),
            telephone=self.tel_number, address=self.client_data.pass_address)
        self.insurer = self.s(SavePolicy=True)

        self.start_while_true = datetime.now()
        while True:
            if (datetime.now() - self.start_while_true) > timedelta(minutes=4):
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")}ОСАГО долго проверяется сайтом(4 мин.)')
                raise CreateErrorUGSK

            self.r = self.session.post("https://e-osago.ugsk.ru/local/tools/webslon/elpolis.api/", data=self.s())
            print(self.r.json())
            if self.r.json().get("error") != 0 and self.r.json().get("msg").find("Сервис в настоящий момент недоступен") == -1:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при сохранении данных страхователя: {self.r.json()["msg"]}')
                raise CreateErrorUGSK
            elif self.r.json().get("error") == 0:
                break
            else:
                time.sleep(random.randrange(5, 50) / 10)

        self.insurer_id = self.r.json()["data"][0]["id"]
        self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Страхователь сохранен')

        # -------------------------------------------Собственник--------------------------------------------------------
        if self.client_data.sobstv_yavl_strah != '"+"':
            self.s = SaveSobstvJson(
                pass_series=self.client_data.sobstv_pass_seriya, pass_number=self.client_data.sobstv_pass_number,
                name=self.client_data.sobstv_name,
                lastname=self.client_data.sobstv_surname, middlename=self.client_data.sobstv_otchestvo,
                birthday=datetime.strptime(self.client_data.sobstv_birthday, "%Y-%m-%d").strftime("%d.%m.%Y"),
                address=self.client_data.sobstv_pass_address)

            self.owner = self.s(SavePolicy=True)

            self.start_while_true = datetime.now()
            while True:
                if (datetime.now() - self.start_while_true) > timedelta(minutes=4):
                    self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")}ОСАГО долго проверяется сайтом(4 мин.)')
                    raise CreateErrorUGSK

                self.r = self.session.post("https://e-osago.ugsk.ru/local/tools/webslon/elpolis.api/", data=self.s())
                print(self.r.json())
                if self.r.json().get("error") != 0 and self.r.json().get("msg").find("Сервис в настоящий момент недоступен") == -1:
                    self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при сохранении данных собственника: {self.r.json()["msg"]}')
                    raise CreateErrorUGSK
                elif self.r.json().get("error") == 0:
                    break
                else:
                    time.sleep(random.randrange(5, 50) / 10)

            self.owner_id = self.r.json()["data"][0]["id"]
            self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Собственник сохранен')

        # -------------------------------------------Водители-----------------------------------------------------------
        if self.client_data.c_ogr_or_not != "Без ограничений":
            self.drivers = []
            self.drivers_id = []
            for self.voditel_data in self.client_data.voditeli:
                if self.voditel_data.surname == "":
                    break
                self.s = SaveVoditelJson(name=self.voditel_data.name, middlename=self.voditel_data.otchestvo, lastname=self.voditel_data.surname,
                                    birthday=datetime.strptime(self.voditel_data.birthday, "%Y-%m-%d").strftime("%d.%m.%Y"),
                                    series_vod=self.voditel_data.seriya_vu,
                                    number_vod=self.voditel_data.nomer_vu, date_vod=datetime.strptime(self.voditel_data.data_vidachi_vu, "%Y-%m-%d").strftime("%d.%m.%Y"),
                                    stag=datetime.strptime(self.voditel_data.nachalo_staga, "%Y-%m-%d").strftime("%d.%m.%Y"),
                                    foreign_dl=self.voditel_data.foreign_dl, tr=self.voditel_data.tr)
                self.drivers.append(self.s(SavePolicy=True))

                self.start_while_true = datetime.now()
                while True:
                    if (datetime.now() - self.start_while_true) > timedelta(minutes=4):
                        self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")}ОСАГО долго проверяется сайтом(4 мин.)')
                        raise CreateErrorUGSK

                    self.r = self.session.post("https://e-osago.ugsk.ru/local/tools/webslon/elpolis.api/", data=self.s())
                    print(self.r.json())
                    if self.r.json().get("error") != 0 and self.r.json().get("msg").find("Сервис в настоящий момент недоступен") == -1:
                        self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при сохранении данных водителя: {self.r.json()["msg"]}')
                        raise CreateErrorUGSK
                    elif self.r.json().get("error") == 0:
                        break
                    else:
                        time.sleep(random.randrange(5, 50) / 10)

                self.drivers_id.append(self.r.json()["data"][0]["id"])
        self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Водители сохранены')

        # -----------------------------------------Машина---------------------------------------------------------------
        self.dict_args_vehicle = {}
        self.dict_args_vehicle["target"] = target_dict[self.client_data.target]
        self.dict_args_vehicle["document_type"] = document_type_dict[self.client_data.type_document]
        self.dict_args_vehicle["reg_number"] = self.client_data.ctc_ptc_reg_znak
        self.dict_args_vehicle["year"] = self.client_data.year
        self.dict_args_vehicle["mark"] = self.client_data.mark
        self.dict_args_vehicle["model"] = self.client_data.model
        self.dict_args_vehicle["category"] = self.client_data.category
        self.dict_args_vehicle["proxies"] = self.proxies

        if self.client_data.type_document == "ПТС" or self.client_data.type_document == "СТС" or self.client_data.type_document == "ПСМ":
            self.dict_args_vehicle["ptc_ctc_series"] = self.client_data.ctc_ptc_seriya
            self.dict_args_vehicle["ptc_ctc_number"] = self.client_data.ctc_ptc_number
            self.dict_args_vehicle["ptc_ctc_date"] = datetime.strptime(self.client_data.ctc_ptc_vidach, "%Y-%m-%d").strftime("%d.%m.%Y")
        elif self.client_data.type_document == "ЭПТС":
            self.dict_args_vehicle["eptc_number"] = self.client_data.ctc_ptc_number
            self.dict_args_vehicle["eptc_date"] = datetime.strptime(self.client_data.ctc_ptc_vidach, "%Y-%m-%d").strftime("%d.%m.%Y")

        if self.client_data.nomer_dk != "":
            self.dict_args_vehicle["diagn_card_number"] = self.client_data.nomer_dk
        if self.client_data.data_TO != "":
            self.dict_args_vehicle["diagn_card_date"] = datetime.strptime(self.client_data.data_TO, "%Y-%m-%d").strftime("%d.%m.%Y")
        if self.client_data.modification != "":
            self.dict_args_vehicle["modification"] = self.client_data.modification
        else:
            self.dict_args_vehicle["power"] = self.client_data.powers
        if self.client_data.type_cusov != "":
            self.dict_args_vehicle["type_body"] = self.client_data.type_cusov
        if self.client_data.type_engine != "":
            self.dict_args_vehicle["type_engine"] = self.client_data.type_engine
        if self.client_data.transmission != "":
            self.dict_args_vehicle["type_kpp"] = self.client_data.transmission
        if self.client_data.ctc_ptc_vin != "":
            self.dict_args_vehicle["vin"] = self.client_data.ctc_ptc_vin
        else:
            self.dict_args_vehicle["chassis_number"] = self.client_data.ctc_ptc_nomer_shassi
            self.dict_args_vehicle["body_number"] = self.client_data.ctc_ptc_nomer_cusov
        if self.client_data.count_pass_mest != "":
            self.dict_args_vehicle["seats_count"] = self.client_data.count_pass_mest
        if self.client_data.max_mass != "":
            self.dict_args_vehicle["max_mass"] = self.client_data.max_mass
        if self.client_data.pricep != "":
            self.dict_args_vehicle["with_trailer"] = self.client_data.pricep
        if self.client_data.other_mark != "":
            self.dict_args_vehicle["other_mark"] = self.client_data.other_mark

        self.s = SaveVehicleJson(**self.dict_args_vehicle)
        self.vehicle = self.s(SavePolicy=True)

        self.start_while_true = datetime.now()
        while True:
            if (datetime.now() - self.start_while_true) > timedelta(minutes=4):
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")}ОСАГО долго проверяется сайтом(4 мин.)')
                raise CreateErrorUGSK

            self.r = self.session.post("https://e-osago.ugsk.ru/local/tools/webslon/elpolis.api/", data=self.s())
            print(self.r.json())
            if self.r.json().get("error") != 0 and self.r.json().get("msg").find("Сервис в настоящий момент недоступен") == -1:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при сохранении данных транспорта: {self.r.json()["msg"]}')
                raise CreateErrorUGSK
            elif self.r.json().get("error") == 0:
                break
            else:
                time.sleep(random.randrange(5, 50) / 10)

        self.vehicle_id = self.r.json()["data"]["id"]
        self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Транспот сохранен')

        # --------------------------------------Отправить ОСАГО---------------------------------------------------------
        if datetime.strptime(self.client_data.OSAGO_start, "%Y-%m-%d") - datetime.now() >= timedelta(days=4):
            self.date_start = datetime.strptime(self.client_data.OSAGO_start, "%Y-%m-%d").strftime("%d.%m.%Y")
        else:
            self.date_start = (datetime.now() + timedelta(days=4)).strftime("%d.%m.%Y")
        self.dict_args_savepolicy = {
            "insurer": self.insurer,
            "insurer_id": self.insurer_id,
            "vehicle": self.vehicle,
            "vehicle_id": self.vehicle_id,
            "dateStart": self.date_start,
            "OSAGO_count_mouth": self.client_data.OSAGO_count_mouth
        }
        if self.client_data.c_ogr_or_not != "Без ограничений":
            self.dict_args_savepolicy["drivers"] = self.drivers
            self.dict_args_savepolicy["drivers_id"] = self.drivers_id
        if self.client_data.sobstv_yavl_strah != '"+"':
            self.dict_args_savepolicy["owner"] = self.owner
            self.dict_args_savepolicy["owner_id"] = self.owner_id

        self.s = SavePolicyJson(**self.dict_args_savepolicy)

        self.start_while_true = datetime.now()
        while True:
            if (datetime.now() - self.start_while_true) > timedelta(minutes=4):
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")}ОСАГО долго проверяется сайтом(4 мин.)')
                raise CreateErrorUGSK

            self.r = self.session.post("https://e-osago.ugsk.ru/local/tools/webslon/elpolis.api/", data=self.s())
            print(self.r.json())
            if self.r.json().get("error") != 0 and self.r.json().get("msg").find("Сервис в настоящий момент недоступен") == -1:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при создании ОСАГО: {self.r.json()["msg"]}')
                raise CreateErrorUGSK
            elif self.r.json().get("error") == 0:
                break
            else:
                time.sleep(random.randrange(5, 50) / 10)

        self.draft_id = self.r.json()["data"]["draftId"]
        self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} ОСАГО сохранено')

        # ---------Для редиректа не обязательно-----------Проверка ОСАГО------------------------------------------------
        # self.s = CheckPolicyOsagoJson(draft_id=self.draft_id)
        # self.start_while_true = datetime.now()
        # while True:
        #     if (datetime.now() - self.start_while_true) > timedelta(minutes=4):
        #         self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")}ОСАГО долго проверяется сайтом(4 мин.)')
        #         raise CreateErrorUGSK
        #     self.r = self.session.post("https://e-osago.ugsk.ru/local/tools/webslon/elpolis.api/", data=self.s())
        #     print(self.r.json())
        #     if self.r.json().get("error") != 0:
        #         self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")}Ошибка при проверке ОСАГО: {self.r.json()["msg"]}')
        #         raise CreateErrorUGSK
        #     elif self.r.json().get("error") == 0 and (self.r.json()["result"]["status"] == "ok" or self.r.json()["result"]["status"] == "selection"):
        #         break
        #     elif self.r.json().get("error") == 0 and self.r.json()["result"]["status"] == "wait":
        #         print("Ждем...")
        #         time.sleep(random.randrange(5, 50) / 10)
        # self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} ОСАГО проверено сайтом')

        self.batut()
        # ---------------------------------------Проверка ОСАГО---------------------------------------------------------
        self.s = CheckPolicyOsagoJson(draft_id=self.draft_id)
        self.start_while_true = datetime.now()
        while True:
            if (datetime.now() - self.start_while_true) > timedelta(minutes=4):
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")}ОСАГО долго проверяется РСА(4 мин.)')
                raise CreateErrorUGSK
            self.r = self.session.post("https://e-osago.ugsk.ru/local/tools/webslon/elpolis.api/", data=self.s())
            print(self.r.json())
            if self.r.json().get("error") != 0:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")}Ошибка при проверке ОСАГО сайтом РСА: {self.r.json()["msg"]}')
                raise CreateErrorUGSK
            elif self.r.json().get("error") == 0 and self.r.json()["result"]["status"] == "selection" and self.r.json()["result"]["selectionFullDataUrl"] != None:
                break
            elif self.r.json().get("error") == 0 and self.r.json()["result"]["status"] == "wait":
                print("Ждем...")
                time.sleep(random.randrange(5, 50) / 10)
        self.json_table.set_value("url_rca", self.r.json()["result"]["selectionFullDataUrl"])
        self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Создана ссылка на РСА')
        return self.r.json()["result"]["selectionFullDataUrl"]

    def rca_create_dog(self, url_rca):
        self.rca_methods_client = RCA(url_token=url_rca, json_table=self.json_table)
        try:
            self.rca_methods_client.reg()
            self.password_rca = self.telephone.get_sms_code()

            self.tel_number = f'7{self.json_table.data.telephone}'
            self.json_table.set_value("login_rca", self.tel_number)
            self.json_table.set_value("password_rca", self.password_rca)

            self.rca_methods_client.login(login_phone=self.tel_number, password=self.password_rca)
            self.rca_methods_client.check_data()
            self.rca_methods_client.logout()
        except:
            self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Проблема с РСА. Берем новый номер')
            self.json_table.set_value('reg_date_telephone', "10.01 10:10 2020")
            self.json_table.set_value('telephone', "")
            self.json_table.set_value('id_num_telephone', "")
            raise Exception

    def batut(self):
        # --------------------------------------Батут ОСАГО-------------------------------------------------------------
        self.start_while_true_batut = datetime.now()
        while True:
            if (datetime.now() - self.start_while_true_batut) > timedelta(minutes=4):
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")}ОСАГО долго оправляет запрос на батут(4 мин.)')
                raise CreateErrorUGSK
            self.s = OsagoStartRedirectJson(draft_id=self.draft_id)
            self.r = self.session.post("https://e-osago.ugsk.ru/local/tools/webslon/elpolis.api/", data=self.s())
            print(self.r.json())
            if self.r.json().get("error") != 0:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")}Ошибка создания запроса на редирект РСА: {self.r.json()["msg"]}')
                raise CreateErrorUGSK
            elif self.r.json()["data"]["return"]["Status"] == True:
                break
            self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Создан запрос на редирект РСА')
            time.sleep(5)

            self.s = CheckPolicyOsagoJson(draft_id=self.draft_id)
            self.r = self.session.post("https://e-osago.ugsk.ru/local/tools/webslon/elpolis.api/", data=self.s())
            print(self.r.json())
            if self.r.json().get("error") != 0:
                self.json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")}Ошибка при проверке ОСАГО сайтом РСА: {self.r.json()["msg"]}')
                raise CreateErrorUGSK


class AuthErrorUGSK(Exception):
    pass
class CreateErrorUGSK(Exception):
    pass