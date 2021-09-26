import json
import os
import re

from lib.utils.singleton import Singleton


class Schema(metaclass=Singleton):
    _path = os.path.join('lib', 'data', 'schema_definitions.json')
    _pattern = '(?<=({})).+?(?={})'
    _type_converter = {
        'str': str,
        'int': int,
        'float': float,
        'complex': complex
    }

    def __init__(self):
        self._get_typing_ref()
        data = self._load()
        for k, v in data.items():
            self.__setattr__(k, self._parse_schema(v))

    def get(self, item: str, default=None):
        return self._dict().get(item, default=default)

    def set(self, schema):
        data = self._load()
        table_name = self._get_table_name(schema)
        data[table_name] = schema
        self.__setattr__(table_name, self._parse_schema(schema))
        self._dump_and_save(data)
        return table_name

    def rm(self, schema_name):
        data = self._load()
        if data.pop(schema_name):
            self._dump_and_save(data)
            return schema_name

    def _load(self):
        with open(self._path) as f:
            return json.load(f)

    def _dump_and_save(self, dict_: dict):
        self._check_type(dict_, dict, 'dict_')
        with open(self._path, 'w') as f:
            json.dump(dict_, f)

    def _get_table_name(self, schema) -> str:
        pattern = self._pattern.format('CREATE TABLE `', '`')
        match = re.search(pattern, schema)
        if not match:
            raise NameError('Name of the table cannot be parsed from schema: \n {}'.format(schema))
        return match.group()

    def _parse_schema(self, schema: str) -> dict:
        lines = schema.split('\n')
        parsed_schema = dict()
        for s in lines:
            name, typing = self._get_field_name(s), self._get_field_typing(s)
            if name and typing:
                typing_ = self._typing_ref['sql_to_py'].get(typing)
                if not typing_:
                    raise TypeError('type `{}` of field `{}` cannot be interpreted'.format(typing, name))
                parsed_schema[name] = typing_
        return parsed_schema

    def _get_field_name(self, s: str):
        return self._get_regex_match(self._pattern.format('`', '`'), s)

    def _get_field_typing(self, s: str):
        return self._get_regex_match(r'(?<=(`)(\ |\t)).+?(?=(\()|\ )', s)

    def _get_regex_match(self, pattern: str, s: str):
        match = re.search(pattern, s)
        if match:
            return match.group().strip()

    def _get_typing_ref(self):
        with open(os.path.join('lib', 'data', 'typing_ref.json')) as f:
            data = json.load(f)
            data['sql_to_py'] = self._convert_to_type(data['sql_to_py'])
        self._typing_ref = data

    def _convert_to_type(self, dict_):
        return {k: self._type_converter.get(v) for k, v in dict_.items()}

    def __getitem__(self, item: str):
        return self._dict()[item]

    def _dict(self):
        """
        :return: Dictionary of `cls`'s attributes
        """
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    @classmethod
    def _check_type(cls, obj: object, class_, name: str):
        if not isinstance(obj, class_):
            raise TypeError('Type of `{}` must be `{}`, received `{}` instead'.format(name, class_, type(obj)))
