"""A bottle with a limited capacity that holds items."""
from __future__ import annotations
import collections.abc
from typing import cast, Any, Optional, Sequence, Tuple, Union

from lib.item import Item

class Bottle:
    """Represents a capacity limited bottle in the game."""
    def __init__(
        self,
        init_data: Union[Sequence[Item], Bottle, Sequence[str]],
        capacity: Optional[int] = None,
    ):
        """Create a bottle with `init_data` and `capacity`."""
        self._capacity = capacity or 4
        # Ensure this is only ever set to the maximum size
        self.__data: Tuple[Item, ...]
        if isinstance(init_data, Bottle):
            self._capacity = capacity or init_data.capacity
            self.__data = init_data.data[:capacity]
        else:
            type_map = set(map(type, iter(init_data)))
            if type_map == {Item}:
                init_data = cast(
                    Sequence[Item], init_data[:capacity]
                )
                self.__data = tuple(init_data)
            elif type_map == {str}:
                init_data = cast(
                    Sequence[str], init_data[:capacity]
                )
                self.__data = tuple(
                    Item(value) for value in init_data[:capacity]
                )
            elif type_map == set():
                self.__data = tuple()
            else:
                raise TypeError(
                    f"Unknown initialiser: {init_data.__class__.__name__}"
                    f": {type_map.__repr__()}"
                )

        # Setup the number of matching items at the head of the bottle
        data_len = len(self.__data)
        if data_len != 0:
            self.__num_matching_head = 1
        else:
            self.__num_matching_head = 0

        # if there is more than one item, loop backward through the items
        # counting how many match the head item, break the loop at the
        # first non-matching item.
        if data_len > 1:
            head = self.__data[-1]
            for item in reversed(self.__data[:-1]):
                if item == head:
                    self.__num_matching_head += 1
                else:
                    break

    @property
    def data(self) -> Tuple[Item, ...]:
        """Non-settable public exposure of the internal data."""
        return self.__data

    @property
    def capacity(self) -> int:
        """Get the capacity of this bottle."""
        return self._capacity

    @property
    def is_empty(self) -> bool:
        """Check if there are any items in the bottle.
        Returns true if the bottle is empty.
        """
        return len(self.__data) == 0

    @property
    def is_full(self) -> bool:
        """Check if the bottle is full.
        Returns true if the bottle contains it's maximum number of items.
        """
        return len(self.__data) >= self.capacity

    @property
    def is_unique(self) -> bool:
        """Check if the bottle has a unique collection of items.
        Returns true if empty or all contents are the same colour.
        """
        if len(self.__data) == 0:
            return True
        return len(set(self.__data)) == 1

    @property
    def is_solved(self) -> bool:
        """Check if the bottle is solved.

        Returns true if empty or full and all contents are the same colour.
        """
        return self.is_empty or (self.is_unique and self.is_full)

    @property
    def head(self) -> Optional[Item]:
        """Get the top most item in the bottle or None if empty."""
        if self.is_empty:
            return None
        return self.__data[-1]

    @property
    def num_matching_head(self) -> int:
        """Count of consecutive items that match `self.head`.
        This includes `self.head` so for a non-empty bottle will
        always be one and will be zero if the bottle is empty.
        """
        return self.__num_matching_head

    def minRequiredMoves(self) -> int:
        """Count of minimum moves to solve a bottle
        For each bottle, the number of colors that are on top 
        of a different color is counted. For instance, a bottle with "Red, Green, Blue" 
        needs at least two moves to sort the bottle, i.e. move Green and Blue out of the bottle.
        """
        ret: int = 0
        for i in range (1, len(self.__data)):
            if self.data[i] and self.__data[i] != self.__data[i - 1]:
                ret += 1
        return ret

    def test_item(self, item: Optional[Item]) -> bool:
        """Check if `item` can be put in this bottle."""
        if self.is_full or (not self.is_empty and self.__data[-1] != item):
            return False
        return True

    def pour(self, target: Bottle) -> bool:
        """Move the head item from this bottle to target bottle.
        If there are multiple concurrent items that are equal, move as many as
        fit within `target` over to it.
        Returns a bool indicating if any items were successfully moved.
        """
        head = self.head
        if head is None:
            return False
        if not target.test_item(head):
            return False
        # Remove the last item from data and add it to target
        self.__data = self.__data[:-1]
        target.add(head)
        self.__num_matching_head -= 1
        # Check for matching colours left at head and keep repeating
        # until all have been moved or target is full
        while self.head is not None and self.head == head:
            if target.is_full:
                break
            self.__data = self.__data[:-1]
            target.add(head)
            self.__num_matching_head -= 1
        if self.__num_matching_head == 0 and not self.is_empty:
            # There is a new head colour and we need to re-compute the number
            # of matching items by looping backward through the items
            self.__num_matching_head = 1
            for item in reversed(self.__data[:-1]):
                if item == self.head:
                    self.__num_matching_head += 1
                else:
                    break
        return True

    def add(self, item: Item) -> bool:
        """Add `item` to this collection.
        Returns a boolean indicating success.
        """
        if not self.test_item(item):
            return False
        # Convert data to a list and then back to a tuple to change it
        data = list(self.__data)
        data.append(item)
        self.__num_matching_head += 1
        self.__data = tuple(data)
        return True

    def copy(self) -> Bottle:
        """Create a new bottle with the same data.
        The new bottle can be mutated using the `add` function
        without affecting the original bottle.
        """
        return Bottle(self)

    def __eq__(self, other: Any) -> bool:
        """Check if this bottle is equal to other."""
        if isinstance(other, Bottle):
            return self.__data == other.data
        if isinstance(other, collections.abc.Sequence):
            return self.__data == tuple(other)
        return False

    def __ne__(self, other: Any) -> bool:
        """Check if this bottle is not equal to other."""
        return not self.__eq__(other)

    def __str__(self) -> str:
        """Get the string representation of this bottle."""
        content = [str(content) for content in self.__data]
        padding = ""
        if len(content) < self.capacity:
            padding = " " * (self.capacity - len(self))
        return f"[{''.join(content)}{padding}]"

    def __repr__(self) -> str:
        """Get a representation of the bottle."""
        return f"[{','.join(item.__repr__() for item in self.__data)}]"

    def __len__(self) -> int:
        """Return the number of items contained."""
        return len(self.__data)

    def __getitem__(self, idx):
        """Get the `item` at `index`."""
        return self.__data.__getitem__(idx)

    def __iter__(self):
        """Iterate over this bottle's items."""
        self.__iter_val = 0
        return self

    def __next__(self):
        """Get the next item from this bottle."""
        if self.__iter_val >= self.capacity:
            raise StopIteration
        self.__iter_val += 1
        return self.__data[-1 * self.__iter_val]
