import json
from typing import Union

from lib.node.node_parser import NodeParser
from lib.schema.schema import Schema


class LibApi:
    schema = Schema()
    node_parser = NodeParser

    @classmethod
    def parse(cls, query, is_json=False, from_path=False):
        if from_path:
            cls._check_file_extension(file_path=query, extension='json')
            with open(query) as f:
                query = json.load(f)
        if is_json:
            query = json.load(query)
        if not is_json and not from_path:
            cls._check_type(query, dict, 'query')
        nodes = query.get('nodes')
        edges = query.get('edges')
        if not nodes or not edges:
            raise ValueError('`nodes` and `edges` must not be `None`')
        return cls.node_parser.parse(nodes, edges)

    @classmethod
    def add_schema(cls, schema: str):
        cls._check_type(schema, str, 'schema')
        schema_name = cls.schema.set(schema)
        if schema_name:
            print('Schema `{}` has been added succesfully.'.format(schema_name))
            return True

    @classmethod
    def remove_schema(cls, schema_name: str):
        cls._check_type(schema_name, str, 'schema_name')
        if cls.schema.rm(schema_name):
            print('Schema `{}` has been deleted succesfully.'.format(schema_name))
            return True


    @classmethod
    def _check_file_extension(cls, file_path: str, extension: Union[str, list]):
        if isinstance(extension, str):
            extension = [extension]
        cls._check_type(extension, list, 'extension')
        file_extension = file_path.split('.')[-1]
        if file_extension not in extension:
            raise TypeError('File extension must be `.json`, received `.{}` instead'.format(file_extension))

    @classmethod
    def _check_type(cls, obj: object, class_, name: str):
        if not isinstance(obj, class_):
            raise TypeError('Type of `{}` must be `{}`, received `{}` instead'.format(name, class_, type(obj)))
