import re
from typing import Dict, Union, List, Tuple

from lib.node.node_type import NodeType


class TextTransformation(NodeType):
    context_0 = 'In `TextTransformation`\'s NodeType class.'
    context_1 = 'In `transformObject`,'
    SchemaType = Dict[str, Union[List[str], str]]
    template = '{}(`{}`) as `{}`'
    allowed_types = [str]

    @classmethod
    def parse(cls, origin_node, origin_schema: SchemaType, *args, **kwargs) -> Tuple[SchemaType, str]:
        str_ = cls._select(origin=origin_node, fields=[k for k in origin_schema.keys()])

        transform_object = kwargs.get('transformObject')
        cls._check_transform_object(transform_object)

        for x in transform_object:
            c, t = x.get('column'), x.get('transformation')
            cls._check_nested_exist(c, t)
            cls.validate(origin_schema, c, cls.allowed_types, context=cls.context_0)
            fixed_column_pattern = '`{}`'.format(c)
            str_ = re.sub(fixed_column_pattern, cls.template.format(t, c, c), str_)
        schema = cls._compute_schema(origin_schema, fields=kwargs.get('fields'))
        return schema, str_

    @classmethod
    def _check_nested_exist(cls, c, t):
        if not c or not t:
            raise ValueError('`column` and `transformation` must not be `None`.',
                             'received column={} and transformation={} instead.'.format(c, t),
                             cls.context_1,
                             cls.context_0)

