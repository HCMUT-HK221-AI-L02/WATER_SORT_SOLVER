"""Entry point for the solver"""
from typing import Optional
import click
from lib import file2collection
from lib.collection import ContainerCollection
from lib.search import Option, bfs, dfs

def main():
    puzzle: str = input("Path to puzzle, please provide a .json file only, for example 'puzzle/stat.json' : ")
    algorithm: str = input ("Algorithm, please type DFS or A*: ")
    try:
        start: ContainerCollection = file2collection.load(puzzle)
    except ValueError as err:
        raise click.BadArgumentUsage("Invalid PUZZLE: " + str(err))
    print("Here is the input: \n")
    print(start, "\n")

    result: Optional[Option] = None
    if algorithm == "BFS":
        print("Searching using Breadth-First Search\n")
        result = bfs(start)
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