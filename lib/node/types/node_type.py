from abc import ABC
from typing import Union

from lib.node.select_parser import SelectParser


class NodeType(ABC):
    """
    Superclass to create node types
    """

    @classmethod
    def parse(cls, fields: Union[list, str], origin: str, *args, **kwargs):
        """
        Method called by NodeParser to parse a specific NODE_TYPE
        :param fields:
        :param origin:
        :param args:
        :param kwargs:
        :return: Whole parsed node type
        """
        return " ".join([
            SelectParser.parse(fields, origin),
            cls.resolve(*args, **kwargs)
        ])

    @classmethod
    def resolve(cls, *args, **kwargs):
        """
        Must implements the parsing stage of the information related
        Must be replaced in children of NodeType
        :param args:
        :param kwargs:
        :return: Parsed node_type
        """
        pass


