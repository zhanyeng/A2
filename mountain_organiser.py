from __future__ import annotations

from mountain import Mountain

class MountainOrganiser:

    def __init__(self) -> None:
        self.mountains = []

    def cur_position(self, mountain: Mountain) -> int:
        def compare(m1, m2):
            if m1.length < m2.length:
                return -1
            elif m1.length > m2.length:
                return 1
            else:
                return m1.name.compare(m2.name)

        left = 0
        right = len(self.mountains) - 1

        while left <= right:
            mid = (left + right) // 2
            curr_mountain = self.mountains[mid]

            comparison = compare(curr_mountain, mountain)
            if comparison == 0:
                return mid + 1
            elif comparison < 0:
                left = mid + 1
            else:
                right = mid - 1

        raise KeyError("Mountain not found")

    def add_mountains(self, mountains: list[Mountain]) -> None:
        self.mountains.extend(mountains)
        self.mountains.sort(key=lambda m: (m.length, m.name))
