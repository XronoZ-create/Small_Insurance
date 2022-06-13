import json
from request_reg_21.json.get_address import GetAddressJson

class SaveStrahJson:
    def __init__(self, document, name, lastname, middlename, email, birthday, telephone, address, api_key):

        self.registrationAddress = GetAddressJson(address=address)

        self.json = \
            {
                "api_key": api_key,
                "id": "00000000-0000-0000-0000-000000000000",
                "status": "ФизЛицо",
                "foreign": False,
                "document": {
                    "type": document["type"],
                    "series": str(document["series"]),
                    "number": str(document["number"]),
                    "dateOfIssue": "",
                    "organizationOfIssue": "",
                    "experienceFrom": "",
                    "name": "",
                    "lastname": "",
                    "divisionCode": "",
                    "country": "РОССИЯ"
                },
                "defDocument": document["type"],
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
                "documentType": document["type"],
                "email": str(email),
                "foreignDL": False,
                "countryDL": "",
                "birthday": str(birthday),
                "birthPlace": "",
                "snils": None,
                "isInsurer": True,
                "isEntrepreneur": False,
                "documents": {
                    document["type"]: {
                        "type": document["type"],
                        "series": str(document["series"]),
                        "number": str(document["number"]),
                        "dateOfIssue": "",
                        "organizationOfIssue": "",
                        "experienceFrom": "",
                        "name": "",
                        "lastname": "",
                        "divisionCode": "",
                        "country": "РОССИЯ"
                    }
                },
                "telephones": {
                    "mobile": str(telephone)
                },
                "registrationAddressFlatNumber": self.registrationAddress()["flat_number"],
                "postAddressFlatNumber": None,
                "type": "Страхователь",
                "method": "saveContractor"
            }
        print(self.json)

    def __call__(self, *args, **kwargs):
        if kwargs.get("SavePolicy") != None and kwargs["SavePolicy"] == True:
            self.wo_api = dict(self.json)
            self.wo_api.pop("api_key")
            return self.wo_api
        else:
            return json.dumps(self.json, ensure_ascii=False).encode('utf-8')

class SaveSobstvJson:
    def __init__(self, document, name, lastname, middlename, birthday, address, api_key):

        self.registrationAddress = GetAddressJson(address=address)
        self.json = \
            {
                "api_key": api_key,
                "id": "",
                "status": "ФизЛицо",
                "foreign": False,
                "document": {
                    "type": document["type"],
                    "series": str(document["series"]),
                    "number": str(document["number"]),
                },
                "defDocument": document["type"],
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
                "documentType": document["type"],
                "birthday": str(birthday),
                "documents": {
                    document["type"]: {
                        "type": document["type"],
                        "series": str(document["series"]),
                        "number": str(document["number"])
                    }
                },
                "registrationAddressFlatNumber": self.registrationAddress()["flat_number"],
                "postAddressFlatNumber": None,
                "type": "Собственник",
                "method": "saveContractor"
            }

    def __call__(self, *args, **kwargs):
        if kwargs.get("SavePolicy") != None and kwargs["SavePolicy"] == True:
            self.wo_api = dict(self.json)
            self.wo_api.pop("api_key")
            return self.wo_api
        else:
            return json.dumps(self.json, ensure_ascii=False).encode('utf-8')