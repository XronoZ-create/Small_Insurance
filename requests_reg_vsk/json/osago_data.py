import json
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from .get_address import GetAddressSobstvJson, GetAddressStrahJson
from requests_reg_vsk.site_data.category import category_dict
from requests_reg_vsk.site_data.target import target_dict

class OsagoData:
    def __init__(self, client_data, session_id):
        self.data = {
            'drivers': {}
        }
        # -------------------------------------- Водители --------------------------------------------------------------
        self.num_vod = 0
        for self.vod in client_data.voditeli:
            if self.vod.surname == '':
                break
            self.data['drivers'][str(self.num_vod)] = {
                  "isOwner": False,
                  "deleted": False,
                  "birthDate": datetime.strptime(self.vod.birthday, "%Y-%m-%d").strftime("%d.%m.%Y"),
                  "countryId": "643",
                  "firstName": self.vod.name,
                  "lastName": self.vod.surname,
                  "middleName": self.vod.otchestvo,
                  "document": [
                    {
                      "typeId": 20,
                      "number": self.vod.nomer_vu,
                      "serial": self.vod.seriya_vu,
                      "license": "active"
                    }
                  ],
                  "experienceDate": datetime.strptime(self.vod.nachalo_staga, "%Y-%m-%d").strftime("%d.%m.%Y"),
                  "index": self.num_vod
                }
            if self.vod.foreign_dl == True:
                self.data['drivers'][str(self.num_vod)]['document']['typeId'] = 22
            self.num_vod += 1
        # --------------------------------------------------------------------------------------------------------------

        if datetime.strptime(client_data.OSAGO_start, "%Y-%m-%d") - datetime.now() >= timedelta(days=4):
            self.date_start = datetime.strptime(client_data.OSAGO_start, "%Y-%m-%d").strftime("%d.%m.%Y")
        else:
            self.date_start = (datetime.now() + timedelta(days=4)).strftime("%d.%m.%Y")
        self.data.update({
            "commonData": {
                "isLostPolicy": False,
                "isProlongation": False,
                "previousPolicyNumber": "",
                "dateStart": self.date_start,
                "dateEnd": datetime.strftime(datetime.strptime(self.date_start, "%d.%m.%Y") + relativedelta(months=12) - timedelta(days=1), "%d.%m.%Y"),
                "maxAvalibleDateStart": datetime.strftime(datetime.strptime(self.date_start, "%d.%m.%Y") + relativedelta(months=2), "%d.%m.%Y"),
                "minAvalibleDateStart": datetime.strftime(datetime.strptime(self.date_start, "%d.%m.%Y") + relativedelta(months=int(client_data.OSAGO_count_mouth)), "%d.%m.%Y"),
                "periods": [],
                "driversUnlimited": False,
                "showPolicyOwnerDataMismatchNotification": False,
                "isOwnersEquals": False,
                "programs": [],
                "bso": {
                  "zip": "",
                  "address": {
                    "streetKladr": "",
                    "kladr": "",
                    "city": "",
                    "street": "",
                    "noStreet": False,
                    "house": "",
                    "building": "",
                    "apartment": "",
                    "fias": "",
                    "streetFias": ""
                  }
                }
            },
            "policyOwner": {
                "address": GetAddressStrahJson(client_data=client_data)(),
                "document": {
                  "typeId": "12",
                  "serial": client_data.pass_seriya,
                  "number": client_data.pass_number
                },
                "birthDate": datetime.strptime(client_data.birthday, "%Y-%m-%d").strftime("%d.%m.%Y"),
                "firstName": client_data.name,
                "lastName": client_data.surname,
                "middleName": client_data.otchestvo
            },
            "carOwner": {
                "address": GetAddressSobstvJson(client_data=client_data)(),
                "document": {
                  "typeId": 12,
                  "serial": client_data.sobstv_pass_seriya,
                  "number": client_data.sobstv_pass_number
                },
                "birthDate": datetime.strptime(client_data.sobstv_birthday, "%Y-%m-%d").strftime("%d.%m.%Y"),
                "firstName": client_data.sobstv_name,
                "lastName": client_data.sobstv_surname,
                "middleName": client_data.sobstv_otchestvo
            },
            "car": {
                "carIsNotRegistered": False,
                "categoryId": category_dict[client_data.category],
                "document": {
                  "serial": client_data.ctc_ptc_seriya,
                  "number": client_data.ctc_ptc_number,
                  "date": datetime.strptime(client_data.ctc_ptc_vidach, "%Y-%m-%d").strftime("%d.%m.%Y"),
                  "typeId": "31"
                },
                "id": {},
                "hasTrailer": False,
                "isTransCar": False,
                "mark": client_data.mark,
                "markId": client_data.mark_id,
                "model": client_data.model,
                "modelId": client_data.model_id,
                "power": client_data.powers,
                "powerInKwt": 0,
                "purposeId": target_dict[client_data.target],
                "registrationCountryId": 1,
                "yearIssue": client_data.year,
                "indemnity": 1
            },
            "sessid": session_id
        })

        if client_data.voditeli[0].surname == "":
            self.data['commonData']['driversUnlimited'] = True

        if client_data.strah_type_document == 'RussianPassport':
            self.data['policyOwner']['document']['typeId'] = "12"
        elif client_data.strah_type_document == 'Residence':
            self.data['policyOwner']['document']['typeId'] = "9"

        if client_data.sobstv_type_document == 'RussianPassport':
            self.data['carOwner']['document']['typeId'] = 12
        elif client_data.sobstv_type_document == 'Residence':
            self.data['carOwner']['document']['typeId'] = 9

        if client_data.type_document == 'passport':
            self.data['car']['document']['typeId'] = "30"
        elif client_data.type_document == 'certificate':
            self.data['car']['document']['typeId'] = "31"
        elif client_data.type_document == 'ePassport':
            self.data['car']['document']['typeId'] = "41"
        elif client_data.type_document == 'tractorPassport':
            self.data['car']['document']['typeId'] = "32"

        if client_data.ctc_ptc_vin != "":
            self.data['car']['id'] = {"vin": client_data.ctc_ptc_vin}
        elif client_data.ctc_ptc_nomer_shassi != "":
            self.data['car']['id'] = {"chassisNumber": client_data.ctc_ptc_nomer_shassi}
        elif client_data.ctc_ptc_nomer_cusov != "":
            self.data['car']['id'] = {"bodyNumber": client_data.ctc_ptc_nomer_cusov}

        if client_data.ctc_ptc_reg_znak != "":
            self.data['car']['id']['licensePlate'] = client_data.ctc_ptc_reg_znak
        else:
            self.data['car']['carIsNotRegistered'] = True

        if client_data.pricep != "":
            self.data['car']['hasTrailer'] = True
        else:
            self.data['car']['hasTrailer'] = False

        if category_dict[client_data.category] == 4:
            self.data['car']['passengersCount'] = client_data.count_pass_mest
        elif category_dict[client_data.category] == 3:
            self.data['car']['maxWeight'] = client_data.max_mass

        if client_data.mark_name_other != "":
            self.data['car']['mark'] = client_data.mark_name_other
        if client_data.model_name_other != "":
            self.data['car']['model'] = client_data.model_name_other


    def __call__(self, *args, **kwargs):
        return json.dumps(self.data)