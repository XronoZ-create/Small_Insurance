from selenium_reg_alfa.web_selenium import XpathFindAndClick, XpathFindAndPaste
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime

def step_one(driver, client_data, json_table):
    # --------------------------- Подтверждение обработки данных -------------------------------------------------------
    XpathFindAndClick(driver=driver, xpath="//span[@class='cookie-info__close']")

    # --------------------------- Номер машины и регион ----------------------------------------------------------------
    auto_number = client_data.ctc_ptc_reg_znak.replace(" ", "")
    XpathFindAndPaste(xpath="//input[@id='AUTO_NUMBER']", paste=f"{auto_number[0:1]} {auto_number[1:4]} {auto_number[4:]}", driver=driver)
    XpathFindAndPaste(xpath="//input[@name='AUTO_REGION']", paste=client_data.auto_region, driver=driver)

    # --------------------------- VIN ------------------------------------------------------------
    XpathFindAndPaste(xpath="//input[@name='CarIdVIN']", paste=client_data.ctc_ptc_vin, driver=driver)

    # --------------------------- Выбираем категорию -------------------------------------------------------------------
    XpathFindAndClick(driver=driver, xpath="//span[@id='select2-category-container']")
    XpathFindAndClick(driver=driver, xpath=f"//select[@id='category']/parent::span//ul/li[text() = '{client_data.category}']")
    time.sleep(0.5)

    # --------------------------- Заполняем доп.поля для определнных классов автомобилей -------------------------------
    if client_data.category == "C - грузовые":
        XpathFindAndPaste(xpath="//input[@id='Weight']", paste=client_data.max_mass, driver=driver)
    elif client_data.category == "D - автобусы":
        XpathFindAndPaste(xpath="//input[@id='Seats']", paste=client_data.count_pass_mest, driver=driver)

    # -------------------------- Заполняем данные авто -----------------------------------------------------------------
    if client_data.brand_name_other == "":
        standard_auto(driver=driver, client_data=client_data)
    else:
        other_auto(driver=driver, client_data=client_data)

    # --------------------------- Выбираем цель использования ----------------------------------------------------------
    XpathFindAndClick(driver=driver, xpath=f"//select[@id='purposeName']/parent::span")
    XpathFindAndClick(driver=driver, xpath=f"//select[@id='purposeName']/parent::span//ul/li[text() = '{client_data.target}']")

    XpathFindAndClick(driver=driver, xpath="//button[@class='btn js-submit-osago-step-1']")
    # ------------------------------------------------------------------------------------------------------------------


    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='ownerAddressRegionState']")))

    json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Данные авто успешно заполнены')
    print('Данные авто успешно заполнены')


def standard_auto(driver, client_data):
    # --------------------------- Выбираем марку -----------------------------------------------------------------------
    XpathFindAndPaste(xpath="//input[@id='mark']", paste=client_data.brand_name, driver=driver)
    time.sleep(0.5)
    driver.wait_for_request("action=models").response

    # --------------------------- Выбираем модель ----------------------------------------------------------------------
    XpathFindAndPaste(xpath="//input[@id='model']", paste=client_data.model_name, driver=driver)
    XpathFindAndClick(xpath=f"//div[@data-code-value='{client_data.model}']", driver=driver)
    time.sleep(0.5)

    # --------------------------- Выбираем год -------------------------------------------------------------------------
    XpathFindAndPaste(xpath="//input[@id='year']", paste=client_data.year, driver=driver)
    time.sleep(0.5)
    driver.wait_for_request('action=modifications').response

    # --------------------------- Выбираем модификацию -----------------------------------------------------------------
    XpathFindAndClick(driver=driver, xpath=f"//select[@id='modification']/parent::span")
    XpathFindAndClick(driver=driver, xpath=f"//select[@id='modification']/parent::span")
    XpathFindAndClick(driver=driver, xpath=f"//select[@id='modification']/parent::span//ul/li[text() = '{client_data.modification_name}']")

def other_auto(driver, client_data):
    # --------------------------- Выбираем марку -----------------------------------------------------------------------
    XpathFindAndPaste(xpath="//input[@id='mark']", paste="ДРУГОЕ ТС", driver=driver)
    time.sleep(0.5)
    XpathFindAndPaste(xpath="//input[@id='brand_name_other']", paste=client_data.brand_name_other, driver=driver)
    time.sleep(0.5)

    # --------------------------- Выбираем модель ----------------------------------------------------------------------
    XpathFindAndPaste(xpath="//input[@id='other_model']", paste=client_data.model_name_other, driver=driver)
    time.sleep(0.5)

    # --------------------------- Заполняем мощность -------------------------------------------------------------------
    XpathFindAndPaste(xpath="//input[@id='carPower']", paste=client_data.powers, driver=driver)
    time.sleep(0.5)

    # --------------------------- Выбираем год -------------------------------------------------------------------------
    XpathFindAndPaste(xpath="//input[@id='year']", paste=client_data.year, driver=driver)
    time.sleep(0.5)
    driver.wait_for_request('action=modifications').response

    # --------------------------- Выбираем модификацию -----------------------------------------------------------------
    XpathFindAndClick(driver=driver, xpath=f"//select[@id='modification']/parent::span")
    XpathFindAndClick(driver=driver, xpath=f"//select[@id='modification']/parent::span")
    XpathFindAndClick(driver=driver, xpath=f"//select[@id='modification']/parent::span//ul/li[text() = '{client_data.modification_name}']")