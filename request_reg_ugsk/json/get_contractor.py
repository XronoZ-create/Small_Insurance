import json

class GetContractorJson:
    """
      {'data': [{'value': 'PersAreaCont_c3ed8fa4-26e6-491f-9a5c-914d70676349',
       'text': 'Вы Выв Вывыв',
       'status': 'ФизЛицо'},
      {'value': 'PersAreaCont_6b639176-7c3d-4336-82e8-d94777e7c093',
       'text': 'Иван Иванов Иванович',
       'status': 'ФизЛицо'},
      {'value': 'PersAreaCont_e2d8be7d-2e5e-4469-a728-03cb016cc996',
       'text': 'Иванов Иван Ивановчи',
       'status': 'ФизЛицо'}],
     'error': 0}
    """
    def __init__(self, id_contractor=None):
        if id_contractor == None:
            self.json = {
                "method":"getContractors"
            }
        else:
            self.json = {
                "id": id_contractor,
                "isSlingshot": 0,
                "method": "getContractor"
            }
    def __call__(self, *args, **kwargs):
        return json.dumps(self.json)