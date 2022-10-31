"""Entry point for the solver"""
from typing import Optional
import click
import os
from lib import file2collection
from lib.collection import BottleCollection
from lib.search import A_star, State, dfs
import time
import psutil
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
        start_time = time.time()
        process = psutil.Process(os.getpid())
        print("Searching using A* Search\n")
        result = A_star(start)
        print("Time execution in A* Algorithm is %s second" % (time.time() - start_time))
        print("Memory used:", process.memory_info().rss / (1024 * 1024), "MB")

    elif algorithm == "DFS":
        start_time = time.time()
        process = psutil.Process(os.getpid())
        print("Searching using Depth-First Search\n")
        result = dfs(start)
        print("Time execution in Depth-First Search Algorithm is %s second" % (time.time() - start_time))
        print("Memory used:", process.memory_info().rss / (1024 * 1024), "MB")
    if result is None:
        print("Cannot be solved :(")
    else:
        print("Solved in", len(result.moves), "moves\n")
        print(result.collection, "\n\n", result.moves, sep="")
    return None

if __name__ == '__main__':
    main()