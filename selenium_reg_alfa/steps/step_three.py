from selenium_reg_alfa.steps.dadata_address import GetAddressJson
from selenium_reg_alfa.web_selenium import XpathFindAndClick, XpathFindAndPaste
from datetime import datetime, timedelta
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from modules.telephone import TelephoneActivateSms


def step_three(driver, client_data, json_table):
    # --------------------------- Указываем емайл ----------------------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='insurerEmail']", paste=client_data.email_login, driver=driver)

    # --------------------------- Указываем телефон --------------------------------------------------------------------
    # if client_data.telephone != "" and ((datetime.now() - datetime.strptime(client_data.reg_date_telephone, "%d.%m %H:%M %Y")) < timedelta(minutes=50)):
    #     telephone = TelephoneActivateSms(
    #         id_num=client_data.id_num_telephone,
    #         date=datetime.strptime(client_data.reg_date_telephone, "%d.%m %H:%M %Y")
    #     )
    #     telephone.retry_sms()
    #     phone_number = client_data.telephone
    # else:
    #     telephone = TelephoneActivateSms()
    #     telephone.get_number()
    #     phone_number = telephone.tel[1:]
    telephone = TelephoneActivateSms()
    telephone.get_number()
    phone_number = telephone.tel[1:]

    XpathFindAndPaste(xpath=f"//input[@name='insurerPhone']", paste=phone_number, driver=driver)

    # --------------------------- Отправляем код -----------------------------------------------------------------------
    XpathFindAndClick(xpath=f"//div[@class='form__row phone-visible ']//button", driver=driver)

    # --------------------------- Подтверждаем телефон -----------------------------------------------------------------
    phone_code = telephone.get_sms_code()
    XpathFindAndPaste(xpath=f"//input[@id='confirmPhoneCode']", paste=phone_code, driver=driver)
    time.sleep(0.5)
    XpathFindAndClick(xpath=f"//label[@class='form__row phone-hidden']//button", driver=driver)

    # --------------------------- Указываем фамилию страхователя -------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='insurerSurname']", paste=client_data.surname, driver=driver)

    # --------------------------- Указываем имя страхователя -----------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='insurerName']", paste=client_data.name, driver=driver)

    # --------------------------- Указываем отчество страхователя ------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='insurerPatronymic']", paste=client_data.otchestvo, driver=driver)

    # --------------------------- Указываем дату рождения страхователя -------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='insurerBirthDate']", paste=datetime.strptime(client_data.birthday, "%Y-%m-%d").strftime("%d.%m.%Y"), driver=driver)

    # --------------------------- Указываем серию паспорта страхователя ------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='insurerSerial']", paste=client_data.pass_seriya, driver=driver)

    # --------------------------- Указываем номер паспорта страхователя ------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='insurerNumber']", paste=client_data.pass_number, driver=driver)


    registrationAddress = GetAddressJson(address=client_data.pass_address)()
    # --------------------------- Выбираем заполнение адреса вручную ---------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='insurerAddressRegionState']", paste="агась", driver=driver)
    XpathFindAndClick(xpath=f"//input[@name='insurerAddressCity']", driver=driver)
    XpathFindAndClick(xpath=f"//label[@id='insurerAddressRegionState-error']/a", driver=driver)

    # --------------------------- Выбираем индекс ----------------------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='insurerAddressZip']", paste=registrationAddress["Zip"], driver=driver)

    #  --------------------------- Выбираем область --------------------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='insurerAddressState']", paste=registrationAddress["State"], driver=driver)

    #  --------------------------- Выбираем регион ---------------------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='insurerAddressRegion']", paste=registrationAddress["RegionState"], driver=driver)

    #  --------------------------- Выбираем город ----------------------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='insurerAddressCity']", paste=registrationAddress["City"], driver=driver)

    #  --------------------------- Выбираем улицу ----------------------------------------------------------------------
    if registrationAddress["Street"] == None:
        XpathFindAndPaste(xpath=f"//input[@name='insurerAddressStreet']", paste="Нет", driver=driver)
    else:
        XpathFindAndPaste(xpath=f"//input[@name='insurerAddressStreet']", paste=registrationAddress["Street"], driver=driver)

    #  --------------------------- Выбираем дом ------------------------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='insurerAddressHouse']", paste=registrationAddress["HouseRaw"], driver=driver)

    #  --------------------------- Выбираем строение --------------------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='insurerAddressBuilding']", paste=registrationAddress["Building"], driver=driver)

    #  --------------------------- Выбираем квартиру -------------------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='insurerAddressApartment']", paste=registrationAddress["Flat"], driver=driver)


    # --------------------------- Указываем фамилию собственника -------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ownerSurname']", paste=client_data.sobstv_surname, driver=driver)

    # --------------------------- Указываем имя собственника -----------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ownerName']", paste=client_data.sobstv_name, driver=driver)

    # --------------------------- Указываем отчество собственника ------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ownerPatronymic']", paste=client_data.sobstv_otchestvo, driver=driver)

    # --------------------------- Указываем дату рождения собственника -------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ownerBirthDate']", paste=datetime.strptime(client_data.sobstv_birthday, "%Y-%m-%d").strftime("%d.%m.%Y"), driver=driver)

    # --------------------------- Указываем серию паспорта собственника ------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ownerSerial']", paste=client_data.sobstv_pass_seriya, driver=driver)

    # --------------------------- Указываем номер паспорта собственника ------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ownerNumber']", paste=client_data.sobstv_pass_number, driver=driver)

    # --------------------------- Подтверждаем согласие на обработку данных --------------------------------------------
    XpathFindAndClick(xpath=f"//input[@name='agreeLimited']", driver=driver)

    XpathFindAndClick(xpath=f"//button[@name='submit_step2']", driver=driver)
    # ------------------------------------------------------------------------------------------------------------------


    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='ptsSerial']")))

    json_table.set_value('reg_date_telephone', telephone.date.strftime("%d.%m %H:%M %Y"))
    json_table.set_value('telephone', phone_number)
    json_table.set_value('id_num_telephone', telephone.id_num)
    json_table.set_value('telephone_service', telephone.name)

    json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Данные страхователя и собственника успешно заполнены')
    print("Данные страхователя и собственника успешно заполнены")

    return telephone