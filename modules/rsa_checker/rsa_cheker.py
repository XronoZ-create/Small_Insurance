import requests
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk
import os
import urllib3
urllib3.disable_warnings()
from pandastable import Table
import colorama
from colorama import Fore, Style
colorama.init()
from captcha import PoolCaptcha
from contextlib import suppress

def out_yellow(text):
    #print("\033[33m{}\033[0m".format(text))
    print(Fore.YELLOW + text)
    print(Style.RESET_ALL)

def out_red(text):
    #print("\033[31m{}\033[0m".format(text))
    print(Fore.RED + text)
    print(Style.RESET_ALL)

def out_green(text):
    #print("\033[32m{}\033[0m".format(text))
    print(Fore.GREEN + text)
    print(Style.RESET_ALL)

def write_log(type_mess, mess):
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    log_folder_path = 'log'
    str_type = "[INFO]"
    if type_mess == 1:
        str_type = "[INFO]"
        print('%s %s %s' % (now, str_type, mess))
    elif type_mess == 2:
        str_type = "[WARN]"
        out_yellow('%s %s %s' % (now, str_type, mess))
    elif type_mess == 3:
        str_type = "[ERROR]"
        out_red('%s %s %s' % (now, str_type, mess))
    elif type_mess == 4:
        str_type = "[GOOD]"
        out_green('%s %s %s' % (now, str_type, mess))


def get_recapcha_v2_token(api_key, site_key, url):
    s = requests.Session()
    captha_url = 'api.captcha.guru'
    #captha_url = '192.168.0.105'


    get_url = f'http://{captha_url}/in.php?key={api_key}' \
              f'&method=userrecaptcha' \
              f'&googlekey={site_key}' \
              f'&pageurl={url}'

    captcha = s.get(get_url, verify=False)
    captcha_id = captcha.text.split('|')[1]

    while True:
        time.sleep(1)
        recaptcha_answer = s.get("http://{}/res.php?key={}&action=get&id={}".format(captha_url, api_key, captcha_id), verify=False).text
        #print("solving ref captcha...")
        if recaptcha_answer == 'CAPCHA_NOT_READY':
            continue
        if 'ERROR' not in recaptcha_answer:
            break
    recaptcha_answer = recaptcha_answer.split('|')[1]
    return recaptcha_answer

def save_key():
    new_key = entry_key.get()
    with open('api_key.txt', 'w') as f_key:
        f_key.write(new_key)


def check_contract_id_token(url_token, contract_id, comp_id):
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

    resp = requests.post(
        f'https://e-garant.autoins.ru/api/v1/egarant-sk-spreader/ui/{url_token}/insuranceCompanies/{comp_id}/reserve',
        verify=False,
        headers=headers,
        data={})
    if type(resp.json()) is dict:
        if resp.json()['result'] == True:
            return True
    else:
        write_log(2, f'{resp.json()[0]["message"]}')
        return False


def start():
    check_list = []

    for check in checks:
        if check.var.get() == True:
            check_list.append(check.title)



    #input_url = 'https://e-garant.autoins.ru/agreement/2aa61f08-efd1-3f0a-b718-4a59644cf671'
    input_url = entry.get()
    if len(input_url) == 0:
        write_log(2, 'Не задана ссылка для поиска.')
        return
    #input_url = 'https://e-garant.autoins.ru/agreement/2aa61f08-efd1-3f0a-b718-4a59644cf671'

    if len(check_list) == 0:
        write_log(2, 'Не выбрана ни одна СК.')
        return


    write_log(4, f'Начинаю работу: входная ссылка {input_url}')
    start_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    url_token = input_url.split('/')[-1]
    if len(url_token) == 0:
        url_token = input_url.split('/')[-2]

    api_key = entry_key.get()
    site_key = '6LdrVtEUAAAAAM17q4w4vDDWQauUXqNlrk0QAQIe'
    token_url = input_url
    pool_captcha = PoolCaptcha(api_key=api_key, sitekey=site_key, page_url=token_url, len_pool=10)

    while True:
        pool_captcha.update()
        write_log(1, f'Проверка свободных контрактов...')
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

        resp = requests.get(f'https://e-garant.autoins.ru/api/v2/egarant-sk-spreader/ui/{url_token}/insuranceCompanies',
                            verify=False,
                            headers=headers)
        if resp.status_code == 200:
            contract_id_token = resp.cookies['contract_id_token']
            result = resp.json()
            for item in result:

                comp_name = item["searchName"]
                if comp_name in check_list:
                    comp_id = item['id']
                    if item["contractsLeft"] > 0:
                        write_log(4, f'СК: {comp_name}. Найдено свободных контрактов: {item["contractsLeft"]}')

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
                                if check_contract_id_token(url_token, contract_id_token, comp_id):
                                    write_log(4, f'Контракт успешно зарезервирован. СК: {comp_name}')
                                    finish_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                                    with open('result.csv', 'a', encoding='utf-8') as f_res:
                                        f_res.write(f'{url_token};{start_time};{finish_time};{comp_name}\n')
                                    return
                            else:
                                write_log(2, f'Для ссылки {input_url} контракт зарегистрирован ранее')
                                return
                    else:
                        write_log(1, f'СК: {comp_name} - свободных контрактов нет.')
        else:
            with suppress(Exception):
                write_log(3, f'{resp.json()[0]["message"]}')
            write_log(2, f'Прекращаю поиск. Требуется обновить входную ссылку.')
            return

        time.sleep(1)



if __name__ == '__main__':

    if os.path.exists('result.csv') is False:
        with open('result.csv', 'w', encoding='utf-8') as f_res:
            f_res.write(f'Link;Start;Finish;SK\n')

    comn_names = open('comps.txt', 'r', encoding='utf-8').read().splitlines()
    comn_names = sorted(comn_names)

    root = Tk()
    root.title("Поиск контрактов РСА")
    root.geometry("450x420")
    note = ttk.Notebook(root)
    main_frame = ttk.Frame(note)
    note.add(main_frame, text="Главное")
    settings_frame = ttk.Frame(note)
    note.add(settings_frame, text="Настройки")
    rezult_frame = ttk.Frame(note)
    note.add(rezult_frame, text="Результаты")
    note.pack(expand=True, fill=BOTH)


    #---------------------------------------------

    class TestApp(Frame):
        def __init__(self, parent, filepath):
            super().__init__(parent)
            self.table = Table(self, showtoolbar=True, showstatusbar=True)
            self.table.importCSV(filepath, delimiter=';')
            self.table.show()


    app = TestApp(rezult_frame, 'result.csv')
    app.pack(expand = True, fill=BOTH)

    #---------------------------------------------
    # - настройки
    label = Label(settings_frame, text="API токен captcha.guru:")
    label.grid(row=0, column=1)

    entry_key = Entry(settings_frame, width=40)
    if os.path.exists('api_key.txt'):
        api_key = open('api_key.txt', 'r').read()
        entry_key.insert(0, api_key)
    else:
        entry_key.insert(0, '----')
    entry_key.grid(row=1, column=1, padx=5, pady=5)

    button_save = Button(settings_frame, text='Сохранить', command=save_key)
    button_save.grid(row=1, column=2, padx=5, pady=5)

    #------------------------------------
    label = Label(main_frame, text="Ссылка для поиска:")
    label.grid(row=0, column=1)

    entry = Entry(main_frame, width=70)
    entry.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    label = Label(main_frame, text="Выбор СК")
    label.grid(row=2, column=1)


    vscrollbar = Scrollbar(main_frame)
    canvas = Canvas(main_frame, yscrollcommand=vscrollbar.set)
    vscrollbar.config(command=canvas.yview)
    vscrollbar.grid(row=3, column=0, sticky='ns')
    frame = Frame(canvas)
    canvas.grid(row=3, column=1)
    canvas.create_window(0, 0, window=frame, anchor='nw')

    button = Button(main_frame, text='Поехали', font=('Aria', 12), command=start)
    button.grid(row=4, column=1, padx=5, pady=5)


    class CheckButton:
        def __init__(self, master, title):
            self.var = BooleanVar()
            self.var.set(0)
            self.title = title
            self.cb = Checkbutton(
                master, text=title, variable=self.var,  font=('Aria', 12),
                onvalue=1, offvalue=0, justify="left")

            self.cb.pack(side=TOP, anchor=W)


    def ch_on():
        for ch in checks:
            ch.cb.select()


    def ch_off():
        for ch in checks:
            ch.cb.deselect()


    checks = []
    for i in comn_names:
        checks.append(CheckButton(frame, i))

    root.update()
    canvas.config(scrollregion=canvas.bbox("all"))
    root.mainloop()





