# Linked structures

| File | Contents |
| --- | --- |
| `linked_list.py` | singly linked list with a tail pointer: O(1) append and prepend, in-place reversal |
| `stack_queue.py` | stack; FIFO queue from two stacks (amortised O(1)); bracket matching with a stack |
| `lru_cache.py` | least-recently-used cache with O(1) `get` and `put`: dict + doubly linked list with sentinels |

The queue and the cache are tested against reference models (`collections.deque`, `OrderedDict`) over thousands of
random operations, which catches pointer mistakes that example-based tests miss.

```bash
python3 -m unittest discover -s linked_structures -t .
```
