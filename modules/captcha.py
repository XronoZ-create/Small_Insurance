from datetime import datetime, timedelta
import requests
import time

class PoolCaptcha:
    def __init__(self, api_key, len_pool, sitekey, page_url):
        self.api_key = api_key
        self.sitekey = sitekey
        self.len_pool = len_pool
        self.page_url = page_url
        self.captchas = {}  # словарь с решенным капчами: {solve: date}
        self.id_reg_captchas = []  # список с зарегестрированными капчами: [id]

    def reg_captcha(self):
        self.url = "http://api.captcha.guru/in.php?key={api_key}&method=userrecaptcha&googlekey={sitekey}&pageurl={page_url}".format(
            api_key=self.api_key,
            sitekey=self.sitekey,
            page_url=self.page_url
        )
        self.r = requests.get(self.url)
        if self.r.text.split('|')[0] != "OK":
            print(self.r.text, 'Ошибка при регистрации капчи')
        else:
            print('Капча зарегана')
            self.id_reg_captchas.append(self.r.text.split('|')[1])

    def write_solve(self, wait=False, one=False):
        self.url_res = "http://api.captcha.guru/res.php?key={api_key}&action=get&id={id_captcha}"
        while True:
            self.del_id_req_captchas = []
            if len(self.id_reg_captchas) == 0:  # проверка есть ли еще зареганные и не решенные капчи
                break
            for self.id_captcha in self.id_reg_captchas:
                self.r = requests.get(self.url_res.format(api_key=self.api_key, id_captcha=self.id_captcha))
                if self.r.text.split('|')[0] == "OK":
                    print('Капча решена')
                    self.captchas[self.r.text.split('|')[1]] = datetime.now()
                    self.del_id_req_captchas.append(self.id_captcha)
                elif self.r.text == 'CAPCHA_NOT_READY':
                    print(self.r.text, 'Еще не решена')
                else:
                    print(self.r.text, 'Ошибка при решении капчи')
                    self.del_id_req_captchas.append(self.id_captcha)
            for self.id_captcha in self.del_id_req_captchas:
                self.id_reg_captchas.remove(self.id_captcha)

            if wait == False or (len(list(self.captchas.keys())) != 0 and one == True):
                break
            else:
                time.sleep(5)

    def update(self):
        """
        Обновление капч
        :return:
        """
        self.write_solve()
        self.del_captchas = []
        self.len_captchas = len(list(self.captchas.keys()))
        self.len_reg_captchas = len(self.id_reg_captchas)

        if (self.len_reg_captchas + self.len_captchas) < self.len_pool:
            for self._ in range(0, (self.len_pool - (self.len_captchas + self.len_reg_captchas))):
                self.reg_captcha()
        else:
            for self.solve, self.date in self.captchas.items():  # удаление старых капч  регистрация новых
                if (datetime.now() - self.date) > timedelta(seconds=40):
                    self.del_captchas.append(self.solve)
                    self.reg_captcha()
                else:
                    pass
        for self.solve in self.del_captchas:
            self.captchas.pop(self.solve)

    def __getitem__(self, item):
        if len(list(self.captchas.keys())) != 0:
            self.solve = list(self.captchas.keys())[0]
            self.captchas.pop(self.solve)
            return self.solve
        else:
            while True:
                if len(self.id_reg_captchas) == 0:
                    self.reg_captcha()
                self.write_solve(wait=True, one=True)
                if len(list(self.captchas.keys())) != 0:
                    self.solve = list(self.captchas.keys())[0]
                    self.captchas.pop(self.solve)
                    return self.solve
                else:
                    print("Не получилось взять решение капчи. Пробуем еще раз")


class RegCaptchaFailed(Exception):
    pass
class SolveCaptchaFailed(Exception):
    pass