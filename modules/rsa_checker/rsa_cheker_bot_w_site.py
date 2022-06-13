import requests
import time
from datetime import datetime, timedelta
import urllib3
urllib3.disable_warnings()
from modules.captcha import PoolCaptcha
from contextlib import suppress
from config import Config

def check_contract_id_token(url_token, contract_id, comp_id, json_table):
    headers = {'Host': 'e-garant.autoins.ru',
               'Cookie': f'contract_id_token={contract_id}',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
               'Accept': 'application/json, text/plain, */*',
               'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
               'Accept-Encoding': 'gzip, deflate',
               'Origin': 'https://e-garant.autoins.ru',
               'Referer': f'https://e-garant.autoins.ru/companies/{url_token}',
               'Sec-Fetch-Dest': 'empty',
               'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Site': 'same-origin',
               'Content-Length': '0',
               'Te': 'trailers',
               'Connection': 'close'}

    start_while_true = datetime.now()
    while True:
        if (datetime.now() - start_while_true) > timedelta(minutes=3):
            raise LagRca
        elif json_table.active == False:
            raise StopFind

        try:
            resp = requests.post(
                f'https://e-garant.autoins.ru/api/v1/egarant-sk-spreader/ui/{url_token}/insuranceCompanies/{comp_id}/reserve',
                verify=False,
                headers=headers,
                data={})
            if type(resp.json()) is dict:
                if resp.json()['result'] == True:
                    return True
            else:
                print(f'{resp.json()[0]["message"]}')
                return False
        except KeyError:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Не получилось забронировать')

def start_find(input_url, json_table, telephone=None):
    json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Поиск лимитов')
    print(f'Начинаю работу: входная ссылка {input_url}')
    start_time = datetime.now()

    url_token = input_url.split('/')[-1]
    if len(url_token) == 0:
        url_token = input_url.split('/')[-2]

    api_key = Config.guru_captcha_api_key
    site_key = '6LdrVtEUAAAAAM17q4w4vDDWQauUXqNlrk0QAQIe'
    token_url = input_url
    pool_captcha = PoolCaptcha(api_key=api_key, sitekey=site_key, page_url=token_url, len_pool=10)

    check_update = 0
    while True:
        # --------------------------------------------Проверка статуса--------------------------------------------------
        if check_update == 10:
            check_update = 0  # на каждый 10 раз
            if json_table.active == False:
                raise StopFind
        else:
            check_update += 1
        # --------------------------------------------Основная часть----------------------------------------------------
        check_insurances = json_table.data.strah_comp
        pool_captcha.update()
        print(f'Проверка свободных контрактов...')
        token = pool_captcha[0]
        session = requests.Session()
        headers = {'Host': 'e-garant.autoins.ru',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
                   'Accept': 'application/json, text/plain, */*',
                   'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Accept-Encoding': 'gzip, deflate',
                   'Captchatoken': token,
                   'Referer': f'https://e-garant.autoins.ru/companies/{url_token}',
                   'Sec-Fetch-Dest': 'empty',
                   'Sec-Fetch-Mode': 'cors',
                   'Sec-Fetch-Site': 'same-origin',
                   'Te': 'trailers',
                   'Connection': 'close'}
        session.headers = headers
        session.verify = headers

        try:
            resp = requests.get(f'https://e-garant.autoins.ru/api/v2/egarant-sk-spreader/ui/{url_token}/insuranceCompanies', verify=False, headers=headers)
        except Exception as err:
            print(err)
            continue

        if resp.status_code == 200:
            contract_id_token = resp.cookies['contract_id_token']
            result = resp.json()
            for item in result:
                comp_name = item["searchName"]
                if comp_name in check_insurances:
                    comp_id = item['id']
                    if item["contractsLeft"] > 0:
                        print(f'СК: {comp_name}. Найдено свободных контрактов: {item["contractsLeft"]}')

                        headers = {'Host': 'e-garant.autoins.ru',
                                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
                                   'Accept': 'application/json, text/plain, */*',
                                   'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                                   'Accept-Encoding': 'gzip, deflate',
                                   'Referer': f'https://e-garant.autoins.ru/companies/{url_token}',
                                   'Sec-Fetch-Dest': 'empty',
                                   'Sec-Fetch-Mode': 'cors',
                                   'Sec-Fetch-Site': 'same-origin',
                                   'Te': 'trailers',
                                   'Connection': 'close'}


                        resp = requests.get(f'https://e-garant.autoins.ru/api/v2/egarant-sk-spreader/ui/{url_token}/hasInsCompany2Chosen',  verify=False, headers=headers)

                        if resp.status_code == 200:
                            if resp.json()['isChosen'] == False:
                                if check_contract_id_token(url_token, contract_id_token, comp_id, json_table=json_table):
                                    print(f'Контракт успешно зарезервирован. СК: {comp_name}')
                                    if telephone == None:
                                        json_table.stop_bot()  # если запущен режим Ловилки
                                    json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Контракт успешно зарезервирован. СК: {comp_name}')
                                    json_table.set_value("url_rca", input_url)
                                    return input_url
                            else:
                                print(f'Для ссылки {input_url} контракт зарегистрирован ранее')
                                json_table.stop_bot()
                                json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Для ссылки {input_url} контракт зарегистрирован ранее')
                                return
                    else:
                        json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} СК: {comp_name} - свободных контрактов нет.')
                        print(f'СК: {comp_name} - свободных контрактов нет.')
        else:
            with suppress(Exception):
                print(f'{resp.json()[0]["message"]}')
            # json_table.stop_bot()
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Возможно требуется обновить входную ссылку.')
            print(f'Возможно требуется обновить входную ссылку.')

        if telephone != None:
            telephone.check_lifetime()
        elif (datetime.now() - start_time) > timedelta(minutes=60):
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Прошло 60 минут после запуска. Остановлен')
            json_table.stop_bot()
            raise StopFind
        # time.sleep(0.5)



class AlreadyRegFailed(Exception):
    pass
class NeededUpdateUrlRca(Exception):
    pass
class StopFind(Exception):
    pass
class LagRca(Exception):
    pass