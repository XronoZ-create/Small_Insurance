from selenium_reg.reg_acc import RegAcc, AccAlreadyReg
from modules.web_selenium import selenium_client
from modules.selen_analyze import selen_analyze
from modules.table import GoogleTable
from selenium_reg.create_insurance import CreateInsurance, CreateInsuranceFailed, WrongRegData
import modules.rsa_checker.rsa_cheker_bot as rsa_cheker_bot
from modules.rsa_checker.rsa_cheker_bot import StopFind
from loguru import logger
import time
from datetime import datetime
from contextlib import suppress
from modules.other_methods import check_ip
import sys
import random
sys.stdout.flush()

def check_start(server_address):
    """ Проверка необходимости запуска бота """
    while True:
        break_point = False
        id_row = 0
        for client_data in GoogleTable().data:
            status_bot = client_data.status_bot
            if client_data.server_address == server_address and client_data.start_bot != "":
                break_point = True
                break
            elif client_data.server_address == server_address and\
                    client_data.start_bot == "" and\
                    status_bot.find("Бот остановлен") == -1 and\
                    status_bot.find("Завершено") == -1 and \
                    status_bot.find("Ошибка ОСК") == -1:
                client_data.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Бот остановлен')
            id_row += 1
            time.sleep(random.randrange(5, 10) / 10)
        if break_point == True:
            break
        else:
            time.sleep(60)
    return id_row

@logger.catch
def start():
    server_address = check_ip()

    """ Блок регистрации """
    while True:
        id_row = check_start(server_address=server_address)
        sel_cl = selenium_client(headless=True)
        sel_an = selen_analyze(client=sel_cl)

        for _ in range(0, 3):
            try:
                client_data = GoogleTable().data[id_row]
                break
            except:
                time.sleep((random.randrange(1, 10)) / 10)

        if client_data.login_osk != "":
            print("Аккаунт уже зарегистрирован")
            sel_cl.quit_browser()
            break
        if client_data.start_bot == "":
            print("Бот остановлен")
            client_data.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Бот остановлен')
            sel_cl.quit_browser()
            break
        try:
            reg_acc = RegAcc(sel_client=sel_cl, sel_analyze=sel_an)
            reg_acc.run(reg_data=client_data)
            client_data.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Аккаунт успешно зарегистрирован')
            sel_cl.quit_browser()
            break
        except AccAlreadyReg:
            client_data.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: аккаунт уже зарегистрирован')
            logger.exception("RegFailed")
            sel_cl.quit_browser()
        except Exception:
            client_data.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при регистрации')
            logger.exception("RegFailed")
            sel_cl.quit_browser()

    """ Блок создания ОСАГО """
    while True:
        id_row = check_start(server_address=server_address)

        for _ in range(0, 3):
            try:
                client_data = GoogleTable().data[id_row]
                break
            except:
                time.sleep((random.randrange(1, 10))/10)

        if client_data.start_bot == "":
            print("Бот остановлен")
            client_data.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Бот остановлен')
            break
        elif client_data.login_osk == "":
            break
        try:
            sel_cl = selenium_client(headless=True)
            sel_an = selen_analyze(client=sel_cl)
            create_insurance = CreateInsurance(sel_client=sel_cl, sel_analyze=sel_an, client_data=client_data)
            create_insurance.auth()
            create_insurance.one()
            create_insurance.two()
            create_insurance.three()
            create_insurance.four()
            create_insurance.five()
            create_insurance.six()
            url_rca = create_insurance.seven()
            rsa_cheker_bot.start_find(input_url=url_rca, client_data=client_data, telephone=create_insurance.telephone)
            create_insurance.rca_create_dog(url_rca=url_rca)

            client_data.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Завершено')
            client_data.set_value("start_bot", "")

            break
        except CreateInsuranceFailed:
            client_data.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при создании ОСАГО')
            logger.exception("CreateInsuranceFailed")

            with suppress(Exception):
                sel_cl.save_page()
                sel_cl.save_screenshot()
            sel_cl.quit_browser()
            with suppress(Exception):
                create_insurance.telephone.end_number()
        except WrongRegData:
            logger.exception("WrongRegData")

            client_data.set_value("start_bot", "")
            with suppress(Exception):
                sel_cl.save_page()
                sel_cl.save_screenshot()
            sel_cl.quit_browser()
            with suppress(Exception):
                create_insurance.telephone.end_number()
            break
        except StopFind:
            print("Бот остановлен")
            client_data.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Бот остановлен')

            with suppress(Exception):
                create_insurance.telephone.end_number()
            break
        except Exception:
            client_data.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при создании ОСАГО')
            logger.exception("CreateInsuranceFailed")

            with suppress(Exception):
                sel_cl.save_page()
                sel_cl.save_screenshot()
            sel_cl.quit_browser()
            with suppress(Exception):
                create_insurance.telephone.end_number()


if __name__ == "__main__":
    logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB")
    start()