"""Implementation of search algorithms."""
from typing import List, Optional, Tuple, Any
from dataclasses import dataclass
# importing "heapq" to implement heap queue
import heapq
from lib.collection import BottleCollection
from lib.move import Move

@dataclass
class State:
    """Represents an state in the graph of possible games."""
    collection: BottleCollection
    moves: Tuple[Move, ...]
    score: Optional[int] = None
    def __lt__(self, other: Any) ->bool:
        if self.score != other.score:
            return self.score < other.score
        #Tie breaker: sort solutions with many steps in front of solutions with fewer steps.
        #This leads to the algorithm "greedily" trying longer solutions first,
        #before back-tracking to shorter solutions.
        return len(self.moves) > len(other.moves)

def dfs(root: BottleCollection) -> Optional[State]:
    """Perform a depth-first search to find a solution."""
    # Ensure the search is required
    if root.is_solved:
        return State(root, tuple())
    visited: List[BottleCollection] = []
    # Call the recursive function
    return dfs_recursive(visited, State(root, tuple()))

def dfs_recursive(visited: List[BottleCollection], state: State) -> Optional[State]:
    col = state.collection
    #Check if we visited this case or not
    if col in visited:
        return None
    visited.append(col)
    #If this case is solved, just return the result
    if col.is_solved:
        return state
    #Searching for solution
    for move in col.get_moves():
        next_moves = list(state.moves)
        next_moves.append(move)
        next_option = State(col.after_moving(move), tuple(next_moves))
        result = dfs_recursive(visited, next_option)
        if result is not None:
            return result
    # After visiting all possible moves, nothing had a solution
    return None

def A_star(root: BottleCollection) -> Optional[State]:
    state: State = State(root, tuple())
    # h holds partial solutions.
	# Pop() returns (one of) the solution closest to a solved state.
    h: List[State] = [state]
    heapq.heapify(h)

    while len(h):
        base: State = heapq.heappop(h)
        if base.collection.is_solved:
            return base

        for move in base.collection.get_moves():
            # If this move is the reverse of the previous move and the move
            # before that was this move, a loop has been found and needs to
            # be broken by simply ignoring this move.
            if (
                len(base.moves) > 1
                and base.moves[-1] == move.reverse()
                and base.moves[-2] == move
            ):
                continue
            
            next_moves = list(base.moves)
            next_moves.append(move)
            next_state: State = State(base.collection.after_moving(move), tuple(next_moves))

            minRequiredMoves = next_state.collection.minRequiredMoves()
            next_state.score = minRequiredMoves + len(next_state.moves)
            next_state.moves[-1].score = next_state.score

            heapq.heappush(h, next_state)
            #This use to print the current heap when debug
            #print(h, "\n")
    return None