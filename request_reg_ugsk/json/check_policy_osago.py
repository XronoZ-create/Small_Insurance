import json
from datetime import datetime, timedelta

class CheckPolicyOsagoJson:
    def __init__(self, draft_id):
        self.json = {
            "draftId": draft_id,
            "method": "checkPolicyOsagoSaveStatus",
            "data": {
                "startLimitTimeAddOsago": int((datetime.now()-timedelta(minutes=1)).timestamp() * 1000)
            }
        }

    def __call__(self, *args, **kwargs):
        return json.dumps(self.json)