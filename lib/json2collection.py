"""Module for handling the conversion of json input files to collections."""
import json
from typing import TextIO, List

# from solver.lib.container import Container
from lib.collection import ContainerCollection


def load(file: TextIO) -> ContainerCollection:
    """Load a json file into a `ContainerCollection`."""
    content: List[List[str]] = json.load(file)
    return ContainerCollection(content)
