import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from contextlib import suppress
from selenium.webdriver.support.ui import Select
import os
import sys

class selen_analyze():
    def __init__(self, client):
        self.client = client.client

    def XpathFindAndClick(self, xpath):
        try:
            self.f_el = self.client.find_element_by_xpath("//%s[@%s='%s']" % (xpath[0],xpath[1], xpath[2]))
            self.f_el.click()
        except ElementClickInterceptedException:
            self.f_el = self.client.find_element_by_xpath("//%s[@%s='%s']" % (xpath[0], xpath[1], xpath[2]))
            self.client.execute_script("arguments[0].click();", self.f_el)

    def ListXpathFindAndClick(self, xpath):
        for self.a in xpath:
            WebDriverWait(self.client, 20).until(EC.presence_of_element_located(
                (By.XPATH, "//%s[@%s='%s']" % (self.a[0],self.a[1], self.a[2]) )
            ))
            self.XpathFindAndClick(self.a)

    def XpathFindAndPaste(self, xpath):
        """
        Были проблемы на linux-е: не слался символ /
        Поэтому было принято решение всегда работать через вставку скрипта js
        
        :param xpath:
        :return:
        """
        try:
            self.f_el = self.client.find_element_by_xpath("//%s[@%s='%s']" % (xpath[0], xpath[1], xpath[2]))
            # self.f_el.send_keys(xpath[3])
            self.client.execute_script("arguments[0].value='%s';" % xpath[3], self.f_el)
        except ElementNotInteractableException:
            self.f_el = self.client.find_element_by_xpath("//%s[@%s='%s']" % (xpath[0], xpath[1], xpath[2]))
            self.client.execute_script("arguments[0].value='%s';" % xpath[3], self.f_el)

    def ListXpathFindAndPaste(self, xpath):
        for self.a in xpath:
            WebDriverWait(self.client, 20).until(EC.presence_of_element_located(
                (By.XPATH, "//%s[@%s='%s']" % (self.a[0], self.a[1], self.a[2]))
            ))
            self.XpathFindAndPaste(self.a)

    def activate_button(self, xpath):
        self.f_el = self.client.find_element_by_xpath("//%s[@%s='%s']" % (xpath[0], xpath[1], xpath[2]))
        self.client.execute_script("arguments[0].disabled = false;", self.f_el)

    def accept_alert(self):
        self.client.switch_to.alert.accept()

    def XpathChangeValue(self, xpath, value):
        print('Меняем значение в элементе на: %s' % value)
        time.sleep(15)
        self.f_el = self.client.find_element_by_xpath("//%s[@%s='%s']" % (xpath[0], xpath[1], xpath[2]))
        self.client.execute_script("arguments[0].setAttribute('value','%s')" % value, self.f_el)

    def MoveToElement(self, xpath):
        self.action = ActionChains(self.client)
        self.f_el = self.client.find_element_by_xpath("//%s[@%s='%s']" % (xpath[0], xpath[1], xpath[2]))
        self.action.move_to_element(self.f_el).perform()

    def MoveFromOneElementToTwo(self, xpath_one, xpath_two):
        self.action = ActionChains(self.client)
        self.f_el_one = self.client.find_element_by_xpath("//%s[@%s='%s']" % (xpath_one[0], xpath_one[1], xpath_one[2]))
        self.f_el_two = self.client.find_element_by_xpath("//%s[@%s='%s']" % (xpath_two[0], xpath_two[1], xpath_two[2]))

        self.action.move_to_element(self.f_el_one)
        self.action.move_to_element(self.f_el_two)
        self.action.perform()


    def ActionSendKeys(self, xpath):
        self.action = ActionChains(self.client)
        with suppress(Exception):
            self.action.move_to_element(self.f_el)
        self.f_el = self.client.find_element_by_xpath("//%s[@%s='%s']" % (xpath[0], xpath[1], xpath[2]))

        self.action.move_to_element(self.f_el)
        self.action.click()
        self.action.send_keys_to_element(self.f_el, xpath[3])

        self.action.perform()

    def ActionFindAndClick(self, xpath):
        self.action = ActionChains(self.client)
        with suppress(Exception):
            self.action.move_to_element(self.f_el)
        self.f_el = self.client.find_element_by_xpath("//%s[@%s='%s']" % (xpath[0], xpath[1], xpath[2]))
        self.client.execute_script("arguments[0].scrollIntoView();", self.f_el)

        self.action.move_to_element(self.f_el)
        self.action.click()

        self.action.perform()

    def clear_f_el(self):
        self.f_el = None

    def ClearInputField(self, xpath):
        self.action = ActionChains(self.client)
        with suppress(Exception):
            self.action.move_to_element(self.f_el)
        self.f_el = self.client.find_element_by_xpath("//%s[@%s='%s']" % (xpath[0], xpath[1], xpath[2]))

        self.action.move_to_element(self.f_el)
        self.action.click()
        for self._ in range(0, 10):
            self.action.send_keys_to_element(self.f_el, Keys.BACKSPACE)

        self.action.perform()

    def ActionFindAndClickByXpathString(self, xpath_str):
        self.action = ActionChains(self.client)
        with suppress(Exception):
            self.action.move_to_element(self.f_el)
        self.f_el = self.client.find_element_by_xpath(xpath_str)
        self.client.execute_script("arguments[0].scrollIntoView();", self.f_el)

        self.action.move_to_element(self.f_el)
        self.action.click()

        self.action.perform()

    def WaitElementClickable(self, xpath):
        WebDriverWait(self.client, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "//%s[@%s='%s']" % (xpath[0], xpath[1], xpath[2]))
        ))

    def ActionClearAndSendKeys(self, xpath):
        self.ClearInputField(xpath)
        self.action = ActionChains(self.client)
        with suppress(Exception):
            self.action.move_to_element(self.f_el)
        self.f_el = self.client.find_element_by_xpath("//%s[@%s='%s']" % (xpath[0], xpath[1], xpath[2]))

        self.action.move_to_element(self.f_el)
        self.action.click()
        self.action.send_keys_to_element(self.f_el, xpath[3])

        self.action.perform()

    def SelectValue(self, xpath):
        self.select = Select(self.client.find_element_by_xpath("//%s[@%s='%s']" % (xpath[0], xpath[1], xpath[2])))
        self.select.select_by_visible_text(xpath[3])

    def ActionSendKeysIndex(self, xpath):
        self.action = ActionChains(self.client)
        with suppress(Exception):
            self.action.move_to_element(self.f_el)
        self.f_el = self.client.find_elements_by_xpath("//%s[@%s='%s']" % (xpath[0], xpath[1], xpath[2]))[xpath[3]]

        self.action.move_to_element(self.f_el)
        self.action.click()
        self.action.send_keys_to_element(self.f_el, xpath[4])

        self.action.perform()

    def ActionFindAndClickIndex(self, xpath):
        self.action = ActionChains(self.client)
        with suppress(Exception):
            self.action.move_to_element(self.f_el)
        self.f_el = self.client.find_elements_by_xpath("//%s[@%s='%s']" % (xpath[0], xpath[1], xpath[2]))[xpath[3]]
        self.client.execute_script("arguments[0].scrollIntoView();", self.f_el)

        self.action.move_to_element(self.f_el)
        self.action.click()

        self.action.perform()

    def WaitElementClickableXpathString(self, xpath_str, time_wait=20):
        WebDriverWait(self.client, time_wait).until(EC.element_to_be_clickable((By.XPATH, xpath_str)))

    def ActionSendKeysXpathString(self, xpath_str, put_str):
        self.action = ActionChains(self.client)
        with suppress(Exception):
            self.action.move_to_element(self.f_el)
        self.f_el = self.client.find_element_by_xpath(xpath_str)

        self.action.move_to_element(self.f_el)
        self.action.click()
        self.action.send_keys_to_element(self.f_el, put_str)

        self.action.perform()

    def ActionFindAndClickByXpathStringAndVerifyLi(self, xpath_str, verify_str):
        self.action = ActionChains(self.client)
        with suppress(Exception):
            self.action.move_to_element(self.f_el)
        self.f_els = self.client.find_elements_by_xpath(xpath_str)
        for self.f_el in self.f_els:
            if self.f_el.text == verify_str:
                self.client.execute_script("arguments[0].scrollIntoView();", self.f_el)
                self.action.move_to_element(self.f_el)
                self.action.click()
                break

        self.action.perform()

    def UploadFileDragDropByXpathString(self, xpath_str, file_name):
        self.JS_DROP_FILE = """
            var target = arguments[0],
                offsetX = arguments[1],
                offsetY = arguments[2],
                document = target.ownerDocument || document,
                window = document.defaultView || window;

            var input = document.createElement('INPUT');
            input.type = 'file';
            input.onchange = function () {
              var rect = target.getBoundingClientRect(),
                  x = rect.left + (offsetX || (rect.width >> 1)),
                  y = rect.top + (offsetY || (rect.height >> 1)),
                  dataTransfer = { files: this.files };

              ['dragenter', 'dragover', 'drop'].forEach(function (name) {
                var evt = document.createEvent('MouseEvent');
                evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
                evt.dataTransfer = dataTransfer;
                target.dispatchEvent(evt);
              });

              setTimeout(function () { document.body.removeChild(input); }, 25);
            };
            document.body.appendChild(input);
            return input;
        """
        self.f_el = self.client.find_element_by_xpath(xpath_str)
        self.hz = self.f_el.parent
        self.file_input = self.hz.execute_script(self.JS_DROP_FILE, self.f_el, 0, 0)
        self.file_input.send_keys(f'{os.path.abspath(sys.argv[0] + "/..")}/{file_name}')

    def ByPassInvisibleCapthca(self, xpath_str, solve_captcha):
        self.action = ActionChains(self.client)
        self.f_el = self.client.find_element_by_xpath(xpath_str)
        self.client.execute_script(
            f'arguments[0].innerHTML="<input type=\\"submit\\"><textarea name=\\"g-recaptcha-response\\">{solve_captcha}</textarea>;"', self.f_el
        )
        self.f_el_click = self.f_el.find_element_by_xpath("//input[@type='submit']")

        self.client.execute_script("arguments[0].scrollIntoView();", self.f_el_click)
        self.action.move_to_element(self.f_el_click)
        self.action.click()
        self.action.perform()