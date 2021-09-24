import json

from lib.utils.singleton import Singleton
from lib.utils.subscriptable import Subscriptable


class Schema(Subscriptable, metaclass=Singleton):
    def __init__(self):
        with open('/lib/data/schema_definitions.json') as f:
            data = json.load(f)
        for k, v in data.items():
            self.__setattr__(k, self._parse_schema(v))

    def _parse_schema(self, schema: str):
        pass
