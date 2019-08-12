# Graphs

| File | Algorithm | Cost |
| --- | --- | --- |
| `traversal.py` | breadth-first shortest path, iterative depth-first order, connected components | O(V + E) |
| `dijkstra.py` | Dijkstra with a binary heap and lazy deletion; path reconstruction | O((V + E) log V) |
| `topo.py` | Kahn's topological sort that names the nodes on a cycle | O(V + E) |
| `mst.py` | Kruskal's minimum spanning tree with union-find (path compression, union by size) | O(E log E) |

Dijkstra and Kruskal are checked against brute force on small random graphs: every simple path, or every set of
V − 1 edges, is tried.

```bash
python3 -m unittest discover -s graphs -t .
```
