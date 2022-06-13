from urllib.parse import urlencode, parse_qs, parse_qsl


class InitPay:
    def __init__(self, calculation_id, order_id):
        self.data = {
            "id": calculation_id,
            "prod": "OSAGO",
            "orderId": order_id,
            "partnerChannel": "",
            "partnerManagerId": "",
            "vers": "EOSAGO",
            "ajax": "1",
            "code": "5",
            "paym_type": "5"
        }

    def __call__(self, *args, **kwargs):
        return urlencode(self.data)