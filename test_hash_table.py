import unittest

from hash_table import HashTable


class HashTableTests(unittest.TestCase):
    def test_insert_search_and_update(self):
        table = HashTable()
        table.insert("name", "Alice")
        table.insert(7, None)
        self.assertEqual(table.search("name"), "Alice")
        self.assertIsNone(table.search(7))
        table.insert("name", "Bob")
        self.assertEqual(table.search("name"), "Bob")
        self.assertEqual(len(table), 2)

    def test_missing_keys(self):
        table = HashTable(1)
        for operation in (table.search, table.delete):
            with self.assertRaises(KeyError):
                operation("missing")
        table.insert("present", 1)
        for operation in (table.search, table.delete):
            with self.assertRaises(KeyError):
                operation("missing")
        self.assertEqual(table.search("present"), 1)
        self.assertEqual(len(table), 1)

    def test_delete_head_middle_and_tail(self):
        for deleted_key in (0, 3, 6):
            with self.subTest(deleted_key=deleted_key):
                table = HashTable(3)
                for key in (0, 3, 6):
                    table.insert(key, str(key))
                self.assertEqual(table.delete(deleted_key), str(deleted_key))
                with self.assertRaises(KeyError):
                    table.search(deleted_key)
                for key in (0, 3, 6):
                    if key != deleted_key:
                        self.assertEqual(table.search(key), str(key))
                self.assertEqual(len(table), 2)

    def test_many_collisions(self):
        table = HashTable(1)
        for key in range(500):
            table.insert(key, key * 2)
        for key in range(500):
            self.assertEqual(table.search(key), key * 2)
        table.insert(250, "updated")
        self.assertEqual(table.search(250), "updated")
        self.assertEqual(len(table), 500)
        for key in range(0, 500, 2):
            table.delete(key)
        for key in range(1, 500, 2):
            self.assertEqual(table.search(key), key * 2)
        self.assertEqual(len(table), 250)
        for key in range(1, 500, 2):
            table.delete(key)
        self.assertEqual(len(table), 0)
        table.insert("again", 42)
        self.assertEqual(table.search("again"), 42)

    def test_string_collisions(self):
        table = HashTable(2)
        for key in ("a", "c", "e", "g"):
            table.insert(key, key.upper())
        table.delete("c")
        for key in ("a", "e", "g"):
            self.assertEqual(table.search(key), key.upper())

    def test_negative_and_distinct_key_types(self):
        table = HashTable(3)
        for key in (-10, 0, 10, "10", ""):
            table.insert(key, repr(key))
        for key in (-10, 0, 10, "10", ""):
            self.assertEqual(table.search(key), repr(key))
        self.assertEqual(len(table), 5)

    def test_invalid_capacity(self):
        for capacity in (0, -1):
            with self.assertRaises(ValueError):
                HashTable(capacity)
        for capacity in (True, 1.5, "3", None):
            with self.assertRaises(TypeError):
                HashTable(capacity)

    def test_unsupported_keys(self):
        table = HashTable()
        for key in ([], {}, None, 1.5):
            for operation in (table.search, table.delete):
                with self.assertRaises(TypeError):
                    operation(key)
            with self.assertRaises(TypeError):
                table.insert(key, "value")
        self.assertEqual(len(table), 0)


if __name__ == "__main__":
    unittest.main()
