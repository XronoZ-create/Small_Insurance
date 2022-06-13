from seleniumwire import webdriver as wire
from selenium import webdriver as selen
from datetime import datetime
import time
from .proxy_selen import create_proxy as cp

class selenium_client():
    def __init__(self, proxy=None, headless=False, selenwire = False):
        if selenwire == False:
            self.chrome_options = selen.ChromeOptions()
        else:
            self.chrome_options = wire.ChromeOptions()
        if headless:
            self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_argument("--remote-debugging-port=9222")

        if proxy != None:
            self.proxy_split = proxy.split(':')
            self.proxy_options = {
                'proxy': {
                    'https': 'https://%s:%s@%s:%s' % (proxy[2], proxy[3], proxy[0], proxy[1]),
                }
            }
            self.pluginfile = cp(proxy)
            self.chrome_options.add_extension(self.pluginfile)

        if selenwire == False:
            self.client = selen.Chrome(options=self.chrome_options)
        else:
            self.client = wire.Chrome(options=self.chrome_options)


    def open_url(self, url):
        self.client.get(url)
        return self.client.page_source

    def get_cookies(self):
        """
        Функция получения куки selenium-а в виде словаря
        :return: dict{'name':'value'}
        """

        self.cookies_list = self.client.get_cookies()
        self.cookies_dict = {}
        for self.cookie in self.cookies_list:
            self.cookies_dict[self.cookie['name']] = self.cookie['value']
        print(self.cookies_dict)
        return self.cookies_dict

    def dict_cookies_to_browser(self, dict_cookies):
        for self.name, self.value in dict_cookies.items():
            self.client.add_cookie({'name':self.name, 'value':self.value})

        self.client.get_cookies()

    def get_htmlpage(self):
        return self.client.page_source

    def quit_browser(self):
        self.client.quit()

    def save_screenshot(self):
        self.now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.client.get_screenshot_as_file('error-screenshot-%s.png' % self.now)

    def save_page(self):
        self.now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        with open(f'error-page-{self.now}.html', 'w') as self.f:
            self.f.write(self.client.page_source)

    def get_last_headers(self, path):
        for self.request in self.client.requests:
            if self.request.path == path:
                return self.request.headers