class StringConverter:
    @classmethod
    def snake_to_pascal(cls, str_: str):
        if not isinstance(str_, str):
            raise TypeError('Type must be str')
        l_ = str_.split('_')
        return ''.join(s.title() for s in l_)
