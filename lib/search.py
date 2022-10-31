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

    def __eq__(self, other: Any) -> bool:
        if self.collection == other.collection:
            return True
        return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

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
    open_set: List[State] = [state]
    closed_set: List[State] = []
    heapq.heapify(open_set)

    while len(open_set):
        base: State = heapq.heappop(open_set)
        if base.collection.is_solved:
            return base
        if base.collection.minRequiredMoves == 0:
            continue

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
            #Create a new State
            next_moves = list(base.moves)
            next_moves.append(move)
            next_state: State = State(base.collection.after_moving(move), tuple(next_moves))
            #Calculate the f score
            minRequiredMoves = next_state.collection.minRequiredMoves()
            next_state.score = minRequiredMoves + len(next_state.moves)
            next_state.moves[-1].score = next_state.score
            #Check if this state has been visited or not
            if next_state not in open_set and next_state not in closed_set:
                #Add a new state to open set
                heapq.heappush(open_set, next_state)
            else:
                #Check if g value of this state when visit it through the base state
                #is better than the current g value
                #If yes, we have to visit it again through the base state
                if next_state in open_set:
                    visited: State = open_set[open_set.index(next_state)]
                    if len(visited.moves) > len(next_state.moves):
                        visited.moves = next_state.moves
                        visited.score = visited.collection.minRequiredMoves() + len(visited.moves)
                if next_state in closed_set:
                    visited: State = closed_set[closed_set.index(next_state)]
                    if len(visited.moves) > len(next_state.moves):
                        visited.moves = next_state.moves
                        visited.score = visited.collection.minRequiredMoves() + len(visited.moves)
                        #Add this visited state to open set and remove it from closed set 
                        heapq.heappush(open_set, visited)
                        closed_set.remove(visited)
        #Add the visited state to closed set
        closed_set.append(base)
            #This use to print the current heap when debug
            #print(open_set, "\n")
    return None