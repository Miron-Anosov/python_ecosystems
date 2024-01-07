import json
from dataclasses import dataclass


@dataclass
class JsonWorker:
    data_json: str

    def get_dict(self):
        return json.loads(self.data_json)


def read_json(data_json):
    return JsonWorker(data_json).get_dict()
