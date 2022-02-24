from docarray import DocumentArray, Document
from config import DATA_DIR, CSV_FILE
import random
import os


def get_columns(document):
    """
    Return a list of tuples, each tuple containing column name and type
    """
    # tags = document.tags.to_dict()
    tags = document.tags
    names = list(tags.keys())
    types = list(tags.values())
    columns = []

    for field, value in zip(names, types):
        try:
            value = int(value)  # Handle year better
        except:
            pass

        if isinstance(value, str):
            value = "str"
        elif isinstance(value, int):
            value = "int"

        col = (field, value)
        columns.append(col)

    return columns
