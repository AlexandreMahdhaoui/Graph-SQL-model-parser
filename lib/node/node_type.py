from abc import ABC
from typing import Union, List, Tuple, Dict, Any

from lib.node.select_parser import SelectParser


class NodeType(ABC):
    """
    Superclass used to create NODE_TYPE parsers.

    Example:
        class Filter(NodeType):
            @classmethod \n
            def resolve(cls):
                pass

    """
    SchemaType = Dict[str, Union[List[str], str]]

    @classmethod
    def parse(cls, origin_node: str, origin_schema: SchemaType, *args, **kwargs) -> tuple[str, Union[dict, Any]]:
        """
        Method called by NodeParser to parse a specific type of node.\n
        Specific node_types manipulating the SELECT attributes of SQL queries (e.g.: TextTransformation) have different
        way to implement their transformations by replacing this `cls.parse()` method.
            - Use `cls._select()` to get the proper `SELECT x FROM y` block\n
            - Use `cls._parse()` to get the whole `SELECT x FROM y OTHER z` block\n
            Example:\n
            class TextTransformation(NodeType):
                template = '{}({}) as {}'\n
                @classmethod \n
                def parse(cls, origin_node, origin_fields, *args, **kwargs):
                    str_ = cls._select(origin_fields, origin)\n
                    if kwargs.get('transformObject'):
                        for x in kwargs['transformObject']:
                            c, t = x['column'], x['transformation'] \n
                            re.sub(c, cls.template.format([t, c, c]), str_)
                    schema = cls._compute_schema(origin_schema, fields=kwargs.get('fields'))
                    return str_, schema
        :param origin_schema:
        :param origin_node:
        :param args:
        :param kwargs:
        :return: Whole parsed node type
        """
        schema = cls._compute_schema(origin_schema, fields=kwargs.get('fields'))
        return cls._parse(origin_node, schema, *args, **kwargs), schema

    @classmethod
    def _compute_schema(cls, origin_schema, fields=None):
        """
        returns selected fields from origin schema, otherwise origin_schema if no fields have been specified
        """
        if fields:
            if not isinstance(fields, list):
                raise TypeError('\'fields\' must be of type \'list\', type {} was given instead.'.format(type(fields)))
            return {k: v for k, v in origin_schema.items() if k in fields}
        return origin_schema

    @classmethod
    def _parse(cls, origin_node: str, schema: SchemaType, *args, **kwargs) -> str:
        fields = [k for k in schema.keys()]
        return cls._join((cls._select(fields, origin_node), cls.resolve(*args, **kwargs)))

    @classmethod
    def _select(cls, fields: Union[List[str], str], origin: str):
        return SelectParser.parse(fields, origin)

    @classmethod
    def _join(cls, tuple_: Tuple[str, Union[str, None]]):
        if not tuple_[1]:
            return tuple_[0]
        return " ".join(tuple_)

    @classmethod
    def resolve(cls, *args, **kwargs) -> str:
        """
        Must implements the parsing stage of the NODE_TYPE
        Must be replaced in children of NodeType
        :param args:
        :param kwargs:
        :return: Parsed node_type
        """
        pass
