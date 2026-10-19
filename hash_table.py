class _Node:
    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node


class HashTable:
    """A fixed-size bucket array with singly linked collision chains."""

    def __init__(self, capacity=16):
        if type(capacity) is not int:
            raise TypeError("capacity must be an integer")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._buckets = [None] * capacity
        self._size = 0

    def _hash(self, key):
        """Map integer or string keys to a bucket index."""
        if isinstance(key, int):
            return key % len(self._buckets)
        if isinstance(key, str):
            result = 0
            for character in key:
                result = (31 * result + ord(character)) % len(self._buckets)
            return result
        raise TypeError("keys must be integers or strings")

    def insert(self, key, value):
        """Insert a key-value pair, replacing the value if the key exists."""
        index = self._hash(key)
        node = self._buckets[index]
        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next
        self._buckets[index] = _Node(key, value, self._buckets[index])
        self._size += 1

    def search(self, key):
        """Return the stored value, or raise KeyError for a missing key."""
        node = self._buckets[self._hash(key)]
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        raise KeyError(key)

    def delete(self, key):
        """Remove a key and return its value, or raise KeyError."""
        index = self._hash(key)
        previous = None
        node = self._buckets[index]
        while node is not None:
            if node.key == key:
                if previous is None:
                    self._buckets[index] = node.next
                else:
                    previous.next = node.next
                self._size -= 1
                return node.value
            previous = node
            node = node.next
        raise KeyError(key)

    def __len__(self):
        return self._size
