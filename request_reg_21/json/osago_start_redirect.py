import json

class OsagoStartRedirectJson:
    def __init__(self, draft_id, api_key):
        self.json = {"api_key": api_key, "draftId": draft_id, "method": "selectionOsagoStartRedirect"}

    def __call__(self, *args, **kwargs):
        return json.dumps(self.json)