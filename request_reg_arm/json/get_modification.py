import json
import requests

class GetModificationJson:
    def __init__(self, mark, model, modification, proxies=None):
        self.modification_name = modification
        self.json = \
            {
                "markId": mark,
                "modelId": model,
                "useModification": True,
                "method": "GetMarkModelModifications"
            }
        self.headers = {
            'Host': 'b2c.armeec.ru', 'Connection': 'keep-alive', 'Content-Length': '974',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"', 'Origin': 'https://b2c.armeec.ru',
            'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty'
        }

        self.session = requests.Session()
        if proxies != None:
            self.session.proxies = proxies
        self.r = self.session.post(
            "https://b2c.armeec.ru/local/tools/webslon/elpolis.api/",
            data=json.dumps(self.json),
            headers=self.headers
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