import random
import unittest
from collections import OrderedDict

from linked_structures.lru_cache import LRUCache


class LRUCacheTest(unittest.TestCase):
    def test_evicts_the_least_recently_used_key(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")  # a is now more recent than b
        cache.put("c", 3)
        self.assertIsNone(cache.get("b"))
        self.assertEqual(cache.keys(), ["c", "a"])

    def test_updating_a_key_refreshes_it(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("a", 10)
        cache.put("c", 3)
        self.assertEqual(cache.get("a"), 10)
        self.assertIsNone(cache.get("b"))

    def test_matches_an_ordered_dict_model(self):
        rng = random.Random(6)
        cache, model = LRUCache(8), OrderedDict()
        for _ in range(10_000):
            key = rng.randrange(20)
            if rng.random() < 0.5:
                expected = model.get(key)
                if key in model:
                    model.move_to_end(key)
                self.assertEqual(cache.get(key), expected)
            else:
                cache.put(key, key * 2)
                model[key] = key * 2
                model.move_to_end(key)
                if len(model) > 8:
                    model.popitem(last=False)
            self.assertEqual(cache.keys(), list(reversed(model)))

    def test_rejects_zero_capacity(self):
        with self.assertRaises(ValueError):
            LRUCache(0)


if __name__ == "__main__":
    unittest.main()
