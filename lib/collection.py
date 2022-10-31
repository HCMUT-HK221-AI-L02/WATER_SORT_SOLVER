"""Collection stores all bottles"""
from __future__ import annotations

from typing import Union, List, Optional
from lib.item import Item
from lib.move import Move
from lib.bottle import Bottle

class BottleCollection:
    """Collection of bottles."""
    def __init__(
        self,
        data: Union[BottleCollection, List[Bottle], List[List[str]]],
    ):
        """Construct a new collection from `data`."""
        self.__unique_set: Optional[set] = None
        self.__possible_moves: Optional[List[Move]] = None
        if isinstance(data, list):
            self.data = tuple(Bottle(item) for item in data)
        elif isinstance(data, BottleCollection):
            self.data = tuple(bottle.copy() for bottle in data.data)
        else:
            raise TypeError(
                f"Invalid type ({data.__class__.__name__}) "
                "used to construct BottleCollection."
            )

    @property
    def is_solved(self) -> bool:
        """Check if all bottles are solved."""
        return all([bottle.is_solved for bottle in self.data])

    def copy(self) -> BottleCollection:
        """Create a new collection with the same data.
        """
        return BottleCollection(self)

    def minRequiredMoves(self) -> int:
        """Count of minimum moves to solve a collection, which is sum of
        1. Min required moves of each bottle
        2. The bottom-most colors
        For example, if Red is at the bottom of three bottles, at least two moves are required.
        """
        ret: int = 0
        bottom_colors: List[Item] = list()
        bc_count: List[int] = list()
        for i in range (len(self.data)):
            if self.data[i].is_empty: 
                continue
            ret += self.data[i].minRequiredMoves()
            bc: Item = self.data[i][0]
            if bc in bottom_colors:
                bc_count[bottom_colors.index(bc)] += 1
            else:
                bottom_colors.append(bc)
                bc_count.append(0)
        for i in range (len(bc_count)):
            if bc_count[i] != 0: 
                ret += bc_count[i]
        return ret

    # work out all possible next moves:
    def get_moves(self) -> List[Move]:
        """Get a list of possible moves.
        Each move is a possible way to move a colour between two indexes
        in the collection.
        Note: this function uses a cached representation of the collection for
        performance and if any item within the collection is modified may not
        be correct.
        """
        # check for if this is cached
        if self.__possible_moves is not None:
            return self.__possible_moves
        moves: List[Move] = []
        for x in range(len(self)):
            # Skip fully solved bottles
            if (
                self.data[x].is_solved
                or self.data[x].is_empty
                or (self.data[x].is_unique and len(self.data[x]) > 2)
            ):
                continue
            used_in_empty = False
            for y in range(len(self)):
                if x == y:
                    continue
                move = Move(x, y)
                # check if this is a possible move
                if not self.is_valid(move):
                    continue
                #check if source bottle has been poured to an empty bottle
                if used_in_empty and self.data[move.dest].is_empty:
                    continue
                moves.append(move)
                if self.data[move.dest].is_empty:
                    used_in_empty = True
        self.__possible_moves = moves
        return moves

    def is_valid(self, move: Move) -> bool:
        """Check if a move is valid for this collection."""
        # Ensure it's a practical move
        if (
            move.src == move.dest
            or self.data[move.dest].is_full
            or self.data[move.src].is_empty
        ):
            return False
        src = self.data[move.src]
        dest = self.data[move.dest]

        # Don't allow needless movement between unique bottle and empty bottle 
        if src.is_unique and dest.is_empty:
            return False

        # This test_items the top most colour matches.
        # If it does, also check there's enough capacity for the pour.
        # Don't try to put more into a bottle than it could take
        dest_space = dest.capacity - len(dest)
        return (
            self.data[move.dest].test_item(self.data[move.src].head)
            and src.num_matching_head <= dest_space
        )

    def after_moving(self, move: Move) -> BottleCollection:
        """Get a new collection after moving items"""
        if not self.is_valid(move):
            raise ValueError("Invalid move", move)
        _next = BottleCollection(self)
        _next.data[move.src].pour(_next.data[move.dest])
        return _next

    def __getitem__(self, x):
        """Get item for this index."""
        return self.data[x]

    def __len__(self) -> int:
        """Get the number of bottles in the collection."""
        return len(self.data)

    def _unique_set(self):
        """Get the set representing the unique bottles in the collection.

        This set is cached to improve performance of comparing collections
        during the solving process and therefore is not guaranteed to be
        representative of the collection if bottle is directly modified
        rather than using the `after` method.
        """
        if self.__unique_set is None:
            self.__unique_set = set(bottle.data for bottle in self.data)
        return self.__unique_set

    def __eq__(self, other: object) -> bool:
        """Check if this collection is the same as `other`.
        Compares the contents of each bottle but ignores the order.
        Note: this function uses a cached representation of the collection for
        performance and if any item within the collection is modified may not
        be correct.
        """
        if isinstance(other, BottleCollection):
            return self._unique_set() == other._unique_set()
        if isinstance(other, list):
            return self._unique_set() == set(
                bottle.data for bottle in other
            )
        return False

    def __ne__(self, other: object) -> bool:
        """Check if this collection is different to `other`."""
        return not self.__eq__(other)

    def __str__(self) -> str:
        """Printable representation of this collection."""
        return "\n".join(
            str(i).rjust(2, " ") + ": " + str(self.data[i])
            for i in range(len(self))
        )

    def __repr__(self) -> str:
        """Textual representation of the collection."""
        return f"[{','.join(item.__repr__() for item in self.data)}]"
