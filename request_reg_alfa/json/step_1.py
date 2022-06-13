import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from urllib.parse import quote, quote_plus
from urllib.parse import urlencode, parse_qs, parse_qsl

from request_reg_alfa.json.get_address import GetAddressJson

class SaveAuto:
    def __init__(self, client_data, session_id):
        self.data = {
            "sessid": session_id,
            "modification_name": client_data.modification_name,
            "AUTO_COUNTRY": "RUS",
            "AnotherLicensePlate": "",
            "CarIdType": "VIN",
            "CarIdVIN": client_data.ctc_ptc_vin,
            "autoCompleteByAutoNumberEnabled": "Y",
            "fpid": "",
            "category": client_data.category,
            "type": client_data.auto_type,
            "brand_name": client_data.brand_name,
            "brand": client_data.brand,
            "brand_name_other": client_data.brand_name_other,
            "model_name_other": client_data.model_name_other,
            "model_name": client_data.model_name,
            "model": client_data.model,
            "year": client_data.year,
            "yearIssue": "",
            "modification": client_data.modification,
            "carPower": client_data.powers,
            "carPowerKvt": "",
            "purposeName": client_data.target,
            "currentPolicySerial": "ХХХ",
            "currentPolicyNumber": ""
        }
        if client_data.ctc_ptc_reg_znak != "":
            self.data["AUTO_NUMBER"] = f"{client_data.ctc_ptc_reg_znak[0:1]} {client_data.ctc_ptc_reg_znak[1:4]} {client_data.ctc_ptc_reg_znak[4:]}"
            self.data["AUTO_REGION"] = client_data.auto_region
        else:
            self.data["AUTO_NUMBER"] = client_data.ctc_ptc_reg_znak
            self.data["AUTO_REGION"] = client_data.auto_region
            self.data['NO_REGISTRATION'] = 'Y'


        if client_data.ctc_ptc_vin != "":
            self.data['CarIdType'] = "VIN"
            self.data['CarIdVIN'] = client_data.ctc_ptc_vin
        elif client_data.ctc_ptc_nomer_cusov != "":
            self.data['CarIdType'] = "BodyNumber"
            self.data['CarIdBodyNumber'] = client_data.ctc_ptc_nomer_cusov
        elif client_data.ctc_ptc_nomer_shassi != "":
            self.data['CarIdType'] = "ChassisNumber"
            self.data['CarIdChassisNumber'] = client_data.ctc_ptc_nomer_shassi

        if client_data.auto_type == 'Грузовой а/м':
            self.data['Weight'] = client_data.max_mass
        elif client_data.auto_type == 'Автобусы':
            self.data['Seats'] = client_data.count_pass_mest

    def __call__(self, *args, **kwargs):
        return urlencode(self.data)


class SaveVoditelAndOwnerAddress:
    def __init__(self, client_data, calculation_id):
        if datetime.strptime(client_data.OSAGO_start, "%Y-%m-%d") - datetime.now() >= timedelta(days=4):
            self.date_start = datetime.strptime(client_data.OSAGO_start, "%Y-%m-%d").strftime("%d.%m.%Y")
        else:
            self.date_start = (datetime.now() + timedelta(days=4)).strftime("%d.%m.%Y")

        self.registrationAddress = GetAddressJson(address=client_data.pass_address)()
        self.data = {
            "back_url": f"/individuals/auto/eosago/calc/mod/?id={calculation_id}",


            "ownerAddressRegionState": self.registrationAddress['RegionState'],
            "ownerAddressCity": self.registrationAddress['City'],
            "ownerAddressStreet": self.registrationAddress['Street'],
            "ownerAddressHouseRaw": self.registrationAddress['HouseRaw'],
            "ownerAddressApartment": self.registrationAddress['Apartment'],
            "IsInsurerSameAddress": "Y",
            "ownerAddressBuilding": self.registrationAddress['Building'],
            "ownerAddressZip": self.registrationAddress['Zip'],
            "ownerAddressState": self.registrationAddress['State'],
            "ownerAddressRegion": self.registrationAddress['Region'],
            "ownerAddressCountryName": self.registrationAddress['CountryName'],
            "ownerAddressHouse": self.registrationAddress['HouseRaw'],
            "ownerAddressCountryCode": self.registrationAddress['CountryCode'],
            "ownerAddress": self.registrationAddress['Address'],
            "ownerAddressSeparated": self.registrationAddress['Separated'],

            "driversMinLegalAge": "18",

            "ownerSurname": client_data.sobstv_surname,
            "ownerName": client_data.sobstv_name,
            "ownerPatronymic": client_data.sobstv_otchestvo,
            "ownerBirthDate": datetime.strptime(client_data.sobstv_birthday, "%Y-%m-%d").strftime("%d.%m.%Y"),
            "ownerSerial": client_data.sobstv_pass_seriya,
            "ownerNumber": client_data.sobstv_pass_number,
            "ownerSnils": "",

            "submit_step1": ""
        }
        if client_data.voditeli[0].surname != "":
            self.data['driversNumber'] = "limited"
            self.i_vod = 1
            for self.vod in client_data.voditeli:
                if self.vod.surname == "":
                    break
                self.data[f'driver[{self.i_vod}][Surname]'] = self.vod.surname
                self.data[f'driver[{self.i_vod}][Name]'] = self.vod.name
                self.data[f'driver[{self.i_vod}][Patronymic]'] = self.vod.otchestvo
                self.data[f'driver[{self.i_vod}][BirthDate]'] = datetime.strptime(self.vod.birthday, "%Y-%m-%d").strftime("%d.%m.%Y")
                self.data[f'driver[{self.i_vod}][Serial]'] = self.vod.seriya_vu
                self.data[f'driver[{self.i_vod}][Number]'] = self.vod.nomer_vu
                self.data[f'driver[{self.i_vod}][DateIssue]'] = datetime.strptime(self.vod.nachalo_staga, "%Y-%m-%d").strftime("%d.%m.%Y")
                self.data[f'driver[{self.i_vod}][changeData]'] = ''
                self.data[f'driver[{self.i_vod}][PersonalDataInfoAdd][Surname]'] = ''
                self.data[f'driver[{self.i_vod}][PersonalDataInfoAdd][Name]'] = ''
                self.data[f'driver[{self.i_vod}][PersonalDataInfoAdd][Patronymic]'] = ''
                self.data[f'driver[{self.i_vod}][PersonDocumentAdd][Serial]'] = ''
                self.data[f'driver[{self.i_vod}][PersonDocumentAdd][Number]'] = ''
                if self.vod.foreign_dl:
                    self.data[f'driver[{self.i_vod}][IsForeignDocument]'] = 'Y'

                self.i_vod += 1
        else:
            self.data['driversNumber'] = "unlimited"
            self.i_vod = 1
            self.data[f'driver[{self.i_vod}][Surname]'] = ""
            self.data[f'driver[{self.i_vod}][Name]'] = ""
            self.data[f'driver[{self.i_vod}][Patronymic]'] = ""
            self.data[f'driver[{self.i_vod}][BirthDate]'] = ""
            self.data[f'driver[{self.i_vod}][Serial]'] = ""
            self.data[f'driver[{self.i_vod}][Number]'] = ""
            self.data[f'driver[{self.i_vod}][DateIssue]'] = ""
            self.data[f'driver[{self.i_vod}][changeData]'] = ''
            self.data[f'driver[{self.i_vod}][PersonalDataInfoAdd][Surname]'] = ''
            self.data[f'driver[{self.i_vod}][PersonalDataInfoAdd][Name]'] = ''
            self.data[f'driver[{self.i_vod}][PersonalDataInfoAdd][Patronymic]'] = ''
            self.data[f'driver[{self.i_vod}][PersonDocumentAdd][Serial]'] = ''
            self.data[f'driver[{self.i_vod}][PersonDocumentAdd][Number]'] = ''

        if int(client_data.OSAGO_count_mouth) == 12:
            self.data["insuranceDate"] = self.date_start
        else:
            self.data["insuranceDate"] = self.date_start
            self.data['isInsuranceDatePeriods'] = 'Y'
            self.data['period[1][startDate]'] = self.date_start
            self.data['period[1][duration]'] = client_data.OSAGO_count_mouth
            self.data['period[1][endDate]'] = datetime.strftime(datetime.strptime(self.date_start, "%d.%m.%Y") + relativedelta(months=int(client_data.OSAGO_count_mouth)), "%d.%m.%Y")


    def __call__(self, *args, **kwargs):
        return urlencode(self.data)