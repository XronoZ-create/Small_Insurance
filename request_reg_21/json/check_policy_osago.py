import json
from datetime import datetime, timedelta

class CheckPolicyOsagoJson:
    def __init__(self, draft_id, api_key):
        self.json = {
            "api_key": api_key,
            "draftId": draft_id,
            "method": "checkPolicyOsagoSaveStatus",
            "data": {
                "startLimitTimeAddOsago": int((datetime.now()-timedelta(minutes=1)).timestamp() * 1000)
            }
        }

    def __call__(self, *args, **kwargs):
        return json.dumps(self.json)