from abc import ABC
from typing import Union, List, Tuple, Dict, Any

from lib.node.select_parser import SelectParser


class NodeType(ABC):
    """
    Superclass used to create NODE_TYPE parsers.

    Usage:
        class Filter(NodeType):
            @classmethod \n
            def resolve(cls, *args, **kwargs) -> str:
                origin_schema = kwargs.get('__schema__') \n
                var_fields = kwargs.get('var_fields') \n
                ope = kwargs.get('operations') \n
                join_operator = ' {} '.format(kwargs.get('joinOperator')) \n
                if var_fields and ope and join_operator:
                    if not var_fields.__len__() == ope.__len__():
                        raise ValueError('length of `var_fields` and `operations` must be equal')
                    conditions = list() \n
                    for f, o in zip(var_fields, ope):
                        o_, v = o.get('operator'), o.get('value') \n
                        if not o_ and not v:
                            raise ValueError('`operator` and `value` must not be `None`')
                        cls.validate(schema=origin_schema, field_name=f) \n
                        conditions.append(
                            '`{}` {} {}'.format(f, o_, v)
                        )
                    return join_operator.join(conditions)
                raise ValueError('`var_fields`, `operations` and `joinOperator` must not be `None`. Received:',
                                 'var_fields: {}'.format(var_fields), \n
                                 'operations: {}'.format(ope), \n
                                 'joinOperator: {}'.format(join_operator) \n
                                 )

    """
    SchemaType = Dict[str, Union[List[str], str]]
    context_0: str = 'NodeType'

    @classmethod
    def parse(cls, origin_node: str, origin_schema: SchemaType, *args, **kwargs) -> tuple[str, Union[dict, Any]]:
        """
        Method called by NodeParser to parse a specific type of node.\n
        Specific node_types manipulating the SELECT attributes of SQL queries (e.g.: TextTransformation) have different
        way to implement their transformations by replacing this `cls.parse()` method.
            - Use `cls._select()` to get the proper `SELECT x FROM y` block\n
            - Use `cls._parse()` to get the whole `SELECT x FROM y OTHER z` block\n
        Example:
            class TextTransformation(NodeType):
                SchemaType = Dict[str, Union[List[str], str]] \n
                template = '{}({}) as {}' \n
                allowed_types = [str]

                @classmethod \n
                def parse(cls, origin_node, origin_schema: SchemaType, *args, **kwargs):
                    str_ = cls._select(origin=origin_node, fields=[k for k in origin_schema.keys()]) \n
                    if kwargs.get('transformObject'):
                        for x in kwargs['transformObject']:
                            c, t = x.get('column'), x.get('transformation') \n
                            if c and t:
                                cls.validate(origin_schema, c, cls.allowed_types) \n
                                str_ = re.sub(c, cls.template.format([t, c, c]), str_)
                    schema = cls._compute_schema(origin_schema, fields=kwargs.get('fields')) \n
                    return str_, schema
        :param origin_schema: Dict[str, Union[List[str], str]]
        :param origin_node: str
        :param args:
        :param kwargs:
        :return: Whole parsed node type
        """
        schema = cls._compute_schema(origin_schema, fields=kwargs.get('fields'))
        return cls._parse(origin_node, schema, *args, **kwargs), schema

    @classmethod
    def validate(cls, schema: SchemaType, field_name: str, allowed_types: list = None, context: str = None):
        """
        Check if `field_name` exists in `schema`, then if allowed_types is defined checks
        if type of `schema['field_name']` is allowed.
        :param context:
        :param schema: Dict[str, Union[List[str], str]]
        :param field_name: str
        :param allowed_types: list
        :return:
        """
        if not schema.get(field_name):
            raise ValueError('Field `{}` does not exist in schema: \n {}'.format(field_name, schema))
        if allowed_types:
            if not schema.get(field_name) in allowed_types:
                raise TypeError('Type of field `{}` must be of type `{}` but type `{}` was given.'
                                .format(field_name, allowed_types, schema.get(field_name)),
                                'From schema: {}'.format(schema),
                                context)

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
        return cls._join((cls._select(origin_node, fields), cls._resolve(__schema__=schema, *args, **kwargs)))

    @classmethod
    def _select(cls, origin: str, fields: Union[List[str], str]):
        return SelectParser.parse(origin, fields)

    @classmethod
    def _join(cls, tuple_: Tuple[str, Union[str, None]]):
        if not tuple_[1]:
            return tuple_[0]
        return " ".join(tuple_)

    @classmethod
    def _resolve(cls, __schema__, *args, **kwargs):
        transform_object = kwargs.get('transformObject')
        cls._check_transform_object(transform_object)
        return cls.resolve(transform_object=transform_object, __schema__=__schema__, *args, **kwargs)

    @classmethod
    def resolve(cls, transform_object, __origin_schema__, *args, **kwargs) -> str:
        """
        Implements the parsing stage of the NODE_TYPE, must be replaced in children of NodeType

        Provides transform_object and __origin_schema__

        :param transform_object: dict
        :param __origin_schema__: dict
        :param args: *
        :param kwargs: **
        :return: Parsed string
        """
        pass

    @classmethod
    def _check_transform_object(cls, transform_object):
        """
        Check if `transform_object` is not None, raise ValueError if None
        :param transform_object:
        :return:
        """
        if not transform_object:
            raise ValueError('`transformObject` must not be `None`', cls.context_0)
