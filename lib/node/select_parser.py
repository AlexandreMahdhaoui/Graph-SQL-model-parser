from typing import Union


class SelectParser:
    t = "`{}`"
    nt = t + ","
    kw = ["SELECT", "FROM"]

    @classmethod
    def parse(cls, fields: Union[list, str], origin: str):
        return " ".join([
            cls.kw[0],
            cls._parse_fields(fields),
            cls.kw[1],
            cls.t.format(origin)])

    @classmethod
    def _parse_fields(cls, fields: Union[list, str]):
        if fields == '*':
            return fields
        if isinstance(fields, list):
            return " ".join([cls.nt.format(x) for x in fields[:-1]]) + " " + cls.t.format(fields[-1])
        raise TypeError('Type of fields must be list or str equal to \'*\'')
