import re

from lib.node.node_type import NodeType


class TextTransformation(NodeType):
    template = '{}({}) as {}'

    @classmethod
    def parse(cls, origin_schema, origin_node, *args, **kwargs):
        s = cls._select(origin_schema, origin_node)
        if kwargs.get('transformObject'):
            for x in kwargs['transformObject']:
                c, t = x['column'], x['transformation']
                c = re.escape('`{}`'.format(c))
                re.sub(c, cls.template.format([t, c, c]), s)
        return s
