import requests
from typing import List
from pydantic import BaseModel
from config import Config

class JsonTable:
    def __init__(self):
        self.resp_json = requests.post(Config.site_address + "api/check_task", json={"KEY": Config.API_KEY}).json()
        self.type = self.resp_json["type"]
        if self.resp_json["data"] != None and self.type == "osago_osk":
            self.data = PydanticOsagoOsk(**self.resp_json["data"])
        elif self.resp_json["data"] != None and self.type == "hook":
            self.data = PydanticHook(**self.resp_json["data"])
        elif self.resp_json["data"] != None and self.type == "osago_ugsk":
            self.data = PydanticOsagoUGSK(**self.resp_json["data"])
        elif self.resp_json["data"] != None and self.type == "osago_21":
            self.data = PydanticOsago21(**self.resp_json["data"])
        elif self.resp_json["data"] != None and self.type == "osago_arm":
            self.data = PydanticOsagoArm(**self.resp_json["data"])
        elif self.resp_json["data"] != None and self.type == "osago_alfa":
            self.data = PydanticOsagoAlfa(**self.resp_json["data"])
        elif self.resp_json["data"] != None and self.type == "osago_vsk":
            self.data = PydanticOsagoVsk(**self.resp_json["data"])
        else:
            self.data = None

    def set_value(self, name, value):
        self.resp_json = requests.post(
            Config.site_address+"api/set_value",
            json={"KEY": Config.API_KEY, "name": name, "value": value, "id": self.data.id, "type": self.type}
        ).json()
        print(self.resp_json)
        if self.type == "osago_osk":
            self.data = PydanticOsagoOsk(**self.resp_json["update_data"])
        elif self.type == "hook":
            self.data = PydanticHook(**self.resp_json["update_data"])
        elif self.type == "osago_ugsk":
            self.data = PydanticOsagoUGSK(**self.resp_json["update_data"])
        elif self.type == "osago_21":
            self.data = PydanticOsago21(**self.resp_json["update_data"])
        elif self.type == "osago_arm":
            self.data = PydanticOsagoArm(**self.resp_json["update_data"])
        elif self.type == "osago_alfa":
            self.data = PydanticOsagoAlfa(**self.resp_json["update_data"])
        elif self.type == "osago_vsk":
            self.data = PydanticOsagoVsk(**self.resp_json["update_data"])


    def stop_bot(self):
        if self.type == "osago_osk":
            self.resp_json = requests.post(Config.site_address+"api/stop_osago",
                json={"KEY": Config.API_KEY, "osago_id": self.data.id, "type_osago": "osago_osk"}
            ).json()
        elif self.type == "hook":
            self.resp_json = requests.post(Config.site_address+"api/stop_hook",
                json={"KEY": Config.API_KEY, "hook_id": self.data.id}
            ).json()
        elif self.type == "osago_ugsk":
            self.resp_json = requests.post(Config.site_address+"api/stop_osago",
                json={"KEY": Config.API_KEY, "osago_id": self.data.id, "type_osago": "osago_ugsk"}
            ).json()
        elif self.type == "osago_21":
            self.resp_json = requests.post(Config.site_address+"api/stop_osago",
                json={"KEY": Config.API_KEY, "osago_id": self.data.id, "type_osago": "osago_21"}
            ).json()
        elif self.type == "osago_arm":
            self.resp_json = requests.post(Config.site_address+"api/stop_osago",
                json={"KEY": Config.API_KEY, "osago_id": self.data.id, "type_osago": "osago_arm"}
            ).json()
        elif self.type == "osago_alfa":
            self.resp_json = requests.post(Config.site_address+"api/stop_osago",
                json={"KEY": Config.API_KEY, "osago_id": self.data.id, "type_osago": "osago_alfa"}
            ).json()
        elif self.type == "osago_vsk":
            self.resp_json = requests.post(Config.site_address + "api/stop_osago",
               json={"KEY": Config.API_KEY, "osago_id": self.data.id, "type_osago": "osago_vsk"}
               ).json()

    def change_email_address(self):
        self.resp_json = requests.post(
            Config.site_address + "api/change_email_address",
            json={"KEY": Config.API_KEY, "id": self.data.id, "type": self.type}
        ).json()
        print(self.resp_json)
        if self.type == "osago_osk":
            self.data = PydanticOsagoOsk(**self.resp_json["update_data"])
        elif self.type == "osago_ugsk":
            self.data = PydanticOsagoUGSK(**self.resp_json["update_data"])
        elif self.type == "osago_21":
            self.data = PydanticOsago21(**self.resp_json["update_data"])
        elif self.type == "osago_arm":
            self.data = PydanticOsagoArm(**self.resp_json["update_data"])
        elif self.type == "osago_alfa":
            self.data = PydanticOsagoAlfa(**self.resp_json["update_data"])
        elif self.type == "osago_vsk":
            self.data = PydanticOsagoVsk(**self.resp_json["update_data"])

    @property
    def active(self):
        self.resp_json = requests.post(Config.site_address + "api/check_task", json={"KEY": Config.API_KEY}).json()
        if self.resp_json["data"] == None:
            return False
        else:
            if self.type == "osago_osk":
                self.data = PydanticOsagoOsk(**self.resp_json["data"])
            elif self.type == "osago_ugsk":
                self.data = PydanticOsagoUGSK(**self.resp_json["data"])
            elif self.type == "osago_21":
                self.data = PydanticOsago21(**self.resp_json["data"])
            elif self.type == "osago_arm":
                self.data = PydanticOsagoArm(**self.resp_json["data"])
            elif self.type == "osago_alfa":
                self.data = PydanticOsagoAlfa(**self.resp_json["data"])
            elif self.type == "osago_vsk":
                self.data = PydanticOsagoVsk(**self.resp_json["data"])
            return True

    @property
    def telephone_service(self):
        return requests.post(Config.site_address + "api/telephone_service", json={"KEY": Config.API_KEY}).json()["telephone_service"]


class PydanticVoditeliOsk(BaseModel):
    surname: str
    name: str
    otchestvo: str
    birthday: str
    seriya_vu: str
    nomer_vu: str
    data_vidachi_vu: str
    nachalo_staga: str

class PydanticOsagoOsk(BaseModel):
    id: int

    type_osago: str

    url_rca: str
    login_rca: str
    password_rca: str

    login_osk: str
    password_osk: str

    email_login: str
    email_password: str

    surname: str
    name: str
    otchestvo: str
    birthday: str
    pass_seriya: str
    pass_number: str
    pass_vidach: str
    pass_address: str

    sobstv_yavl_strah: str
    sobstv_surname: str
    sobstv_name: str
    sobstv_otchestvo: str
    sobstv_birthday: str
    sobstv_pass_seriya: str
    sobstv_pass_number: str
    sobstv_pass_vidach: str
    sobstv_pass_address: str

    target: str
    mark: str
    model: str
    other_mark: str
    year: str
    powers: str
    type_engine: str
    type_cusov: str
    transmission: str
    modification: str
    category: str

    max_mass: str
    pricep: str

    count_pass_mest: str

    type_document: str

    ctc_ptc_seriya: str
    ctc_ptc_number: str
    ctc_ptc_vidach: str
    ctc_ptc_reg_znak: str
    ctc_ptc_vin: str
    ctc_ptc_nomer_shassi: str
    ctc_ptc_nomer_cusov: str

    nomer_dk: str
    data_TO: str

    c_ogr_or_not: str

    voditeli: List[PydanticVoditeliOsk]

    OSAGO_start: str
    OSAGO_count_mouth: str

    strah_comp: str

    trans_num: str
    est_price_policy: str
    real_price_policy: str
    num_group_wa: str

    status_bot: str

    reg_date_telephone: str
    telephone: str
    id_num_telephone: str
    telephone_service: str

class PydanticHook(BaseModel):
    id: int
    input_url: str
    url_rca: str
    strah_comp: str
    status_bot: str



class PydanticVoditeliUGSK(BaseModel):
    surname: str
    name: str
    otchestvo: str
    birthday: str
    seriya_vu: str
    nomer_vu: str
    data_vidachi_vu: str
    nachalo_staga: str
    foreign_dl: bool
    tr: bool

class PydanticOsagoUGSK(BaseModel):
    id: int

    type_osago: str

    url_rca: str
    login_rca: str
    password_rca: str

    login_osk: str
    password_osk: str

    email_login: str
    email_password: str

    surname: str
    name: str
    otchestvo: str
    birthday: str
    pass_seriya: str
    pass_number: str
    pass_vidach: str
    pass_address: str

    sobstv_yavl_strah: str
    sobstv_surname: str
    sobstv_name: str
    sobstv_otchestvo: str
    sobstv_birthday: str
    sobstv_pass_seriya: str
    sobstv_pass_number: str
    sobstv_pass_vidach: str
    sobstv_pass_address: str

    target: str
    mark: str
    model: str
    other_mark: str
    year: str
    powers: str
    type_engine: str
    type_cusov: str
    transmission: str
    modification: str
    category: str

    max_mass: str
    pricep: str

    count_pass_mest: str

    type_document: str

    ctc_ptc_seriya: str
    ctc_ptc_number: str
    ctc_ptc_vidach: str
    ctc_ptc_reg_znak: str
    ctc_ptc_vin: str
    ctc_ptc_nomer_shassi: str
    ctc_ptc_nomer_cusov: str

    nomer_dk: str
    data_TO: str

    c_ogr_or_not: str

    voditeli: List[PydanticVoditeliUGSK]

    OSAGO_start: str
    OSAGO_count_mouth: str

    strah_comp: str

    trans_num: str
    est_price_policy: str
    real_price_policy: str
    num_group_wa: str

    status_bot: str

    reg_date_telephone: str
    telephone: str
    id_num_telephone: str
    telephone_service: str


class PydanticVoditeli21(BaseModel):
    surname: str
    name: str
    otchestvo: str
    birthday: str
    seriya_vu: str
    nomer_vu: str
    data_vidachi_vu: str
    nachalo_staga: str
    foreign_dl: bool
    tr: bool

class PydanticOsago21(BaseModel):
    id: int

    type_osago: str

    url_rca: str
    login_rca: str
    password_rca: str

    login_osk: str
    password_osk: str

    email_login: str
    email_password: str

    surname: str
    name: str
    otchestvo: str
    birthday: str
    pass_seriya: str
    pass_number: str
    pass_vidach: str
    pass_address: str
    strah_type_document: str

    sobstv_yavl_strah: str
    sobstv_surname: str
    sobstv_name: str
    sobstv_otchestvo: str
    sobstv_birthday: str
    sobstv_pass_seriya: str
    sobstv_pass_number: str
    sobstv_pass_vidach: str
    sobstv_pass_address: str
    sobstv_type_document: str

    target: str
    mark: str
    model: str
    other_mark: str
    year: str
    powers: str
    type_engine: str
    type_cusov: str
    transmission: str
    modification: str
    category: str

    max_mass: str
    pricep: str

    count_pass_mest: str

    type_document: str

    ctc_ptc_seriya: str
    ctc_ptc_number: str
    ctc_ptc_vidach: str
    ctc_ptc_reg_znak: str
    ctc_ptc_vin: str
    ctc_ptc_nomer_shassi: str
    ctc_ptc_nomer_cusov: str

    nomer_dk: str
    data_TO: str

    c_ogr_or_not: str

    voditeli: List[PydanticVoditeli21]

    OSAGO_start: str
    OSAGO_count_mouth: str

    strah_comp: str

    trans_num: str
    est_price_policy: str
    real_price_policy: str
    num_group_wa: str

    status_bot: str

    reg_date_telephone: str
    telephone: str
    id_num_telephone: str
    telephone_service: str


class PydanticVoditeliArm(BaseModel):
    surname: str
    name: str
    otchestvo: str
    birthday: str
    seriya_vu: str
    nomer_vu: str
    data_vidachi_vu: str
    nachalo_staga: str
    foreign_dl: bool
    tr: bool

class PydanticOsagoArm(BaseModel):
    id: int

    type_osago: str

    url_rca: str
    login_rca: str
    password_rca: str

    login_osk: str
    password_osk: str

    email_login: str
    email_password: str

    surname: str
    name: str
    otchestvo: str
    birthday: str
    pass_seriya: str
    pass_number: str
    pass_vidach: str
    pass_address: str

    sobstv_yavl_strah: str
    sobstv_surname: str
    sobstv_name: str
    sobstv_otchestvo: str
    sobstv_birthday: str
    sobstv_pass_seriya: str
    sobstv_pass_number: str
    sobstv_pass_vidach: str
    sobstv_pass_address: str

    target: str
    mark: str
    model: str
    other_mark: str
    year: str
    powers: str
    type_engine: str
    type_cusov: str
    transmission: str
    modification: str
    category: str

    max_mass: str
    pricep: str

    count_pass_mest: str

    type_document: str

    ctc_ptc_seriya: str
    ctc_ptc_number: str
    ctc_ptc_vidach: str
    ctc_ptc_reg_znak: str
    ctc_ptc_vin: str
    ctc_ptc_nomer_shassi: str
    ctc_ptc_nomer_cusov: str

    nomer_dk: str
    data_TO: str

    c_ogr_or_not: str

    voditeli: List[PydanticVoditeliArm]

    OSAGO_start: str
    OSAGO_count_mouth: str

    strah_comp: str

    trans_num: str
    est_price_policy: str
    real_price_policy: str
    num_group_wa: str

    status_bot: str

    reg_date_telephone: str
    telephone: str
    id_num_telephone: str
    telephone_service: str


class PydanticVoditeliAlfa(BaseModel):
    surname: str
    name: str
    otchestvo: str
    birthday: str
    seriya_vu: str
    nomer_vu: str
    data_vidachi_vu: str
    nachalo_staga: str
    foreign_dl: bool
    tr: bool

class PydanticOsagoAlfa(BaseModel):
    id: int

    type_osago: str

    login_parea: str
    password_parea: str

    email_login: str
    email_password: str

    surname: str
    name: str
    otchestvo: str
    birthday: str
    pass_seriya: str
    pass_number: str
    pass_vidach: str
    pass_address: str

    sobstv_yavl_strah: str
    sobstv_surname: str
    sobstv_name: str
    sobstv_otchestvo: str
    sobstv_birthday: str
    sobstv_pass_seriya: str
    sobstv_pass_number: str
    sobstv_pass_vidach: str
    sobstv_pass_address: str

    target: str
    category: str
    year: str
    powers: str
    auto_region: str
    auto_type: str
    brand_name: str
    brand: str
    brand_name_other: str
    model: str
    model_name_other: str
    model_name: str
    modification: str
    modification_name: str

    max_mass: str
    pricep: str

    count_pass_mest: str

    type_document: str

    ctc_ptc_seriya: str
    ctc_ptc_number: str
    ctc_ptc_vidach: str
    ctc_ptc_reg_znak: str
    ctc_ptc_vin: str
    ctc_ptc_nomer_shassi: str
    ctc_ptc_nomer_cusov: str

    nomer_dk: str
    data_TO: str

    c_ogr_or_not: str

    voditeli: List[PydanticVoditeliAlfa]

    OSAGO_start: str
    OSAGO_count_mouth: str

    strah_comp: str

    trans_num: str
    est_price_policy: str
    real_price_policy: str
    num_group_wa: str

    status_bot: str

    reg_date_telephone: str
    telephone: str
    id_num_telephone: str
    telephone_service: str

    url_pay: str

class PydanticVoditeliVsk(BaseModel):
    surname: str
    name: str
    otchestvo: str
    birthday: str
    seriya_vu: str
    nomer_vu: str
    data_vidachi_vu: str
    nachalo_staga: str
    foreign_dl: bool
    tr: bool

    class Config:
        orm_mode = True

class PydanticOsagoVsk(BaseModel):
    id: int

    session_cookies: str
    session_cookies_date: str
    session_id: str

    type_osago: str

    login_parea: str
    password_parea: str

    email_login: str
    email_password: str

    surname: str
    name: str
    otchestvo: str
    birthday: str
    pass_seriya: str
    pass_number: str
    pass_vidach: str
    city_strah: str
    street_strah: str
    building_strah: str
    house_strah: str
    apartment_strah: str
    postal_code_strah: str
    strah_type_document: str

    sobstv_yavl_strah: str
    sobstv_surname: str
    sobstv_name: str
    sobstv_otchestvo: str
    sobstv_birthday: str
    sobstv_pass_seriya: str
    sobstv_pass_number: str
    sobstv_pass_vidach: str
    city_sobstv: str
    street_sobstv: str
    building_sobstv: str
    house_sobstv: str
    apartment_sobstv: str
    postal_code_sobstv: str
    sobstv_type_document: str

    target: str
    category: str
    year: str
    powers: str
    mark: str
    model: str
    mark_name_other: str
    model_name_other: str
    mark_id: str
    model_id: str

    max_mass: str
    pricep: str
    count_pass_mest: str

    type_document: str

    ctc_ptc_seriya: str
    ctc_ptc_number: str
    ctc_ptc_vidach: str
    ctc_ptc_reg_znak: str
    ctc_ptc_vin: str
    ctc_ptc_nomer_shassi: str
    ctc_ptc_nomer_cusov: str

    nomer_dk: str
    data_TO: str

    c_ogr_or_not: str

    voditeli: List[PydanticVoditeliVsk]

    OSAGO_start: str
    OSAGO_count_mouth: str

    strah_comp: str

    trans_num: str
    est_price_policy: str
    real_price_policy: str
    num_group_wa: str

    status_bot: str

    reg_date_telephone: str
    telephone: str
    id_num_telephone: str
    telephone_service: str

    url_pay: str