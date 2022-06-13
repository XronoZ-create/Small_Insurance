import json
import datetime
from dateutil.relativedelta import relativedelta

class SavePolicyJson:
    def __init__(self, api_key, insurer, insurer_id,
                 vehicle, vehicle_id,
                 dateStart, OSAGO_count_mouth, owner=None, owner_id=None, drivers=None, drivers_id=None):
        self.json = {
            "api_key": api_key,
            "startLimitTimeAddOsago": int((datetime.datetime.now()-datetime.timedelta(minutes=3)).timestamp() * 1000),
            "insurer": \
                {
                    "id": insurer_id,
                    "status": insurer["status"],
                    "foreign": insurer["foreignDL"],
                    "document": {
                        "type": insurer["document"]["type"],
                        "series": insurer["document"]["series"],
                        "number": insurer["document"]["number"],
                        "dateOfIssue": insurer["document"]["dateOfIssue"],
                        "organizationOfIssue": insurer["document"]["organizationOfIssue"],
                        "experienceFrom": insurer["document"]["experienceFrom"],
                        "name": insurer["document"]["name"],
                        "lastname": insurer["document"]["lastname"],
                        "divisionCode": insurer["document"]["divisionCode"],
                        "country": insurer["document"]["country"]
                    },
                    "defDocument": insurer["defDocument"],
                    "registrationAddress": insurer["registrationAddress"],
                    "postAddress": {
                        "fullAdress": "",
                        "flatType": "кв"
                    },
                    "AgreementForReceiveSMS": insurer["AgreementForReceiveSMS"],
                    "sentSms": False,
                    "checkCode": False,
                    "confirmationCode": "",
                    "sex": "M",
                    "nationality": "Россия",
                    "numberDMS": None,
                    "name": insurer["name"],
                    "lastname": insurer["lastname"],
                    "middlename": insurer["middlename"],
                    "inn": "",
                    "documentType": insurer["documentType"],
                    "email": insurer["email"],
                    "foreignDL": insurer["foreignDL"],
                    "countryDL": insurer["countryDL"],
                    "birthday": insurer["birthday"],
                    "birthPlace": insurer["birthPlace"],
                    "snils": insurer["snils"],
                    "isInsurer": insurer["isInsurer"],
                    "isEntrepreneur": insurer["isEntrepreneur"],
                    "documents": {
                        insurer["documentType"]: {
                            "type": insurer["documents"][insurer["documentType"]]["type"],
                            "series": insurer["documents"][insurer["documentType"]]["series"],
                            "number": insurer["documents"][insurer["documentType"]]["number"],
                            "dateOfIssue": insurer["documents"][insurer["documentType"]]["dateOfIssue"],
                            "organizationOfIssue": insurer["documents"][insurer["documentType"]]["organizationOfIssue"],
                            "experienceFrom": insurer["documents"][insurer["documentType"]]["experienceFrom"],
                            "name": insurer["documents"][insurer["documentType"]]["name"],
                            "lastname": insurer["documents"][insurer["documentType"]]["lastname"],
                            "divisionCode": insurer["documents"][insurer["documentType"]]["divisionCode"],
                            "country": insurer["documents"][insurer["documentType"]]["country"]
                        }
                    },
                    "telephones": {
                        "mobile": insurer["telephones"]["mobile"]
                    },
                    "registrationAddressFlatNumber": insurer["registrationAddressFlatNumber"],
                    "postAddressFlatNumber": insurer["postAddressFlatNumber"],
                    "type": "Страхователь",
                    "Category": "B"
                },

            "vehicle": \
                {
                    "id": vehicle_id,
                    "registration": vehicle["registration"],
                    "inspectionTicket": vehicle["inspectionTicket"],
                    "purposeOfUse": vehicle["purposeOfUse"],
                    "useModification": vehicle["useModification"],
                    "allDocumentTepesRequested": vehicle["allDocumentTepesRequested"],
                    "currentDocumentType": vehicle["currentDocumentType"],
                    "regNumber": vehicle["regNumber"],
                    "noVin": vehicle["noVin"],
                    "nonstandardVin": vehicle["nonstandardVin"],
                    "vin": vehicle["vin"],

                    "chassisNumber": vehicle["chassisNumber"],
                    "bodyNumber": vehicle["bodyNumber"],

                    "mark": vehicle["mark"],
                    "model": vehicle["model"],
                    "markModelText": vehicle["markModelText"],
                    "ModificationID": vehicle["ModificationID"],
                    "modificationStr": vehicle["modificationStr"],
                    "year": vehicle["year"],
                    "category": vehicle["category"],
                    "power": vehicle["power"],
                    "powerKw": vehicle["powerKw"],
                    "maxMass": vehicle["maxMass"],
                    "unladenMass": "",
                    "seatsCount": vehicle["seatsCount"],
                    "documents": vehicle["documents"],
                    "inspectionCard": vehicle["inspectionCard"],
                    "arModification": vehicle["arModification"],
                    "typeBody": vehicle["typeBody"],
                    "typeEngine": vehicle["typeEngine"],
                    "typeKPP": vehicle["typeKPP"],
                    "countryOfRegistration": vehicle["countryOfRegistration"],
                    "GUIDOwner": vehicle["GUIDOwner"],
                    "type": vehicle["type"]
                },

            "dateStart": dateStart,
            "dateEnd": datetime.datetime.strftime(datetime.datetime.strptime(dateStart, "%d.%m.%Y") + datetime.timedelta(days=364), "%d.%m.%Y"),
            "periods": [
                {
                    "period": int(OSAGO_count_mouth),
                    "start": dateStart,
                    "end": datetime.datetime.strftime(datetime.datetime.strptime(dateStart, "%d.%m.%Y")- datetime.timedelta(days=1) + relativedelta(months=int(OSAGO_count_mouth)), "%d.%m.%Y")
                }
            ],
            "isSlingshot": 0,
            "deliveryMethod": "Электронно",
            "carServices": [
                {
                "id": ""
                }
            ],
            "IDAgent": "",
            "ConsultantID": "",
            "code": "osago",
            "method": "savePolicyOsago"
        }

        if owner == None:
            self.json["owner"] = {
                "defDocument": "RussianPassport",
                "id": "",
                "isInsurer": False,
                "status": None
            }
            self.json["ownerIsInsurer"] = True
        else:
            self.json["owner"] = owner
            self.json["owner"]["id"] = owner_id
            self.json["ownerIsInsurer"] = False

        if drivers != None:
            self.drivers = []
            self.i = 0
            for self.driver in drivers:
                self.new_driver = self.driver

                self.new_driver["id"] = drivers_id[self.i]

                self.new_driver["document"]["name"] = ""
                self.new_driver["document"]["lastname"] = ""
                self.new_driver["document"]["divisionCode"] = ""
                self.new_driver["document"]["country"] = "РОССИЯ"

                self.new_driver["documents"]["DriverLicense"]["experienceFrom"] = ""
                self.new_driver["documents"]["DriverLicense"]["organizationOfIssue"] = ""
                self.new_driver["documents"]["DriverLicense"]["name"] = ""
                self.new_driver["documents"]["DriverLicense"]["lastname"] = ""
                self.new_driver["documents"]["DriverLicense"]["divisionCode"] = ""
                self.new_driver["documents"]["DriverLicense"]["country"] = "РОССИЯ"

                self.new_driver["email"] = ""
                self.new_driver["AgreementForReceiveSMS"] = False
                self.new_driver["numberDMS"] = None
                self.new_driver["sex"] = "M"
                self.new_driver["birthPlace"] = ""
                self.new_driver["inn"] = ""
                self.new_driver["snils"] = None
                self.new_driver["isInsurer"] = False
                self.new_driver["isEntrepreneur"] = False

                self.drivers.append(self.new_driver)
                self.i += 1
            self.json["drivers"] = self.drivers
            self.json["multidrive"] = "N"
        else:
            self.json["multidrive"] = "Y"
            self.json["drivers"] = [{
                "id": "",
                "isInsurer": False
            }]

        if vehicle.get("withTrailer") != None:
            self.json["vehicle"]["withTrailer"] = True

        if vehicle.get("vin") != "":
            self.json["vehicle"]["noVin"] = False
        else:
            self.json["vehicle"]["noVin"] = True

    def __call__(self, *args, **kwargs):
        print(json.dumps(self.json, ensure_ascii=False))
        return json.dumps(self.json, ensure_ascii=False).encode('utf-8')
