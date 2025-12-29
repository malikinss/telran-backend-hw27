# HW27: LFU Dictionary Cache

## Task Definition

The goal of this homework is to implement a custom dictionary-like cache called `LfuDictCache` that:

-   Supports a **limited capacity**
-   Evicts items according to the **LFU (Least Frequently Used)** strategy
-   Uses **LRU (Least Recently Used)** as a tie-breaker when multiple items have the same frequency

You must implement all methods marked with `TODO` in the `LfuDictCache` class and ensure that it passes **all unit tests** provided in `test_lfu_dict_cache.py`.

### Cache Eviction Policy

1. **LFU (Least Frequently Used)**  
   The key-value pair with the **lowest access frequency** is evicted when the cache exceeds its maximum size.

2. **LRU Tie-Breaker**  
   If multiple keys have the same minimal frequency, the **least recently used key** among them will be removed first.

### Notes & Hints

-   Access frequency must be incremented on:
    -   `__getitem__` (key lookup)
    -   updating an existing key via `__setitem__`
-   Consider using:
    -   `DictCache` class (an LRU cache helper)
    -   `SortedDict` from the `sortedcontainers` package for organizing frequencies efficiently
-   All implemented methods must mimic dictionary behavior and pass the unit tests

---

## 📝 Description

`LfuDictCache` is a custom cache combining **LFU** and **LRU** strategies. It is designed for scenarios where:

-   Frequently accessed items should remain in memory
-   Less frequently used items should be evicted to free space
-   Among items with equal frequency, the least recently accessed one is evicted

This project demonstrates how to implement a sophisticated caching mechanism with Python's **magic methods**, while maintaining performance and correctness.

The key features of the cache include:

-   Dictionary-like interface with `__getitem__`, `__setitem__`, `__delitem__`, `__len__`, and `__iter__`
-   Automatic frequency tracking for all accesses
-   Integration of LRU logic to resolve ties when evicting items
-   Strict adherence to a maximum size for memory efficiency

---

## 🎯 Purpose

The main objectives of this homework are:

-   **Understand and implement custom data structures**
-   **Practice cache eviction strategies**, combining LFU and LRU
-   **Work with Python magic methods** (`__getitem__`, `__setitem__`, etc.)
-   **Use ordered and sorted containers** effectively (`OrderedDict`, `SortedDict`)
-   **Develop robust unit tests** to ensure correctness of complex behavior

By completing this task, you will gain practical experience in designing efficient caching systems suitable for performance-critical applications.

---

## 🔍 How It Works

### 1. Initialization

The cache is initialized with a maximum size and internal data structures for:

-   Storing key-value pairs
-   Tracking access frequencies
-   Maintaining recency order among items with the same frequency

### 2. Key Operations

| Operation      | Effect on Frequency | Effect on Recency |
| -------------- | ------------------- | ----------------- |
| `cache[key]`   | +1                  | updated           |
| `cache[key]=v` | +1 (if exists)      | updated           |
| new insertion  | initial frequency   | most recent       |
| eviction       | LFU → LRU tie-break | —                 |

### 3. Eviction Logic

When the cache exceeds its capacity:

1. Identify the **minimum frequency** among all keys
2. If multiple keys share this frequency, remove the **least recently used key**
3. Update all relevant internal data structures to reflect removal

### 4. Iteration & Deletion

-   `__iter__` returns an iterator over all keys (order is arbitrary)
-   `__delitem__` removes a key and all associated metadata, raising `KeyError` if the key does not exist

---

## 📜 Output Example

```python
cache = LfuDictCache(3)
cache['a'] = 1
cache['b'] = 2
cache['c'] = 3

# Access some keys to change frequencies
_ = cache['a']
_ = cache['b']
_ = cache['a']

# Insert a new key → triggers eviction of the LFU key ('c')
cache['d'] = 4

print(list(cache))
# Output: ['a', 'b', 'd'] (order may vary)
```

---

## 📦 Usage

```python
from src import LfuDictCache

cache = LfuDictCache(max_size=3)

# Add items
cache['x'] = 10
cache['y'] = 20
cache['z'] = 30

# Access items
_ = cache['x']

# Insert new item (may evict LFU)
cache['w'] = 40

# Iterate over keys
for key in cache:
    print(key, cache[key])

# Delete an item
del cache['y']

# Get the current size
print(len(cache))
```

---

## 🧪 Running Tests

Run the provided unit tests with:

```bash
python -m unittest discover -s tests
```

The tests cover:

-   LFU and LRU eviction scenarios
-   Key retrieval and insertion
-   Deletion and iteration
-   Error handling (`KeyError`)

---

## ✅ Dependencies

-   Python 3.10+
-   `sortedcontainers` package (for `SortedDict`)

No other external dependencies are required.

---

## 🗂 Project Structure

```
.
├── .gitignore
├── main.py
├── README.md
├── src
│   ├── __init__.py
│   ├── dict_cache.py
│   ├── lfu_dict_cache.py
|   └── types.py
└── tests
    ├── __init__.py
    └── test_lfu_dict_cache.py
```

---

## 📊 Project Status

**Status:** Completed ✅

-   All tests pass successfully
-   LFU/LRU eviction logic verified
-   Fully dictionary-compatible interface implemented

---

## 📄 License

MIT License

---

## 🧮 Conclusion

`LfuDictCache` demonstrates a practical approach to designing **efficient in-memory caches** using Python.  
It combines **frequency tracking** with **recency ordering**, providing both LFU and LRU behaviors for real-world applications like caching, memory management, and performance optimization.

---

Made with ❤️ and `Python` by **Sam-Shepsl Malikin** 🎓  
© 2025 All rights reserved.
