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
        self.json = {
            "RegionState": self.r_json["suggestions"][0]["data"]["region_with_type"],
            "City": self.r_json["suggestions"][0]["data"]["city_with_type"],
            "Settlement": self.r_json["suggestions"][0]["data"]["settlement_with_type"],
            "Street": self.r_json["suggestions"][0]["data"]["street_with_type"],
            "HouseRaw": '%s %s' % (self.r_json["suggestions"][0]["data"]["house_type"], self.r_json["suggestions"][0]["data"]["house"]),
            "Flat": self.r_json["suggestions"][0]["data"]["flat"],
            "Apartment": '',
            "Building": "",
            "Zip": str(self.r_json["suggestions"][0]["data"]["postal_code"] or ''),
            "State": self.r_json["suggestions"][0]["data"]["region_with_type"],
            "Region": "",
            "CountryName": self.r_json["suggestions"][0]["data"]["country"],
            "House": self.r_json["suggestions"][0]["data"]["house"],
            "CountryCode": "643",
            "Address": self.r_json["suggestions"][0]["unrestricted_value"].replace(',', ''),
            "Separated": "0"
        }
        return self.json