from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def XpathFindAndClick(driver, xpath, time_wait=2, action=False):
    try:
        if action:
            raise Exception
        wait = WebDriverWait(driver, time_wait)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        f_el = driver.find_element_by_xpath(xpath)

        actions = ActionChains(driver)
        actions.move_to_element(f_el).perform()

        f_el.click()
    except Exception as err:
        f_el = driver.find_element_by_xpath(xpath)
        driver.execute_script("arguments[0].scrollIntoView();", f_el)
        driver.execute_script("arguments[0].click();", f_el)


def XpathFindAndPaste(xpath, paste, driver):
    if paste == None:
        return
    wait = WebDriverWait(driver, 1)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    f_el = driver.find_element_by_xpath(xpath)

    actions = ActionChains(driver)
    actions.move_to_element(f_el).perform()

    f_el.send_keys(paste)