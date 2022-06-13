import json
from request_reg_arm.json.get_address import GetAddressJson

class SaveStrahJson:
    def __init__(self, pass_series, pass_number, name, lastname, middlename, email, birthday, telephone, address):

        self.registrationAddress = GetAddressJson(address=address)
        self.json = \
            {
                "id": "00000000-0000-0000-0000-000000000000",
                "status": "ФизЛицо",
                "foreign": False,
                "document": {
                    "type": "RussianPassport",
                    "series": str(pass_series),
                    "number": str(pass_number),
                    "dateOfIssue": "02.11.2020",
                    "organizationOfIssue": "Отделом УФМС",
                    "experienceFrom": "",
                    "name": "",
                    "lastname": "",
                    "divisionCode": "510006",
                    "country": "РОССИЯ"
                },
                "defDocument": "RussianPassport",
                "registrationAddress": self.registrationAddress(),
                "postAddress": {
                    "fullAdress": "",
                    "flatType": "кв"
                },
                "AgreementForReceiveSMS": False,
                "sentSms": False,
                "checkCode": False,
                "confirmationCode": "",
                "sex": "M",
                "nationality": "Россия",
                "numberDMS": False,
                "name": str(name),
                "lastname": str(lastname),
                "middlename": str(middlename),
                "inn": "",
                "documentType": "RussianPassport",
                "email": str(email),
                "foreignDL": False,
                "countryDL": "",
                "birthday": str(birthday),
                "birthPlace": "",
                "snils": None,
                "isInsurer": True,
                "isEntrepreneur": False,
                "documents": {
                    "RussianPassport": {
                        "type": "RussianPassport",
                        "series": str(pass_series),
                        "number": str(pass_number),
                        "dateOfIssue": "",
                        "organizationOfIssue": "Отделом УФМС",
                        "experienceFrom": "",
                        "name": "",
                        "lastname": "",
                        "divisionCode": "510006",
                        "country": "РОССИЯ"
                    }
                },
                "telephones": {
                    "mobile": str(telephone)
                },
                "registrationAddressFlatNumber": self.registrationAddress()["flat_number"],
                "postAddressFlatNumber": None,
                "type": "Страхователь",
                "method": "saveContractor",
                "files": [{'name': "billy-gachi.gif", 'fileId': "20211213_001213_3443.gif"}],
                "loadedDocuments": {"RussianPassport": {"type": "RussianPassport", "series": f"{pass_series}", "number": f"{pass_number}",
                                                        "dateOfIssue": "", "organizationOfIssue": "",
                                                        "experienceFrom": "", "name": "", "lastname": "",
                                                        "divisionCode": "", "country": "РОССИЯ"}}
            }

    def __call__(self, *args, **kwargs):
        if kwargs.get("SavePolicy") != None and kwargs["SavePolicy"] == True:
            return self.json
        else:
            return json.dumps(self.json, ensure_ascii=False).encode('utf-8')

class SaveSobstvJson:
    def __init__(self, pass_series, pass_number, name, lastname, middlename, birthday, address):

        self.registrationAddress = GetAddressJson(address=address)
        self.json = \
            {
                "id": "",
                "status": "ФизЛицо",
                "foreign": False,
                "document": {
                    "type": "RussianPassport",
                    "series": str(pass_series),
                    "number": str(pass_number)
                },
                "defDocument": "RussianPassport",
                "registrationAddress": self.registrationAddress(),
                "postAddress": {
                    "flat_number": None,
                    "fullAdress": "",
                    "flatType": "кв"
                },
                "AgreementForReceiveSMS": False,
                "sentSms": False,
                "checkCode": False,
                "confirmationCode": "",
                "nationality": "РОССИЯ",
                "name": str(name),
                "lastname": str(lastname),
                "middlename": str(middlename),
                "documentType": "RussianPassport",
                "birthday": str(birthday),
                "documents": {
                    "RussianPassport": {
                        "type": "RussianPassport",
                        "series": str(pass_series),
                        "number": str(pass_number)
                    }
                },
                "registrationAddressFlatNumber": self.registrationAddress()["flat_number"],
                "postAddressFlatNumber": None,
                "type": "Собственник",
                "method": "saveContractor"
            }

    def __call__(self, *args, **kwargs):
        if kwargs.get("SavePolicy") != None and kwargs["SavePolicy"] == True:
            return self.json
        else:
            return json.dumps(self.json, ensure_ascii=False).encode('utf-8')