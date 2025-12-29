# ./tests/test_lfu_dict_cache.py

import unittest
from src import LfuDictCache


class TestLfuDictCache(unittest.TestCase):
    """
    Unit tests for the `LfuDictCache` class.

    Verifies:
        - LFU eviction logic
        - LRU tie-breaking
        - Dictionary-like behavior
        - Correct handling of edge cases
    """

    def _prepare_cache(self) -> LfuDictCache[str, int]:
        cache = LfuDictCache(3)
        cache["a"] = 1
        cache["b"] = 2
        cache["c"] = 3
        return cache

    def test_eviction_cases(self) -> None:
        """
        Test LFU/LRU eviction behavior.
        """
        test_data = [
            # Same frequency → LRU eviction
            (
                [],                 # pre-operations
                ("d", 4),            # insert
                "a",                # expected evicted key
                {"b": 2, "c": 3, "d": 4},
            ),

            # Different frequency → LFU eviction (with LRU tie-break)
            (
                [("a", 10), ("a", 40), ("get", "c"), ("get", "b")],
                ("d", 4),
                "c",
                {"a": 40, "b": 2, "d": 4},
            ),
        ]

        for pre_ops, insert, evicted, expected_items in test_data:
            print(
                f"Testing eviction with pre_ops={pre_ops}, "
                f"insert={insert}, expecting eviction of '{evicted}'"
            )
            with self.subTest(insert=insert, evicted=evicted):
                cache = self._prepare_cache()

                for op in pre_ops:
                    if op[0] == "get":
                        _ = cache[op[1]]
                    else:
                        cache[op[0]] = op[1]

                cache[insert[0]] = insert[1]

                with self.assertRaises(KeyError):
                    _ = cache[evicted]

                for key, value in expected_items.items():
                    self.assertEqual(value, cache[key])

    def test_iteration_and_deletion(self) -> None:
        """
        Test iteration over keys and deletion behavior.
        """
        test_data = [
            (
                ["a", "b", "c"],
                "c",
                ["a", "b"],
            ),
        ]

        for initial_keys, delete_key, expected_keys in test_data:
            print(
                f"Testing deletion of '{delete_key}', "
                f"expecting keys={expected_keys}"
            )
            with self.subTest(delete_key=delete_key):
                cache = self._prepare_cache()

                self.assertEqual(initial_keys, sorted(list(cache)))

                del cache[delete_key]

                self.assertEqual(expected_keys, sorted(list(cache)))

    def test_len_cases(self) -> None:
        """
        Test __len__ behavior.
        """
        test_data = [
            (None, 3),
            ("b", 2),
        ]

        for delete_key, expected_len in test_data:
            print(
                f"Testing len after deleting '{delete_key}', "
                f"expecting length={expected_len}"
            )
            with self.subTest(delete_key=delete_key):
                cache = self._prepare_cache()

                if delete_key:
                    del cache[delete_key]

                self.assertEqual(expected_len, len(cache))

    def test_error_cases(self) -> None:
        """
        Test error scenarios.
        """
        test_data = [
            ("delete", "x"),
            ("get", "x"),
        ]

        for operation, key in test_data:
            print(f"Testing error case: {operation}('{key}')")
            with self.subTest(operation=operation, key=key):
                cache = self._prepare_cache()

                if operation == "delete":
                    with self.assertRaises(KeyError):
                        del cache[key]
                else:
                    with self.assertRaises(KeyError):
                        _ = cache[key]


if __name__ == "__main__":
    print("Running LfuDictCache tests...")
    unittest.main()
