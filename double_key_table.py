from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        if sizes is not None:
            self.TABLE_SIZES = sizes
        self.table = ArrayR(len(self.TABLE_SIZES))
        self.internal_sizes = internal_sizes if internal_sizes is not None else self.TABLE_SIZES

        for i in range(len(self.table)):
            self.table[i] = LinearProbeTable(self.TABLE_SIZES[i])

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        top_index = self.hash1(key1)
        sub_table = self.table[top_index]
        if sub_table is None:
            if is_insert:
                sub_table = LinearProbeTable(self.internal_sizes[top_index])
                sub_table.hash = lambda k: self.hash2(k, sub_table)
                self.table[top_index] = sub_table
            else:
                raise KeyError(f"Key pair {key1}, {key2} not found")
        bottom_index = sub_table.hash(key2)
        return top_index, bottom_index

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if key is None:
            for sub_table in self.table:
                if sub_table is not None:
                    yield from sub_table.iter_keys()
        else:
            top_index = self.hash1(key)
            sub_table = self.table[top_index]
            if sub_table is not None:
                yield from sub_table.iter_keys(key)

    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        if key is None:
            result = []
            for sub_table in self.table:
                if sub_table is not None:
                    result.extend(sub_table.keys())
            return result
        else:
            top_index = self.hash1(key)
            sub_table = self.table[top_index]
            if sub_table is not None:
                return sub_table.keys()
            else:
                return []

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        if key is None:
            for sub_table in self.table:
                if sub_table is not None:
                    yield from sub_table.iter_values()
        else:
            top_index = self.hash1(key)
            sub_table = self.table[top_index]
            if sub_table is not None:
                yield from sub_table.iter_values()

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        if key is None:
            result = []
            for sub_table in self.table:
                if sub_table is not None:
                    result.extend(sub_table.values())
            return result
        else:
            top_index = self.hash1(key)
            sub_table = self.table[top_index]
            if sub_table is not None:
                return sub_table.values()
            else:
                return []

    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        top_index, bottom_index = self._linear_probe(key[0], key[1], False)
        sub_table = self.table[top_index]
        return sub_table[bottom_index]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        top_index, bottom_index = self._linear_probe(key[0], key[1], True)
        sub_table = self.table[top_index]
        sub_table[bottom_index] = data

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        top_index, bottom_index = self._linear_probe(key[0], key[1], False)
        sub_table = self.table[top_index]
        del sub_table[bottom_index]

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        old_table = self.table
        old_sizes = self.internal_sizes

        self.table = ArrayR(len(self.TABLE_SIZES))
        self.internal_sizes = [old_sizes[self.TABLE_SIZES.index(size)] for size in self.TABLE_SIZES]

        for i in range(len(self.table)):
            self.table[i] = LinearProbeTable(self.TABLE_SIZES[i])

        for sub_table in old_table:
            if sub_table is not None:
                for key, value in sub_table.items():
                    top_index, bottom_index = self._linear_probe(key, value, True)
                    new_sub_table = self.table[top_index]
                    new_sub_table[bottom_index] = value

    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.table)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        count = 0
        for sub_table in self.table:
            if sub_table is not None:
                count += len(sub_table)
        return count


def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()
