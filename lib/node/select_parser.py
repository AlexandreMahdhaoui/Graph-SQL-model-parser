from typing import Union, List


class SelectParser:
    FieldsType = Union[List[str], str]
    t = "`{}`"
    nt = t + ","
    kw = ["SELECT", "FROM"]

    @classmethod
    def parse(cls, origin: str, fields: FieldsType):
        return " ".join([
            cls.kw[0],
            cls._parse_fields(fields),
            cls.kw[1],
            cls.t.format(origin)])

    @classmethod
    def _parse_fields(cls, fields: FieldsType):
        if fields == '*':
            return fields
        if not isinstance(fields, list):
            raise TypeError('Type of fields must be of type \'list\' or type \'str\' and \'fields\' == \'*\'')
        return " ".join([cls.nt.format(x) for x in fields[:-1]]) + " " + cls.t.format(fields[-1])
