# Sorting

Four comparison sorts, all with the same signature as `sorted(items, key=...)`, so they can be tested against it.

| Algorithm | Time (best / average / worst) | Extra space | Stable | Worth knowing |
| --- | --- | --- | --- | --- |
| `insertion_sort` | n / n² / n² | O(1) | yes | fastest for tiny or nearly sorted lists |
| `merge_sort` | n log n in all cases | O(n) | yes | stability comes from taking the left element on ties |
| `quick_sort` | n log n / n log n / n² | O(log n) stack | no | random pivot and a three-way split keep duplicates and sorted input cheap |
| `heap_sort` | n log n in all cases | O(1) | no | builds the heap bottom-up in O(n) |

The quicksort recurses into the smaller partition and loops over the larger one, so the recursion depth stays
logarithmic: a test runs it on 20,000 equal items and on sorted input with a recursion limit of 200.

```bash
python3 -m unittest discover -s sorting -t .
```
