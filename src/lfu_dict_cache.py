# ./src/lfu_dict_cache.py

from typing import Generic, Iterator, TypeAlias
from sortedcontainers import SortedDict

from .types import K, V
from .dict_cache import DictCache

Freq: TypeAlias = int
LruCache: TypeAlias = DictCache[K, None]
FreqToLru: TypeAlias = SortedDict[Freq, LruCache]  # type:ignore


class LfuDictCache(Generic[K, V]):
    """
    LFU (Least Frequently Used) cache with LRU tie-breaking.

    This cache maintains a limited number of key-value pairs.

    When the maximum size is exceeded, it evicts the key with the lowest
    access frequency.

    If multiple keys share the same frequency, the least recently used (LRU)
    among them is evicted.

    Attributes:
        _max_size (int): Maximum number of items in the cache.
        _values (dict[K, V]): Dictionary storing the actual key-value pairs.
        _freq (dict[K, int]): Dictionary storing the access frequency of
                              each key.
        _freq_to_lru (SortedDict[Freq, LruCache]): Maps each frequency to
                                                   an LRU cache of keys with
                                                   that frequency.
    """

    def __init__(self, max_size: int):
        """
        Initializes the LFU cache.

        Args:
            max_size (int): Maximum number of items the cache can hold.
                            If set to 0, the cache does not store any items.

        Raises:
            ValueError: If `max_size` is negative.
        """
        if max_size < 0:
            raise ValueError("max_size cannot be negative")
        self._max_size: int = max_size
        self._values: dict[K, V] = {}
        self._freq: dict[K, int] = {}
        self._freq_to_lru: FreqToLru = SortedDict()

    # ---------- internal helpers ----------
    def _remove_key(self, key: K) -> None:
        """
        Removes a key from cache, frequency dict, and corresponding LRU.

        Args:
            key (K): Key to remove.

        Raises:
            KeyError: If key is not present in cache.
        """
        freq = self._freq[key]
        lru = self._freq_to_lru[freq]

        del self._values[key]
        del self._freq[key]
        del lru[key]
        self._clean_freq_bucket(lru, freq)

    def _add_key_to_freq(self, key: K, freq: Freq) -> None:
        """
        Adds a key to a frequency bucket, creating it if missing.

        Args:
            key (K): Key to add.
            freq (int): Frequency bucket to add key to.
        """
        if freq not in self._freq_to_lru:
            self._freq_to_lru[freq] = DictCache(self._max_size)
        self._freq_to_lru[freq][key] = None

    def _evict(self) -> None:
        """
        Evicts the least frequently used key. Ties are broken using LRU.
        """
        _, lru = self._freq_to_lru.peekitem(0)
        key = next(iter(lru))
        self._remove_key(key)

    def _increase_freq(self, key: K) -> None:
        """
        Increases frequency of a key by one and moves it to the new frequency
        bucket.

        Args:
            key (K): Key to update.
        """
        old_freq = self._freq[key]
        new_freq = old_freq + 1

        old_lru = self._get_lru(old_freq)
        del old_lru[key]
        self._clean_freq_bucket(old_lru, old_freq)

        self._add_key_to_freq(key, new_freq)
        self._freq[key] = new_freq

    def _clean_freq_bucket(self, lru: LruCache, freq: Freq) -> None:
        """
        Removes a frequency bucket if it is empty.

        Args:
            lru (LruCache): The LRU cache corresponding to the frequency.
            freq (int): The frequency of the bucket.
        """
        if len(lru) == 0:
            del self._freq_to_lru[freq]

    def _is_full(self) -> bool:
        """
        Checks whether the cache has reached its maximum size.

        Returns:
            bool: True if cache is full, False otherwise.
        """
        full: bool = len(self._values) >= self._max_size
        return full

    def _set_value(self, key: K, value: V) -> None:
        """
        Sets or updates the value for a key in the cache without changing
        its frequency.

        Args:
            key (K): Key to insert or update.
            value (V): Value associated with the key.
        """
        self._values[key] = value

    def _ensure_freq_bucket(self, freq: Freq) -> None:
        """
        Ensures that a frequency bucket exists for the given frequency.

        If the bucket does not exist, it creates a new LRU cache for
        that frequency.

        Args:
            freq (int): Frequency to ensure.
        """
        if freq not in self._freq_to_lru:
            self._freq_to_lru[freq] = DictCache(self._max_size)

    def _get_lru(self, freq: Freq) -> LruCache:
        """
        Retrieves the LRU cache corresponding to a given frequency.

        Args:
            freq (int): The frequency for which to get the LRU cache.

        Returns:
            LruCache: The LRU cache containing keys with the specified
                      frequency.

        Raises:
            KeyError: If there is no LRU cache for the given frequency.
        """
        return self._freq_to_lru[freq]

    # ---------- dict-like API ----------

    def __getitem__(self, key: K) -> V:
        """
        Retrieves the value associated with the key and updates its frequency.

        Args:
            key (K): Key to retrieve.

        Returns:
            V: Value associated with the key.

        Raises:
            KeyError: If the key does not exist in the cache.
        """
        try:
            value: V = self._values[key]
        except KeyError:
            raise
        self._increase_freq(key)
        return value

    def __setitem__(self, key: K, value: V) -> None:
        """
        Inserts or updates the key-value pair in the cache.

        If the key already exists, its value is updated and frequency
        increased.

        If the key is new and the cache is full, the LFU/LRU eviction policy
        is applied.

        Args:
            key (K): Key to insert or update.
            value (V): Value associated with the key.
        """
        if self._max_size == 0:
            return

        if key in self._values:
            self._set_value(key, value)
            self._increase_freq(key)
        else:
            if self._is_full():
                self._evict()
            self._set_value(key, value)
            self._freq[key] = 1
            self._add_key_to_freq(key, 1)

    def __delitem__(self, key: K) -> None:
        """
        Deletes a key-value pair from the cache.

        Args:
            key (K): Key to delete.

        Raises:
            KeyError: If the key does not exist.
        """
        try:
            self._remove_key(key)
        except KeyError:
            raise

    def __iter__(self) -> Iterator[K]:
        """
        Returns an iterator over the keys in the cache.

        Returns:
            Iterator[K]: Iterator over keys in insertion order.
        """
        keys: Iterator[K] = iter(self._values)
        return keys

    def __len__(self) -> int:
        """
        Returns the number of items currently stored in the cache.

        Returns:
            int: Number of items.
        """
        length: int = len(self._values)
        return length
