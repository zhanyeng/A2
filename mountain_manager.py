from mountain import Mountain

class MountainManager:

    def __init__(self) -> None:
        self.mountains = []

    def add_mountain(self, mountain: Mountain):
        self.mountains.append(mountain)

    def remove_mountain(self, mountain: Mountain):
        self.mountains.remove(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain):
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int):
        return [mountain for mountain in self.mountains if mountain.difficulty_level == diff]

    def group_by_difficulty(self):
        grouped_mountains = [[] for _ in range(10)]  # Assuming difficulty levels from 0 to 9
        for mountain in self.mountains:
            grouped_mountains[mountain.difficulty_level].append(mountain)

        return [mountains for mountains in grouped_mountains if mountains]
