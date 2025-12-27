# HW27: LFU Dictionary Cache

## Task Definition

Implement all methods marked with `TODO` in the class `LfuDictCache`.

`LfuDictCache` is a dictionary-like cache with a **limited capacity** that evicts
items according to the **LFU (Least Frequently Used)** strategy.

### Cache Eviction Policy

1. **LFU (Least Frequently Used)**

    - When the cache exceeds its maximum size, the key-value pair with the
      **lowest access frequency** must be removed.

2. **LRU tie-breaker**
    - If multiple keys have the same minimal frequency, the
      **least recently used** key among them must be evicted.

### Notes & Hints

-   LFU = _Least Frequently Used_
-   Access frequency must be incremented on:
    -   `__getitem__`
    -   updating an existing key via `__setitem__`
-   Consider using:
    -   `DictCache` class (see `main.py`)
    -   `SortedDict` from the `sortedcontainers` package for organizing frequencies
-   The implementation must pass **all tests from `test_lfu_dict_cache.py`**

### Provided Classes

#### DictCache

`DictCache` is a helper class based on `OrderedDict` that implements an **LRU cache**.
It automatically:

-   moves accessed keys to the most recent position
-   evicts the least recently used key when capacity is exceeded

You may use this class internally to resolve **LRU behavior** when LFU frequencies are equal.

### Class to Implement

```python
class LfuDictCache(Generic[K, V]):
```

### Constructor

```python
def __init__(self, max_size: int):
```

#### Requirements

-   Initialize an LFU cache with a maximum capacity `max_size`
-   Define and initialize all internal data structures required for:

    -   storing key-value pairs
    -   tracking access frequencies
    -   resolving LRU order when frequencies are equal

### Required Methods

1.  `__getitem__`

```python
def __getitem__(self, key: K) -> V:
```

-   Return the value associated with `key`
-   Increase the access frequency of the key
-   Update recency information (for LRU tie-break)
-   Raise `KeyError` if the key does not exist

---

2.  `__setitem__`

```python
def __setitem__(self, key: K, value: V):
```

-   If `key` already exists:
-   Update its value
-   Increase its access frequency
-   Update recency
-   If `key` is new:
    -   Insert it with initial frequency
    -   If insertion causes the cache to exceed `max_size`:
-   Evict one key according to LFU policy
-   Use LRU strategy when frequencies are equal

3. `__delitem__`

```python
def __delitem__(self, key: K):
```

-   Remove the key-value pair from the cache
-   Remove all associated metadata (frequency, recency)
-   Raise `KeyError` if the key does not exist

4. `__iter__`

```python
def __iter__(self) -> Iterator[K]:
```

-   Return an iterator over cache keys
-   Order is **arbitrary** (tests must not depend on ordering)

5. `__len__`

```python
def __len__(self) -> int:
```

-   Return the number of key-value pairs currently stored in the cache

### Behavioral Summary

| Operation      | Effect on Frequency | Effect on Recency |
| -------------- | ------------------- | ----------------- |
| `cache[key]`   | +1                  | updated           |
| `cache[key]=v` | +1 (if exists)      | updated           |
| new insertion  | initial frequency   | most recent       |
| eviction       | LFU → LRU tie-break | —                 |

### Constraints

-   The cache must behave like a dictionary
-   All magic methods (`__getitem__`, `__setitem__`, etc.) must work correctly
-   The implementation must pass all provided unit tests

### Goal

The goal of this assignment is to practice:

-   custom data structures
-   cache eviction strategies
-   combining LFU and LRU logic
-   correct usage of Python magic methods
-   working with ordered and sorted containers

## 📝 Description

## 🎯 Purpose

## 🔍 How It Works

## 📜 Output Example

## 📦 Usage

## 🧪 Running Tests

## ✅ Dependencies

## 🗂 Project Structure

## 📊 Project Status

## 📄 License

MIT License

---

## 🧮 Conclusion

---

Made with ❤️ and `Python` by **Sam-Shepsl Malikin** 🎓
© 2025 All rights reserved.
