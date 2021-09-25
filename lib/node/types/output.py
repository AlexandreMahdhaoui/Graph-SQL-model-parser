from lib.node.node_type import NodeType


class Output(NodeType):
    context_0 = 'In `Output`\'s NodeType class.'
    context_1 = 'In transformObject'
    allowed_items = {
        'limit': [int],
        'offset': [int]
    }

    @classmethod
    def resolve(cls, transform_object, __origin_schema__, *args, **kwargs) -> str:
        cls._check_transf_obj_type(transform_object)
        str_list = list()
        for k, v in transform_object.items():
            cls._validate_items(k, v)
            str_list.extend([k, repr(v)])
        return ' '.join(str_list)

    @classmethod
    def _validate_items(cls, keyword, value):
        type_ = cls.allowed_items.get(keyword)
        if not type_:
            raise ValueError('Keyword `{}` is not a valid key for `cls.allowed_items` dictionary'.format(keyword),
                             cls.context_0)
        if not type(value) in type_:
            raise ValueError('Type of value `{}` of keyword `{}` must be in `{}`.'.format(value, keyword, type_),
                             'Received type `{}` instead.'.format(type(value)),
                             cls.context_0)

    @classmethod
    def _check_transf_obj_type(cls, transform_object):
        if not isinstance(transform_object, dict):
            raise TypeError('Type of `transform_object` must be `dict`, received `{}` instead.'.format(type(transform_object)),
                            cls.context_0)
