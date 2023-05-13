from __future__ import annotations
from dataclasses import dataclass
from data_structures.linked_stack import LinkedStack
from mountain import Mountain

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality


@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        if isinstance(self.path_follow.store, TrailSeries):
            return TrailSeries(mountain=self.path_follow.store.mountain, following=self.path_follow.store.following)
        else:
            return self.path_follow.store


@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        new_series = TrailSeries(mountain, Trail(self))
        return new_series

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        return TrailSplit(Trail(None), Trail(None), Trail(self))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""

        new_series = Trail(TrailSeries(mountain, self.following))
        actual_series = TrailSeries(self.mountain, new_series)
        return actual_series

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""

        new_series = Trail((TrailSplit(path_top=Trail(None), path_bottom=Trail(None), path_follow=self.following)))

        return TrailSeries(self.mountain, new_series)


TrailStore = Union[TrailSplit, TrailSeries, None]


@dataclass
class Trail:
    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        return Trail(TrailSeries(mountain=mountain, following=self))

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        return Trail(TrailSplit(path_top=Trail(None), path_bottom=Trail(None), path_follow=self))

    def follow_path(self, personality):
        stack =LinkedStack()
        current = self

        while current:
            if isinstance(current.store, TrailSeries):
                personality.add_mountain(current.store.mountain)
                current = current.store.following
            elif isinstance(current.store, TrailSplit):
                if personality.select_branch(current.store.path_top, current.store.path_bottom):
                    current = current.store.path_top
                else:
                    current = current.store.path_bottom

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        if isinstance(self.store, TrailSeries):
            return [self.store.mountain] + self.store.following.collect_all_mountains()
        elif isinstance(self.store, TrailSplit):
            return (
                    self.store.path_top.collect_all_mountains() +
                    self.store.path_bottom.collect_all_mountains() +
                    self.store.path_follow.collect_all_mountains()
            )
        else:
            return []

    def length_k_paths(self, k) -> list[list[Mountain]]:  # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        if k == 0:
            return [[]]
        paths = []
        if isinstance(self.store, TrailSplit):
            paths += self.store.path_top.length_k_paths(k - 1)
            paths += self.store.path_bottom.length_k_paths(k - 1)
            paths += self.store.path_follow.length_k_paths(k - 1)
        elif isinstance(self.store, TrailSeries):
            paths += self.store.following.length_k_paths(k - 1)
        return [[self.store.mountain] + p for p in paths]
