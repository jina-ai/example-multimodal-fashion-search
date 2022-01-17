import os
from docarray.array.document import DocumentArray
from config import MAX_DOCS, SERVER, PORT, DATA_DIR, CSV_FILE
from jina import Client, Document
import random

search_terms = ("Dress", "Shirt", "Shoe")

# Server
def generate_price(minimum=10, maximum=200):
    price = random.randrange(minimum, maximum)

    return price


def input_docs_from_csv(file_path=CSV_FILE, max_docs=100, data_dir=DATA_DIR):
    docs = DocumentArray()
    import csv
    from itertools import islice

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in islice(reader, max_docs):
            try:  # To skip malformed rows
                filename = f"{data_dir}/{row['id']}.jpg"
                doc = Document(uri=filename, tags=row)
                random.seed(int(doc.tags['id'])) # Ensure reproducability

                # Generate useful data that's missing
                doc.tags["price"] = generate_price()  # Generate fake price
                doc.tags["rating"] = random.randrange(0, 5)

                doc.load_uri_to_image_blob()
                docs.append(doc)
            except:
                pass

    return docs


def get_columns(document):
    """
    Return a list of tuples, each tuple containing column name and type
    """
    tags = document.tags.to_dict()
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


# Client


def get_matches(input, server=SERVER, port=PORT, limit=MAX_DOCS, filters=None):
    from pprint import pprint
    pprint(filters)
    client = Client(host=server, protocol="http", port=port)
    response = client.search(
        Document(text=input),
        return_results=True,
        parameters={"limit": limit, "filter": filters},
        show_progress=True,
    )
    matches = response[0].docs[0].matches
    # for match in matches:
        # print(match.id)
        # print(match.tags["year"])
        # print(match.tags.keys)

    return matches


def print_stars(rating, maximum=5):
    rating = int(rating)
    positive = "★"
    negative = "☆"

    string = rating * positive + (maximum - rating) * negative

    return string


def resize_image(filename, resize_factor=2):
    from PIL import Image

    image = Image.open(filename)
    w, h = image.size
    image = image.resize((w * resize_factor, h * resize_factor), Image.ANTIALIAS)

    return image
