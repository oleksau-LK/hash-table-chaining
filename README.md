# Hash table with chaining

Simple Python 3 hash table. Each bucket holds a singly linked list to handle
collisions. No dependencies are required.

Keys are integers or strings; values can be any object. Integer keys use modulo
hashing; strings use a polynomial hash with multiplier 31. The bucket count is
fixed (default: 16). Operations take O(1) time on average with short chains and
O(n) in the worst case.

```python
from hash_table import HashTable

table = HashTable(capacity=5)
table.insert("apple", 10)
table.insert("apple", 20)  # Replace the existing value.
print(table.search("apple"))  # 20
print(table.delete("apple"))  # 20
print(len(table))  # 0
```

`search` and `delete` raise `KeyError` for missing keys. Unsupported key types
raise `TypeError`. Capacity must be a positive integer.

Run tests, including forced collisions and deletion at every chain position:

```sh
python3 -m unittest -v
```
