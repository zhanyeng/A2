from __future__ import annotations

from mountain import Mountain
from data_structures.referential_array import ArrayR, TypeVar


class MountainOrganiser:

    def __init__(self) -> None:
        self.mountains = []

    def cur_position(self, mountain: Mountain) -> int:
        low = 0
        high = len(self.mountains) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.mountains[mid] == mountain:
                return mid
            elif self.mountains[mid].length < mountain.length:
                low = mid + 1
            elif self.mountains[mid].length > mountain.length:
                high = mid - 1
            elif self.mountains[mid].name < mountain.name:
                low = mid + 1
            elif self.mountains[mid].name > mountain.name:
                high = mid - 1

        raise KeyError("Mountain not found")

    def add_mountains(self, mountains: list[Mountain]) -> None:
        self.mountains.extend(mountains)
        tmp = [None] * len(self.mountains)
        self._merge_sort_aux(0, len(self.mountains) - 1, tmp)

    def _merge_sort_aux(self, start: int, end: int, tmp: ArrayR) -> None:
        if start < end:
            mid = (start + end) // 2
            self._merge_sort_aux(start, mid, tmp)
            self._merge_sort_aux(mid + 1, end, tmp)
            self._merge_arrays(start, mid, end, tmp)

    def _merge_arrays(a: list, start: int, mid: int, end: int, tmp: ArrayR) -> None:
        ia = start
        ib = mid + 1
        for k in range(start, end + 1):
            if ia > mid:
                tmp[k] = a[ib]
                ib += 1
            elif ib > end:
                tmp[k] = a[ia]
                ia += 1
            elif a[ia] <= a[ib]:
                tmp[k] = a[ia]
                ia += 1
            else:
                tmp[k] = a[ib]
                ib += 1
        for k in range(start, end + 1):
            a[k] = tmp[k]
