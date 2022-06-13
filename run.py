import modules.rsa_checker.rsa_cheker_bot_w_site as rsa_cheker_bot
from modules.rsa_checker.rsa_cheker_bot_w_site import StopFind
from loguru import logger
import time
from datetime import datetime, timedelta
from contextlib import suppress
from modules.other_methods import check_ip
import sys
import random
from modules.json_table import JsonTable
from request_reg_ugsk.reg_acc import RegAcc as RegAccUGSK, AccAlreadyReg
from request_reg_ugsk.create_osago import CreateInsurance as CreateInsuranceUGSK, AuthErrorUGSK, CreateErrorUGSK
from request_reg_21.reg_acc import RegAcc as RegAcc21
from request_reg_21.create_osago import CreateInsurance as CreateInsurance21, AuthError21, CreateError21

from request_reg_arm.reg_acc import RegAcc as RegAccArm
from request_reg_arm.create_osago import CreateInsurance as CreateInsuranceArm, AuthErrorArm, CreateErrorArm

from request_reg_alfa.create_osago import CreateInsurance as CreateInsuranceAlfa, CreateErrorAlfa

from requests_reg_vsk.create_osago import CreateInsurance as CreateInsuranceVsk, CreateErrorVsk


sys.stdout.flush()

def check_start():
    """ Проверка необходимости запуска бота """
    while True:
        json_table = JsonTable()
        data = json_table.data
        type = json_table.type
        print({"data": data, "type": type})

        if data != None and type == "hook":
            return json_table, type
        elif data != None and type == "osago_ugsk":
            return json_table, type
        elif data != None and type =="osago_21":
            return json_table, type
        elif data != None and type =="osago_arm":
            return json_table, type
        elif data != None and type =="osago_alfa":
            return json_table, type
        elif data != None and type =="osago_vsk":
            return json_table, type
        else:
            time.sleep(random.randrange(5, 50) / 10)


@logger.catch
def start():
    while True:
        try:
            json_table, type = check_start()
            if type == "hook":
                start_hook(json_table)
            elif type == "osago_ugsk":
                start_ugsk(json_table)
            elif type == "osago_21":
                start_21(json_table)
            elif type == "osago_arm":
                start_arm(json_table)
            elif type == "osago_alfa":
                start_alfa(json_table)
            elif type == "osago_vsk":
                start_vsk(json_table)
        except Exception as err:
            with suppress(Exception):
                json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Критическая ошибка: {err}')

def start_hook(json_table):
    hook_data = json_table.data
    json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Бот приступил к выполнению')

    try:
        rsa_cheker_bot.start_find(input_url=hook_data.input_url, json_table=json_table)
    except StopFind:
        pass

def start_ugsk(json_table):
    # ----------------------------------------------------Регистрация---------------------------------------------------
    client_data = json_table.data
    json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Бот приступил к выполнению')
    if client_data.login_osk != "":
        print("Аккаунт уже зарегистрирован")
    else:
        try:
            reg_acc = RegAccUGSK()
            reg_acc.run(reg_data=client_data, json_table=json_table)
        except AccAlreadyReg:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: аккаунт уже зарегистрирован')
            logger.exception("RegFailed")
            return
        except Exception:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при регистрации')
            logger.exception("RegFailed")
            return

    # --------------------------------------------------Создание ОСАГО--------------------------------------------------
    if client_data.login_osk == "":
        return
    try:
        create_insurance = CreateInsuranceUGSK(json_table=json_table)
        create_insurance.auth()
        url_rca = create_insurance.create()
        rsa_cheker_bot.start_find(input_url=url_rca, json_table=json_table, telephone=create_insurance.telephone)
        create_insurance.rca_create_dog(url_rca=url_rca)
        json_table.stop_bot()
        json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Завершено')
    except AuthErrorUGSK:
        logger.exception("AuthErrorUGSK")
    except CreateErrorUGSK:
        logger.exception("CreateErrorUGSK")
    except StopFind:
        print("Бот остановлен")
        json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Бот остановлен')
    except Exception:
        json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при создании ОСАГО')
        logger.exception("CreateInsuranceFailed")

    with suppress(Exception):
        create_insurance.telephone.end_number()

def start_21(json_table):
    # ----------------------------------------------------Регистрация---------------------------------------------------
    client_data = json_table.data
    json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Бот приступил к выполнению')
    if client_data.login_osk != "":
        print("Аккаунт уже зарегистрирован")
    else:
        try:
            reg_acc = RegAcc21()
            reg_acc.run(reg_data=client_data, json_table=json_table)
        except AccAlreadyReg:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: аккаунт уже зарегистрирован')
            logger.exception("RegFailed")
            return
        except Exception:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при регистрации')
            logger.exception("RegFailed")
            return

    # --------------------------------------------------Создание ОСАГО--------------------------------------------------
    if client_data.login_osk == "":
        return
    try:
        create_insurance = CreateInsurance21(json_table=json_table)
        create_insurance.auth()
        url_rca = create_insurance.create()
        rsa_cheker_bot.start_find(input_url=url_rca, json_table=json_table, telephone=create_insurance.telephone)
        create_insurance.rca_create_dog(url_rca=url_rca)
        json_table.stop_bot()
        json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Завершено')
    except AuthError21:
        logger.exception("AuthErrorUGSK")
    except CreateError21:
        logger.exception("CreateErrorUGSK")
    except StopFind:
        print("Бот остановлен")
        json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Бот остановлен')
    except Exception:
        json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при создании ОСАГО')
        logger.exception("CreateInsuranceFailed")

    with suppress(Exception):
        create_insurance.telephone.end_number()

def start_arm(json_table):
    # ----------------------------------------------------Регистрация---------------------------------------------------
    client_data = json_table.data
    json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Бот приступил к выполнению')

    if client_data.login_osk != "" and \
            client_data.telephone != "" and \
            (
                (client_data.telephone_service == 'onlinesim' and (datetime.now() - datetime.strptime(client_data.reg_date_telephone, "%d.%m %H:%M %Y")) < timedelta(minutes=30)) or
                ((datetime.now() - datetime.strptime(client_data.reg_date_telephone, "%d.%m %H:%M %Y")) < timedelta(minutes=50))
            ):
        print("Аккаунт уже зарегистрирован")
    else:
        try:
            reg_acc = RegAccArm()
            telephone = reg_acc.run(reg_data=client_data, json_table=json_table)[2]
            reg_date = datetime.now()

            tel_number = telephone.tel[1:]
            json_table.set_value('reg_date_telephone', telephone.active_client.date.strftime("%d.%m %H:%M %Y"))
            json_table.set_value('telephone', tel_number)
            json_table.set_value('id_num_telephone', telephone.active_client.id_num)
            json_table.set_value('telephone_service', telephone.active_client.name)
        except AccAlreadyReg:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка: аккаунт уже зарегистрирован')
            logger.exception("RegFailed")
            return
        except Exception:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при регистрации')
            logger.exception("RegFailed")
            return

    # --------------------------------------------------Создание ОСАГО--------------------------------------------------

    while json_table.active and (
                (client_data.telephone_service == 'onlinesim' and (datetime.now() - datetime.strptime(client_data.reg_date_telephone, "%d.%m %H:%M %Y")) < timedelta(minutes=30)) or
                ((datetime.now() - datetime.strptime(client_data.reg_date_telephone, "%d.%m %H:%M %Y")) < timedelta(minutes=50))
            ):
        try:
            create_insurance = CreateInsuranceArm(json_table=json_table)
            create_insurance.auth()
            url_rca = create_insurance.create()
            rsa_cheker_bot.start_find(input_url=url_rca, json_table=json_table, telephone=create_insurance.telephone)
            create_insurance.rca_create_dog(url_rca=url_rca)
            json_table.stop_bot()
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Завершено')
        except AuthErrorArm:
            logger.exception("AuthErrorUGSK")
        except CreateErrorArm:
            logger.exception("CreateErrorUGSK")
        except StopFind:
            print("Бот остановлен")
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Бот остановлен')
        except Exception:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при создании ОСАГО')
            logger.exception("CreateInsuranceFailed")

def start_alfa(json_table):
    client_data = json_table.data
    json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Бот приступил к выполнению')

    # --------------------------------------------------Создание ОСАГО--------------------------------------------------

    while json_table.active:
        try:
            create_insurance = CreateInsuranceAlfa(json_table=json_table)
            create_insurance.auth()
            create_insurance.create()

            json_table.stop_bot()
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Завершено')
        except CreateErrorAlfa:
            logger.exception("CreateErrorAlfa")
        except StopFind:
            print("Бот остановлен")
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Бот остановлен')
        except Exception:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при создании ОСАГО')
            logger.exception("CreateInsuranceFailed")

def start_vsk(json_table):
    json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Бот приступил к выполнению')

    # --------------------------------------------------Создание ОСАГО--------------------------------------------------
    try:
        create_insurance = CreateInsuranceVsk(json_table=json_table)
        create_insurance.auth()
    except Exception:
        json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при создании ОСАГО')
        logger.exception("CreateInsuranceFailed")
        with suppress(Exception):
            create_insurance.driver.quit()
        return

    while json_table.active:
        try:
            url_rca = create_insurance.create()

            json_table.stop_bot()
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Завершено')
        except CreateErrorVsk:
            logger.exception("CreateErrorVSK")
        except StopFind:
            print("Бот остановлен")
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Бот остановлен')
        except Exception:
            json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка при создании ОСАГО')
            logger.exception("CreateInsuranceFailed")
    with suppress(Exception):
        create_insurance.driver.quit()

if __name__ == "__main__":
    logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB")
    start()