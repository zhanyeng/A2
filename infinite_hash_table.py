from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        self.table = [None] * self.TABLE_SIZE


    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        location = self.get_location(key)
        current_table = self.table
        for index in location:
            current_table = current_table[index]
            if current_table is None:
                raise KeyError(key)
        return current_table

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        location = self.get_location(key)
        current_table = self.table
        for index in location[:-1]:
            if current_table[index] is None:
                current_table[index] = [None] * self.TABLE_SIZE
            current_table = current_table[index]
        current_table[location[-1]] = value

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        location = self.get_location(key)
        path = []
        current_table = self.table
        for index in location[:-1]:
            path.append((current_table, index))
            current_table = current_table[index]
            if current_table is None:
                raise KeyError(key)
        del current_table[location[-1]]
        while len(current_table) == 1:
            parent_table, parent_index = path.pop()
            del parent_table[parent_index]
            current_table = parent_table

    def __len__(self):
        count = 0
        stack = [self.table]
        while stack:
            current_table = stack.pop()
            for entry in current_table:
                if entry is None:
                    continue
                if isinstance(entry, list):
                    stack.append(entry)
                else:
                    count += 1
        return count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        location = []
        current_table = self.table
        for level in range(len(key) + 1):
            index = self.hash(key, level)
            location.append(index)
            if current_table[index] is None:
                raise KeyError("Key does not exist")
            current_table = current_table[index]
        return location

    def __contains__(self, key: K) -> bool:
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
