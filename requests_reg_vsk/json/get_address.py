import json
import requests
from config import Config
from requests_reg_vsk.site_data.country import country_alfa

class GetAddressStrahJson:
    def __init__(self, client_data):
        self.client_data = client_data

    def __call__(self, *args, **kwargs):
        self.headers = {
            'accept': 'application/json, text/plain, */*', 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'origin': 'https://eosago21-vek.ru/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        self.session = requests.Session()
        if Config.proxies != None:
            self.proxies = Config.proxies
            self.session.proxies = self.proxies

        # ---------------------------------- Город ---------------------------------------------------------------------
        self.params = {
            "q": self.client_data.city_strah.split(',')[0]
        }
        self.r = self.session.get("https://shop.vsk.ru/osago/ajax/kladr/search/", params=self.params, headers=self.headers)
        self.r_json = self.r.json()
        print(self.r_json)
        self.dict_address_city = {}
        for self.one_address in self.r_json:
            self.dict_address_city[self.one_address['value']] = {'id': self.one_address['id'], 'fias': self.one_address['fias']}
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------- Улица ----------------------------------------------------------------------
        if self.client_data.street_strah != '':
            self.params = {
                "q": self.client_data.street_strah.split(',')[0],
                "city": self.dict_address_city[self.client_data.city_strah]['fias']
            }
            self.r = self.session.get("https://shop.vsk.ru/osago/ajax/kladr/search/", params=self.params, headers=self.headers)
            self.r_json = self.r.json()
            print(self.r_json)
            self.dict_address_street = {}
            for self.one_address in self.r_json:
                self.dict_address_street[self.one_address['value']] = {'id': self.one_address['id'], 'fias': self.one_address['fias']}
        # --------------------------------------------------------------------------------------------------------------

        self.json = \
            {
                "kladr": self.dict_address_city[self.client_data.city_strah]['id'],
                "city": self.client_data.city_strah,
                "postalCode": self.client_data.postal_code_strah,
                "countryId": 643,
                "fias": self.dict_address_city[self.client_data.city_strah]['fias'],
            }
        if self.client_data.street_strah == '':
            self.json['noStreet'] = True
        else:
            self.json['noStreet'] = False
            self.json["street"] = self.client_data.street_strah
            self.json["streetKladr"] = self.dict_address_street[self.client_data.street_strah]['id']
            self.json["streetFias"] = self.dict_address_street[self.client_data.street_strah]['fias']

        if self.client_data.apartment_strah != '':
            self.json['apartment'] = self.client_data.apartment_strah
        if self.client_data.house_strah != '':
            self.json['house'] = self.client_data.house_strah
        if self.client_data.building_strah != '':
            self.json['building'] = self.client_data.building_strah

        return self.json

class GetAddressSobstvJson:
    def __init__(self, client_data):
        self.client_data = client_data

    def __call__(self, *args, **kwargs):
        self.headers = {
            'accept': 'application/json, text/plain, */*', 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'origin': 'https://eosago21-vek.ru/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        self.session = requests.Session()
        if Config.proxies != None:
            self.proxies = Config.proxies
            self.session.proxies = self.proxies

        # ---------------------------------- Город ---------------------------------------------------------------------
        self.params = {
            "q": self.client_data.city_sobstv.split(',')[0]
        }
        self.r = self.session.get("https://shop.vsk.ru/osago/ajax/kladr/search/", params=self.params, headers=self.headers)
        self.r_json = self.r.json()
        print(self.r_json)
        self.dict_address_city = {}
        for self.one_address in self.r_json:
            self.dict_address_city[self.one_address['value']] = {'id': self.one_address['id'], 'fias': self.one_address['fias']}
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------- Улица ----------------------------------------------------------------------
        if self.client_data.street_sobstv != '':
            self.params = {
                "q": self.client_data.street_sobstv.split(',')[0],
                "city": self.dict_address_city[self.client_data.city_sobstv]['fias']
            }
            self.r = self.session.get("https://shop.vsk.ru/osago/ajax/kladr/search/", params=self.params, headers=self.headers)
            self.r_json = self.r.json()
            print(self.r_json)
            self.dict_address_street = {}
            for self.one_address in self.r_json:
                self.dict_address_street[self.one_address['value']] = {'id': self.one_address['id'], 'fias': self.one_address['fias']}
        # --------------------------------------------------------------------------------------------------------------

        self.json = \
            {
                "kladr": self.dict_address_city[self.client_data.city_sobstv]['id'],
                "city": self.client_data.city_sobstv,
                "postalCode": self.client_data.postal_code_sobstv,
                "countryId": 643,
                "fias": self.dict_address_city[self.client_data.city_sobstv]['fias'],
            }
        if self.client_data.street_sobstv == '':
            self.json['noStreet'] = True
        else:
            self.json['noStreet'] = False
            self.json["street"] = self.client_data.street_sobstv
            self.json["streetKladr"] = self.dict_address_street[self.client_data.street_sobstv]['id']
            self.json["streetFias"] = self.dict_address_street[self.client_data.street_sobstv]['fias']

        if self.client_data.apartment_sobstv != '':
            self.json['apartment'] = self.client_data.apartment_sobstv
        if self.client_data.house_sobstv != '':
            self.json['house'] = self.client_data.house_sobstv
        if self.client_data.building_sobstv != '':
            self.json['building'] = self.client_data.building_sobstv

        return self.json


# a = Ge(address="Респ Башкортостан, г Давлеканово, ул Ферапонтова, д 38 к 1")
# print(a())