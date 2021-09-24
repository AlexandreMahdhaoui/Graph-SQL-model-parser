from abc import ABC
from typing import Union, List, Tuple

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
    FieldsType = Union[List[str], str]

    @classmethod
    def parse(cls, fields: FieldsType, origin: str, *args, **kwargs) -> str:
        """
        Method called by NodeParser to parse a specific type of node.\n
        Specific types manipulating the SELECT attributes. (e.g.: TextTransformation)
            - Replace `cls.parse()`\n
            - Use `cls._parse()` to get the proper `SELECT x FROM y OTHER z` block\n
            - Use `cls._select()` to get only the `SELECT x FROM y` block

            Example:\n
            class TextTransformation(NodeType):
                template = '{}({}) as {}'\n
                @classmethod \n
                def parse(cls, fields, origin, *args, **kwargs):
                    s = cls._select(fields, origin)\n
                    if kwargs.get('transformObject'):
                        for x in kwargs['transformObject']:
                            c, t = x['column'], x['transformation'] \n
                            re.sub(c, cls.template.format([t, c, c]), s)
                    return s


        :param fields:
        :param origin:
        :param args:
        :param kwargs:
        :return: Whole parsed node type
        """
        return cls._parse(fields, origin, *args, **kwargs)

    @classmethod
    def _parse(cls, fields: FieldsType, origin: str, *args, **kwargs) -> str:
        return cls._join((cls._select(fields, origin), cls.resolve(*args, **kwargs)))

    @classmethod
    def _select(cls, fields: FieldsType, origin: str):
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
