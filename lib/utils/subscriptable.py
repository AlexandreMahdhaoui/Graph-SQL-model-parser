from abc import ABC


class Subscriptable(ABC):
    _child_dict: dict = None

    def __getitem__(self, item: str):
        return self._get_child_dict()[item]

    def get(self, item: str, default=None):
        return self._get_child_dict().get(item, default=default)

    @classmethod
    def _get_child_dict(cls):
        """
        :return: Dictionary of `cls`'s attributes
        """
        if not cls._child_dict:
            cls._child_dict = {k: v for k, v in cls.__dict__.items() if not k.startswith('_')}
        return cls._child_dict

