from lib.node.node_type import NodeType


class Sort(NodeType):
    OPERATOR = 'ORDER BY'
    context_0 = 'In `Sort`\'s NodeType class.'
    context_1 = 'In transformObject'

    @classmethod
    def resolve(cls, transform_object, __origin_schema__, *args, **kwargs) -> str:
        cls._check_transf_obj_type(transform_object)
        str_list = list()
        for x in transform_object:
            target = x.get('target')
            order = x.get('order')
            cls._check_exist(target, order)
            cls.validate(schema=__origin_schema__, field_name=target, context=cls.context_0)
            str_list.append(
                '`{}` {}'.format(target, order)
            )
        return ' '.join([cls.OPERATOR, ', '.join(str_list)])

    @classmethod
    def _check_transf_obj_type(cls, transform_object):
        if not isinstance(transform_object, list):
            raise TypeError('Type of `transform_object` must be `list`, received `{}` instead.'.format(type(transform_object)),
                            cls.context_0)

    @classmethod
    def _check_exist(cls, target, order):
        if not target or not order:
            raise ValueError('`target` and `order` must not be `None`',
                             'Received target={}, order={} instead.'.format(target, order),
                             cls.context_1,
                             cls.context_0)
