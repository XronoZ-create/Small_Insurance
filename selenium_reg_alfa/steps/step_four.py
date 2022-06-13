from selenium_reg_alfa.steps.dadata_address import GetAddressJson
from selenium_reg_alfa.web_selenium import XpathFindAndClick, XpathFindAndPaste
from datetime import datetime
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def step_four(driver, client_data, json_table):
    # --------------------------- Выбираем подходящий тип документа ----------------------------------------------------
    if client_data.type_document == 'ПТС':
        pass
    elif client_data.type_document == 'СТС':
        XpathFindAndClick(driver=driver, xpath="//span[@class='select2-selection select2-selection--single']")
        XpathFindAndClick(driver=driver, xpath=f"//ul[@class='select2-results__options']/li[position()=2]")
        time.sleep(0.5)
    elif client_data.type_document == 'ПСМ':
        XpathFindAndClick(driver=driver, xpath="//span[@class='select2-selection select2-selection--single']")
        XpathFindAndClick(driver=driver, xpath=f"//ul[@class='select2-results__options']/li[position()=3]")
        time.sleep(0.5)
    elif client_data.type_document == 'ЭПТС':
        XpathFindAndClick(driver=driver, xpath="//span[@class='select2-selection select2-selection--single']")
        XpathFindAndClick(driver=driver, xpath=f"//ul[@class='select2-results__options']/li[position()=4]")
        time.sleep(0.5)

    # ------------------------------- Заполняем данные документа на авто -----------------------------------------------
    if client_data.type_document != 'ePassport':
        # --------------------------- Указываем серию документа --------------------------------------------------------
        XpathFindAndPaste(xpath=f"//input[@name='ptsSerial']", paste=client_data.ctc_ptc_seriya, driver=driver)

    # --------------------------- Указываем номер документа --------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ptsNumber']", paste=client_data.ctc_ptc_number, driver=driver)

    # --------------------------- Указываем дату документа ---------------------------------------------------------
    XpathFindAndPaste(xpath=f"//input[@name='ptsDateIssue']", paste=datetime.strptime(client_data.ctc_ptc_vidach, "%Y-%m-%d").strftime("%d.%m.%Y"), driver=driver)

    # --------------------------- Указываем наличие прицепа ------------------------------------------------------------
    if client_data.pricep != "":
        XpathFindAndClick(driver=driver, xpath=f"//select[@name='WithUseTrailer']/parent::span")
        XpathFindAndClick(driver=driver, xpath=f"//select[@name='WithUseTrailer']/parent::span//option[text() = 'Да']")

    XpathFindAndClick(driver=driver, xpath=f"//button[@name='submit_step3']")

    XpathFindAndClick(driver=driver, xpath=f"//input[@name='agreement']", time_wait=10)
    XpathFindAndClick(driver=driver, xpath=f"//button[text() = 'Перейти в егарант']", time_wait=10)

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//form[@class='form js-validate js-no-ajax js-no-loader']")))

    egarant_url = driver.find_element_by_xpath("//form[@class='form js-validate js-no-ajax js-no-loader']").get_attribute('action')
    print(egarant_url)

    if egarant_url == "http://egarant.autoins.ru/egarant-web-1.0/insuranceCompany.htm?DraftPolicyId=":
        json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Ошибка. Пустой ответ от Альфа')
        raise Exception

    json_table.set_value("status_bot", f'{datetime.now().strftime("%d.%m %H:%M")} Успешно получена ссылка на Е-ГАРАНТ')
    print("Успешно получена ссылка на Е-ГАРАНТ")

    return egarant_url