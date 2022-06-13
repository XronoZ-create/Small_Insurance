from selenium_reg_alfa.steps.dadata_address import GetAddressJson
from selenium_reg_alfa.web_selenium import XpathFindAndClick, XpathFindAndPaste
from datetime import datetime
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def step_two(driver, client_data, json_table):
    # ---------------------------------- Убираем всплывающий мусор только в оконнмо режиме------------------------------
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//iframe[@class='flocktory-widget']")))
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@class='flocktory-widget']"))
    XpathFindAndClick(xpath=f"//button", driver=driver)
    driver.switch_to.default_content()
    # ------------------------------------------------------------------------------------------------------------------


    registrationAddress = GetAddressJson(address=client_data.sobstv_pass_address)()
    # --------------------------- Выбираем заполнение адреса вручную ---------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ownerAddressRegionState']", paste="агась", driver=driver)
    XpathFindAndClick(xpath=f"//input[@name='ownerAddressCity']", driver=driver)
    XpathFindAndClick(xpath=f"//label[@id='ownerAddressRegionState-error']/a", driver=driver)

    # --------------------------- Выбираем индекс ----------------------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ownerAddressZip']", paste=registrationAddress["Zip"], driver=driver)

    #  --------------------------- Выбираем область --------------------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ownerAddressState']", paste=registrationAddress["State"], driver=driver)

    #  --------------------------- Выбираем регион ---------------------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ownerAddressRegion']", paste=registrationAddress["RegionState"], driver=driver)

    #  --------------------------- Выбираем город ----------------------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ownerAddressCity']", paste=registrationAddress["City"], driver=driver)

    #  --------------------------- Выбираем улицу ----------------------------------------------------------------------
    if registrationAddress["Street"] == None:
        XpathFindAndPaste(xpath=f"//input[@name='ownerAddressStreet']", paste="Нет", driver=driver)
    else:
        XpathFindAndPaste(xpath=f"//input[@name='ownerAddressStreet']", paste=registrationAddress["Street"], driver=driver)

    #  --------------------------- Выбираем дом ------------------------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ownerAddressHouse']", paste=registrationAddress["HouseRaw"], driver=driver)

    #  --------------------------- Выбираем строение --------------------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ownerAddressBuilding']", paste=registrationAddress["Building"], driver=driver)

    #  --------------------------- Выбираем квартиру -------------------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ownerAddressApartment']", paste=registrationAddress["Flat"], driver=driver)


    # --------------------------- Заполняем водителей ------------------------------------------------------------------
    if client_data.c_ogr_or_not == 'С ограничением':
        id_vod = 1
        for one_vod in client_data.voditeli:
            XpathFindAndPaste(xpath=f"//input[@name='driver[{id_vod}][Surname]']", paste=one_vod.surname, driver=driver)
            XpathFindAndPaste(xpath=f"//input[@name='driver[{id_vod}][Name]']", paste=one_vod.name, driver=driver)
            XpathFindAndPaste(xpath=f"//input[@name='driver[{id_vod}][Patronymic]']", paste=one_vod.otchestvo, driver=driver)

            XpathFindAndPaste(xpath=f"//input[@name='driver[{id_vod}][BirthDate]']", paste=datetime.strptime(one_vod.birthday, "%Y-%m-%d").strftime("%d.%m.%Y"), driver=driver)

            XpathFindAndPaste(xpath=f"//input[@name='driver[{id_vod}][Serial]']", paste=one_vod.seriya_vu, driver=driver)
            XpathFindAndPaste(xpath=f"//input[@name='driver[{id_vod}][Number]']", paste=one_vod.nomer_vu, driver=driver)

            XpathFindAndPaste(xpath=f"//input[@name='driver[{id_vod}][DateIssue]']", paste=datetime.strptime(one_vod.data_vidachi_vu, "%Y-%m-%d").strftime("%d.%m.%Y"), driver=driver)  # почему то не дает раньше 2018г. указывать

            try:  # ловим ошибку, если ид больше, чем существует в списке водителей
                if client_data.voditeli[id_vod].surname != "":
                    id_vod += 1
                    XpathFindAndClick(xpath="//span[text() = 'Добавить водителя']", driver=driver)
                else:
                    break
            except:
                pass

    XpathFindAndClick(driver=driver, xpath="//button[@name='submit_step1']")
    # ------------------------------------------------------------------------------------------------------------------

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='insurerEmail']")))

    json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Данные водителей успешно заполнены')
    print('Данные водителей успешно заполнены')