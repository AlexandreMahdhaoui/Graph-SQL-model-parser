import json
import os
import re
from typing import Tuple

from lib.utils.singleton import Singleton


class Schema(metaclass=Singleton):
    _pattern = '(?<=({})).+?(?={})'

    def __init__(self):
        self._get_typing_ref()
        with open(os.path.join('lib', 'data', 'schema_definitions.json')) as f:
            data = json.load(f)
        for k, v in data.items():
            self.__setattr__(k, self._parse_schema(v))
        print(self._dict())

    def get_table_name(self, schema) -> str:
        pattern = self._pattern.format('CREATE TABLE `', '`')
        match = re.search(pattern, schema)
        if match:
            return match.group()

    def _parse_schema(self, schema: str):
        lines = schema.split('\n')
        i, table_name = self._get_table_name(lines)
        return self._get_parsed_schema(lines[i:])

    def _get_table_name(self, lines) -> Tuple[int, str]:
        pattern = self._pattern.format('CREATE TABLE `', '`')
        for i, s in enumerate(lines):
            match = re.search(pattern, s)
            if match:
                return i, match.group()

    def _get_parsed_schema(self, lines: list) -> dict:
        parsed_schema = dict()
        for s in lines:
            name, typing = self._get_field_name(s), self._get_field_typing(s)
            if name and typing:
                typing_ = self._typing_ref['sql_to_py'].get(typing)
                if not typing_:
                    raise TypeError('type `{}` of field `{}` cannot be interpreted'.format(name, typing))
                parsed_schema[name] = typing_
        return parsed_schema

    def _get_field_name(self, s: str):
        return self._get_regex_match(s, self._pattern.format('`', '`'))

    def _get_field_typing(self, s: str):
        return self._get_regex_match(s, r'(?<=(`)(\ |\t)).+?(?=(\()|\ )')

    def _get_regex_match(self, s: str, p: str):
        match = re.match(p, s)
        return match.group().strip() if match else None

    def _get_typing_ref(self):
        with open(os.path.join('lib', 'data', 'typing_ref.json')) as f:
            data = json.load(f)
        self._typing_ref = data

    def __getitem__(self, item: str):
        return self._dict()[item]

    def get(self, item: str, default=None):
        return self._dict().get(item, default=default)

    def _dict(self):
        """
        :return: Dictionary of `cls`'s attributes
        """
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}