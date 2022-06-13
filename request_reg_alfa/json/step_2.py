import json
from datetime import datetime, timedelta
from urllib.parse import quote, quote_plus
from urllib.parse import urlencode, parse_qs, parse_qsl

from request_reg_alfa.json.get_address import GetAddressJson

class SaveInsurance:
    def __init__(self, client_data, phone_number, calculation_id):
        self.registrationAddress = GetAddressJson(address=client_data.sobstv_pass_address)()
        self.data = {
            "back_url": f"/individuals/auto/eosago/calc/pers/?id={calculation_id}",
            "minLegalAge": "18",

            "insurerEmail": client_data.email_login,
            "insurerPhone": phone_number,

            "insurerSurname": client_data.surname,
            "insurerName": client_data.name,
            "insurerPatronymic": client_data.otchestvo,
            "insurerBirthDate": datetime.strptime(client_data.birthday, "%Y-%m-%d").strftime("%d.%m.%Y"),
            "insurerSerial": client_data.pass_seriya,
            "insurerNumber": client_data.pass_number,

            "insurerAddressRegionState": self.registrationAddress['RegionState'],
            "insurerAddressCity": self.registrationAddress['City'],
            "insurerAddressStreet": self.registrationAddress['Street'],
            "insurerAddressHouseRaw": self.registrationAddress['HouseRaw'],
            "insurerAddressApartment": self.registrationAddress['Apartment'],
            "insurerSnils": "",
            "insurerAddressBuilding": self.registrationAddress['Building'],
            "insurerAddressZip": self.registrationAddress['Zip'],
            "insurerAddressState": self.registrationAddress['State'],
            "insurerAddressRegion": self.registrationAddress['Region'],
            "insurerAddressHouse": self.registrationAddress['HouseRaw'],
            "insurerAddress": self.registrationAddress['Address'],
            "insurerAddressSeparated": self.registrationAddress['Separated'],
            "insurerAddressCountryName": self.registrationAddress['CountryName'],
            "insurerAddressCountryCode": self.registrationAddress['CountryCode'],

            "juicyId": "w.202205132120197e0c0b9c-d302-11ec-8923-22eaf59a3a91.C",

            "ownerSurname": client_data.sobstv_surname,
            "ownerName": client_data.sobstv_name,
            "ownerPatronymic": client_data.sobstv_otchestvo,
            "ownerBirthDate": datetime.strptime(client_data.sobstv_birthday, "%Y-%m-%d").strftime("%d.%m.%Y"),
            "ownerSerial": client_data.sobstv_pass_seriya,
            "ownerNumber": client_data.sobstv_pass_number,
            "ownerSnils": "",

            "agreeLimited": "on",
            "submit_step2": ""
        }

    def __call__(self, *args, **kwargs):
        return urlencode(self.data)