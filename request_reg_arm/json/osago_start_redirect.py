import json

class OsagoStartRedirectJson:
    def __init__(self, draft_id):
        self.json = {"draftId": draft_id, "method": "selectionOsagoStartRedirect"}

    def __call__(self, *args, **kwargs):
        return json.dumps(self.json)