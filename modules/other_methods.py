import requests
import time

def check_ip():
    while True:
        r = requests.get('http://myip.dnsomatic.com')
        if r.status_code == 200:
            return r.text
        time.sleep(2)