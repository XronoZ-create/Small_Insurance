class ConfigDevelopment:
    guru_captcha_api_key = ""
    anticaptcha_captcha_api_key = ""

    vak_sms_api_key = ""
    online_sim_api_key = ""
    activate_sms_api_key = ""

    site_address = "http://127.0.0.1:5000/"
    API_KEY = ""

    proxies = None

    token_dadata = ""

    selenium_version = 101

class ConfigDeploy:
    guru_captcha_api_key = ""
    anticaptcha_captcha_api_key = ""

    vak_sms_api_key = ""
    online_sim_api_key = ""

    site_address = "http://"
    API_KEY = ""

    proxies = {
        'http': f'https://qHqZaXna:CR3YrX6t@212.192.168.116:58338',
        'https': f'https://qHqZaXna:CR3YrX6t@212.192.168.116:58338',
    }

    token_dadata = ""

    selenium_version = 100


class Config(ConfigDeploy):
    pass

