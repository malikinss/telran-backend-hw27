# ./src/__init__.py

from .dict_cache import DictCache
from .lfu_dict_cache import LfuDictCache

__all__ = [
    'DictCache',
    'LfuDictCache'
]
