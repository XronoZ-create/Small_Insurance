import json
import requests
from config import Config

class GetAddressJson:
    def __init__(self, address):
        self.params = {
            "count": 7,
            "query": address,
            "token": "2c580fc9d73e7813ece6cbb9462efde2decdeb86",
            "type": "ADDRESS"
        }

    def __call__(self, *args, **kwargs):
        self.headers = {
            'accept': 'application/json, text/plain, */*', 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'origin': 'https://eosago21-vek.ru/',
            'referer': 'https://eosago21-vek.ru/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        self.session = requests.Session()
        if Config.proxies != None:
            self.proxies = Config.proxies
            self.session.proxies = self.proxies

        self.r = self.session.get("https://dadata.ru/api/v2/suggest/address/", params=self.params, headers=self.headers)
        self.r_json = self.r.json()
        print(self.r_json)
        self.json = \
            {
                "buildingId": self.r_json["suggestions"][0]["data"]["house_kladr_id"],
                "fullAdress": self.r_json["suggestions"][0]["value"],
                "flatType": "кв",
                "index": self.r_json["suggestions"][0]["data"]["postal_code"],
                "region": self.r_json["suggestions"][0]["data"]["region"],
                "regionId": self.r_json["suggestions"][0]["data"]["region_kladr_id"],
                "city": self.r_json["suggestions"][0]["data"]["city"],
                "cityId": self.r_json["suggestions"][0]["data"]["city_kladr_id"],
                "street_fias_id": self.r_json["suggestions"][0]["data"]["street_fias_id"],
                "street": self.r_json["suggestions"][0]["data"]["street"],
                "streetId": self.r_json["suggestions"][0]["data"]["street_kladr_id"],
                "fias_id": self.r_json["suggestions"][0]["data"]["fias_id"],
                "kladr_id": self.r_json["suggestions"][0]["data"]["kladr_id"],
                "okato": self.r_json["suggestions"][0]["data"]["okato"],
                "flat_number": self.r_json["suggestions"][0]["data"]["flat"],
                "home": self.r_json["suggestions"][0]["data"]["house"],
                "house": self.r_json["suggestions"][0]["data"]["house"],
            }
        if self.r_json["suggestions"][0]["data"]["area"] != None:
            self.json["district"] = self.r_json["suggestions"][0]["data"]["area"]
            self.json["districtId"] = self.r_json["suggestions"][0]["data"]["area_kladr_id"]
        if self.r_json["suggestions"][0]["data"]["settlement"] != None:
            self.json["settlement"] = self.r_json["suggestions"][0]["data"]["settlement"]
            self.json["settlementId"] = self.r_json["suggestions"][0]["data"]["settlement_kladr_id"]
        if self.r_json["suggestions"][0]["data"]["block"] != None:
            self.json["block"] = self.r_json["suggestions"][0]["data"]["block"]
            self.json["home"] = "%s %s %s" % (self.r_json["suggestions"][0]["data"]["house"], self.r_json["suggestions"][0]["data"]["block_type"], self.r_json["suggestions"][0]["data"]["block"])
        return self.json