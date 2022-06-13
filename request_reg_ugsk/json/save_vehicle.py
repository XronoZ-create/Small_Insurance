import json
from request_reg_ugsk.json.get_modification import GetModificationJson

class SaveVehicleJson:
    """
        "purposeOfUse": ["Личная", "УчебнаяЕзда", "ПассажирскиеПеревозки", "Такси", "СдачаВАренду", "ДорожныеИСпециальныеТС", "ЭкстренныеИКоммСлужбы", "ОпасныйГруз", "Прочее"],
        "currentDocumentType": ["passport", "certificate", "ePassport"]
    """
    def __init__(self, target, document_type, reg_number,
                 year, mark, model, category, proxies, ptc_ctc_series=None, ptc_ctc_number=None, ptc_ctc_date=None, eptc_number=None, eptc_date=None,
                 diagn_card_number="", diagn_card_date="", power=None, modification=None, type_body=None, type_engine=None, type_kpp=None,
                 chassis_number="", body_number="", max_mass="", seats_count="",
                 with_trailer="",
                 vin="", other_mark=""):

        self.proxies = proxies

        if mark == "Другая марка":
            self.mark_model_text = other_mark
        else:
            self.mark_model_text = f"{mark} {model}"
        self.mark = mark
        self.model = model
        self.modification = modification
        self.json = \
            {
                "id": "",
                "registration": "russia",
                "seatsCount": seats_count,
                "inspectionTicket": {
                    "series": "",
                    "number": "",
                    "Date": ""
                },
                "purposeOfUse": target,
                "useModification": True,
                "allDocumentTepesRequested": {

                },
                "currentDocumentType": document_type,
                "regNumber": reg_number,
                "nonstandardVin": False,

                "vin": vin,

                "mark": mark,
                "maxMass": max_mass,
                "model": model,
                "markModelText": self.mark_model_text,
                "ModificationID": "000000000000000000000000000000",
                "modificationStr": "",
                "year": str(year),
                "category": category,
                "inspectionCard": {
                    "number": diagn_card_number,
                    "term": diagn_card_date
                },
                "arModification": {

                },
                "bodyNumber": body_number,
                "chassisNumber": chassis_number,
                "typeBody": type_body,
                "typeEngine": type_engine,
                "typeKPP": type_kpp,
                "countryOfRegistration": "РОССИЯ",
                "GUIDOwner": "00000000-0000-0000-0000-000000000000",
                "type": "Транспортное средство",
                "method": "saveVehicle"
            }
        if document_type == "passport" or document_type == "certificate":
            self.json["documents"] = {
                document_type: {
                    "series": ptc_ctc_series,
                    "number": ptc_ctc_number,
                    "dateOfIssue": ptc_ctc_date
                }
            }
        elif document_type == "tractorPassport":
            self.json["documents"] = {
                document_type: {
                    "series": ptc_ctc_series,
                    "number": ptc_ctc_number,
                    "dateOfIssue": ptc_ctc_date
                },
                "passport": {
                    "series": "",
                    "number": "",
                    "dateOfIssue": ""
                }
            }
        elif document_type == "ePassport":
            self.json["documents"] = {
                 document_type: {
                     "series": "",
                     "number": eptc_number,
                     "dateOfIssue": eptc_date
                 },
                "passport": {
                    "series": "",
                    "number": "",
                    "dateOfIssue": ""
                }
             }

        if power != None:
            self.json["power"] = power.replace(',', '.')
            self.json["powerKw"] = round(float(power.replace(',', '.'))*0.73549875, 2)

        if with_trailer != "":
            self.json["withTrailer"] = True

        if vin != "":
            self.json["noVin"] = False
        else:
            self.json["noVin"] = True

    def __call__(self, *args, **kwargs):
        if self.modification != None:
            self.mod = GetModificationJson(mark=self.mark, model=self.model, modification=self.modification, proxies=self.proxies)
            self.json["arModification"] = self.mod()
            self.json["typeBody"] = self.mod()["TypeBody"]
            self.json["typeEngine"] = self.mod()["TypeEngine"]
            self.json["typeKPP"] = self.mod()["TypeKPP"]
            self.json["ModificationID"] = self.mod()["id"]
            self.json["modificationStr"] = self.mod()["modificationname"]
            self.json["power"] = self.mod()["Power"]
            self.json["powerKw"] = round(float(self.mod()["Power"]) * 0.73549875, 2)

        if kwargs.get("SavePolicy") != None and kwargs["SavePolicy"] == True:
            return self.json
        else:
            return json.dumps(self.json)