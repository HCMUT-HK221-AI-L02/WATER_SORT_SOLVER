"""Route files to the correct loader for convert to a collection."""
import pathlib

from lib import json2collection
from lib.collection import ContainerCollection


def load(path: str) -> ContainerCollection:
    """Load a file based on it's extension."""
    file = pathlib.Path(path)
    if file.suffix == ".json":
        with file.open() as fh:
            return json2collection.load(fh)
    else:
        raise ValueError("Invalid file")
