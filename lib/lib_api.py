from lib.node.node_parser import NodeParser
from lib.schema.schema import Schema


class LibApi:
    schema = Schema()
    node_parser = NodeParser

    @classmethod
    def parse(cls, query):
        if not isinstance(query, dict):
            raise TypeError('Type of `query` must be `dict`, received `{}` instead'.format(type(query)))
        nodes = query.get('nodes')
        edges = query.get('edges')
        if not nodes or not edges:
            raise ValueError('`nodes` and `edges` must not be `None`')
        return cls.node_parser.parse(nodes, edges)
