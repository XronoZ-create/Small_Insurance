import json

class SaveVoditelJson:
    """

    """
    def __init__(self, name, middlename, lastname, birthday, series_vod, number_vod, date_vod, stag, foreign_dl, api_key, tr):
        self.json = \
            {
                "api_key": api_key,
                "items": [
                    {
                        "id": "",
                        "status": "ФизЛицо",
                        "document": {
                            "type": "DriverLicense",
                            "typeDL": "DriverLicense",
                            "series": series_vod,
                            "number": number_vod,
                            "dateOfIssue": date_vod,
                            "experienceFrom": stag
                        },
                        "foreign": False,
                        "nationality": "РОССИЯ",
                        "foreignDL": False,
                        "countryDL": "Россия",
                        "documents": {
                            "DriverLicense": {
                                "type": "DriverLicense",
                                "typeDL": "DriverLicense",
                                "series": series_vod,
                                "number": number_vod,
                                "dateOfIssue": date_vod,
                                "experienceFrom": stag
                            }
                        },
                        "lastname": lastname,
                        "name": name,
                        "middlename": middlename,
                        "birthday": birthday
                    }
                ],
                "type": "Водители",
                "Category": "B",
                "method": "saveContractor"
            }
        if foreign_dl == True:
            self.json["items"][0]["document"]["typeDL"] = "ForeignDriverLicense"
            self.json["items"][0]["foreignDL"] = True
            self.json["items"][0]["countryDL"] = "АЗЕРБАЙДЖАН"
            self.json["items"][0]["documents"]["DriverLicense"]["typeDL"] = "ForeignDriverLicense"
        if tr == True:
            self.json["items"][0]["document"]["typeDL"] = "TractorDriverLicense"
            self.json["items"][0]["documents"]["DriverLicense"]["typeDL"] = "TractorDriverLicense"



    def __call__(self, *args, **kwargs):
        if kwargs.get("SavePolicy") != None and kwargs["SavePolicy"] == True:
            return self.json["items"][0]
        else:
            return json.dumps(self.json)