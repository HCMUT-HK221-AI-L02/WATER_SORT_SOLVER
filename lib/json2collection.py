"""Module for handling the conversion of json input files to collections."""
import json
from typing import TextIO, List

from lib.collection import BottleCollection

def load(file: TextIO) -> BottleCollection:
    """Load a json file into a `BottleCollection`."""
    content: List[List[str]] = json.load(file)
    return BottleCollection(content)
