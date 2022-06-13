import json

class GetVehicleJson:
    def __init__(self, id_vehicle=None):
        if id_vehicle == None:
            self.json = {"method":"getVehicles"}
        else:
            self.json = {
                "id": id_vehicle,
                "isSlingshot": 0,
                "method": "getVehicle"
            }

    def __call__(self, *args, **kwargs):
        return json.dumps(self.json)