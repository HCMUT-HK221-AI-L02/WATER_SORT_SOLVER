"""Entry point for the solver"""
from typing import Optional
import click

from lib import file2collection
from lib.collection import BottleCollection
from lib.search import A_star, State, dfs

def main():
    puzzle: str = input("Path to puzzle, please provide a .json file only, for example 'puzzle/stat.json' : ")
    try:
        start: BottleCollection = file2collection.load(puzzle)
    except ValueError as err:
        raise click.BadArgumentUsage("Invalid PUZZLE: " + str(err))
    print("Here is the input: \n")
    print(start, "\n")

    algorithm: str = input ("Algorithm, please type DFS or A*: ")
    result: Optional[State] = None
    if algorithm == "A*":
        print("Searching using A* Search\n")
        result = A_star(start)
    elif algorithm == "DFS":
        print("Searching using Depth-First Search\n")
        result = dfs(start)
    if result is None:
        print("Cannot be solved :(")
    else:
        print("Solved in", len(result.moves), "moves\n")
        print(result.collection, "\n\n", result.moves, sep="")
    return None

if __name__ == '__main__':
    main()