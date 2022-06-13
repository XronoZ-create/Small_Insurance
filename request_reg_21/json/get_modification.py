import json
import requests

class GetModificationJson:
    def __init__(self, mark, model, modification, proxies=None):
        self.modification_name = modification
        self.url_site = 'https://eosago21-vek.ru/personal/?register=yes&backurl=%2Fpersonal%2Findex.php'
        self.headers_site = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9', 'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'eosago21-vek.ru', 'Referer': 'https://eosago21-vek.ru/personal/',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"', 'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
        self.headers_check = {
            'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9', 'Connection': 'keep-alive', 'Content-Length': '1270',
            'Content-Type': 'application/json',
            'Host': 'eosago21-vek.ru', 'Origin': 'https://eosago21-vek.ru',
            'Referer': 'https://eosago21-vek.ru/osago/policy/',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }

        self.session = requests.Session()
        if proxies != None:
            self.session.proxies = proxies
        self.r = self.session.get(self.url_site, headers=self.headers_site)
        self.api_key = self.r.text.split("window.api_key = ")[1].split(";")[0].replace("'", "")

        self.json = \
            {
                "api_key": self.api_key,
                "markId": mark,
                "modelId": model,
                "useModification": True,
                "method": "GetMarkModelModifications"
            }
        self.r = self.session.post(
            "https://eosago21-vek.ru/local/tools/webslon/elpolis.api/",
            data=json.dumps(self.json),
            headers=self.headers_check
        )
        self.r_json = self.r.json()
        self.modification_json = {}
        self.i = 1
        for self.one_modification in self.r_json["data"]:
            if self.one_modification["modificationname"] == self.modification_name:
                self.modification_json = self.one_modification
                self.modification_json["modificationname"] = f"{self.i}) {self.modification_json['modificationname']}"
                break
            self.i += 1

    def __call__(self, *args, **kwargs):
        return self.modification_json