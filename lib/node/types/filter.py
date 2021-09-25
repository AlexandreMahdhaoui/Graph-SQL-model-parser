from lib.node.node_type import NodeType


class Filter(NodeType):
    OPERATOR = 'WHERE'
    context_0 = 'In `Filter`\'s NodeType class.'
    context_1 = 'In `transformObject`'
    context_2 = 'In `operations`'

    @classmethod
    def resolve(cls, transform_object, __origin_schema__, *args, **kwargs) -> str:
        var_fields = transform_object.get('var_fields')
        ope = transform_object.get('operations')
        join_operator = ' {} '.format(transform_object.get('joinOperator'))

        cls._check_exist(var_fields, ope, join_operator)
        cls._check_len(var_fields, ope)

        str_list = list()
        for f, o in zip(var_fields, ope):
            o_, v = o.get('operator'), o.get('value')
            cls._check_nested(o_, v)
            cls.validate(schema=__origin_schema__, field_name=f, context=cls.context_0)
            str_list.append(
                '`{}` {} {}'.format(f, o_, v)
            )
        return ' '.join([cls.OPERATOR, join_operator.join(str_list)])

    @classmethod
    def _check_nested(cls, o_, v):
        if not o_ or not v:
            raise ValueError('`operator` and `value` must not be `None`,', cls.context_2, cls.context_1, cls.context_0)

    @classmethod
    def _check_len(cls, var_fields, ope):
        if not var_fields.__len__() == ope.__len__():
            raise ValueError('length of `var_fields` and `operations` must be equal', cls.context_1, cls.context_0)

    @classmethod
    def _check_exist(cls, var_fields, ope, join_operator):
        if not var_fields or not ope or not join_operator:
            raise ValueError('`var_fields`, `operations` and `joinOperator` must not be `None`. \n Received: \n',
                             'var_fields: {}'.format(var_fields),
                             'operations: {}'.format(ope),
                             'joinOperator: {}'.format(join_operator),
                             cls.context_0)