import json
from datetime import datetime, timedelta
from urllib.parse import quote, quote_plus

from request_reg_alfa.json.get_address import GetAddressJson

class SavePts:
    def __init__(self, client_data):
        self.registrationAddress = GetAddressJson(address=client_data.sobstv_pass_address)()
        self.data = {
            "stoaId": "",
            "submit_step3": ""
        }
        if client_data.pricep != "":
            self.data["WithUseTrailer"] = "Y"
        else:
            self.data["WithUseTrailer"] = "N"

        if client_data.type_document == 'ПТС':
            self.data['ptsType'] = '30'
            self.data['ptsSerial'] = client_data.ctc_ptc_seriya
            self.data['ptsNumber'] = client_data.ctc_ptc_number
            self.data['ptsDateIssue'] = datetime.strptime(client_data.ctc_ptc_vidach, "%Y-%m-%d").strftime("%d.%m.%Y")
        elif client_data.type_document == 'СТС':
            self.data['ptsType'] = '31'
            self.data['ptsSerial'] = client_data.ctc_ptc_seriya
            self.data['ptsNumber'] = client_data.ctc_ptc_number
            self.data['ptsDateIssue'] = datetime.strptime(client_data.ctc_ptc_vidach, "%Y-%m-%d").strftime("%d.%m.%Y")
        elif client_data.type_document == 'ЭПТС':
            self.data['ptsType'] = '41'
            self.data['ptsSerial'] = ""
            self.data['ptsNumber'] = client_data.ctc_ptc_number
            self.data['ptsDateIssue'] = datetime.strptime(client_data.ctc_ptc_vidach, "%Y-%m-%d").strftime("%d.%m.%Y")
        elif client_data.type_document == 'ПСМ':
            self.data['ptsType'] = '32'
            self.data['ptsSerial'] = client_data.ctc_ptc_seriya
            self.data['ptsNumber'] = client_data.ctc_ptc_number
            self.data['ptsDateIssue'] = datetime.strptime(client_data.ctc_ptc_vidach, "%Y-%m-%d").strftime("%d.%m.%Y")

    def __call__(self, *args, **kwargs):
        return self.data