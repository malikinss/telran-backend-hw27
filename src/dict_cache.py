# ./src/dict_cache.py

from collections import OrderedDict
from .types import K, V


class DictCache(OrderedDict[K, V]):
    def __init__(self, maxsize=128):
        super().__init__()
        self.maxsize = maxsize
    # The  methods __getitem__ and __setitem__ should be overriden
    # Assumption: only following methods should be overriden for making tests
    # from test_dict_cache.py passed4

    # Hints as follows:
    # super().__getitem__(key) calls method __getitem__ of OrderedDict
    # super().__setitem__(key, value) calls method __setitem__ of OrderedDict
    # consider using self.move_to_end(key) of OrderedDict for making item with
    # the given key as most recent
    # consider using self.popitem(last=False) for removing least
    # recent (eldest item)

    def __getitem__(self, key) -> V:
        res = super().__getitem__(key)
        self.move_to_end(key)
        return res

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)

        if len(self) > self.maxsize:
            self.popitem(last=False)
