from docarray import DocumentArray
from config import TEXT_IMAGE_SERVER, TEXT_IMAGE_PORT, DATA_DIR, TOP_K, IMAGE_IMAGE_SERVER, IMAGE_IMAGE_PORT
from jina import Client, Document
import random

search_terms = ("Dress", "Shirt", "Shoe")

# Server
def generate_price(minimum=10, maximum=200):
    price = random.randrange(minimum, maximum)

    return price


def input_docs_from_csv(file_path, max_docs):
    docs = DocumentArray()
    import csv
    from itertools import islice

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in islice(reader, max_docs):
            try:  # To skip malformed rows
                filename = f"{DATA_DIR}/{row['id']}.jpg"
                doc = Document(uri=filename, tags=row)
                # random.seed(int(doc.tags['id'])) # Ensure reproducability

                # Generate useful data that's missing
                doc.tags["price"] = generate_price()  # Generate fake price
                doc.tags["rating"] = random.randrange(0, 5)

                doc.convert_uri_to_image_blob()
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

def get_matches_from_image(input, server=IMAGE_IMAGE_SERVER, port=IMAGE_IMAGE_PORT, limit=TOP_K, filters=None):
    data = input.read()
    query_doc = Document(buffer=data)
    query_doc.convert_buffer_to_image_blob()
    query_doc.set_image_blob_shape((80, 60))

    client = Client(host=server, protocol="http", port=port)
    response = client.search(
        query_doc,
        return_results=True,
        parameters={"limit": limit, "filter": filters},
        show_progress=True,
    )
    from pprint import pprint
    pprint(response)
    matches = response[0].docs[0].matches

    return matches


def get_matches(input, server=TEXT_IMAGE_SERVER, port=TEXT_IMAGE_PORT, limit=TOP_K, filters=None):
    # filters = {
        # "season": {"$eq": "Fall"}
    # }
    client = Client(host=server, protocol="http", port=port)
    matches = client.search(
        Document(text=input),
        return_results=True,
        parameters={"limit": limit, "filter": filters},
        show_progress=True,
    )

    return matches[0].matches


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

class facets:
    gender = ["Men", "Women"]
    season = ["Summer", "Spring", "Fall", "Winter"]
    color = ['Beige', 'Black', 'Blue', 'Bronze', 'Brown', 'Burgundy', 'Charcoal', 'Coffee Brown', 'Copper', 'Cream', 'Fluorescent Green', 'Gold', 'Green', 'Grey', 'Grey Melange', 'Khaki', 'Lavender', 'Lime Green', 'Magenta', 'Maroon', 'Mauve', 'Metallic', 'Multi', 'Mushroom Brown', 'Mustard', 'NA', 'Navy Blue', 'Nude', 'Off White', 'Olive', 'Orange', 'Peach', 'Pink', 'Purple', 'Red', 'Rose', 'Rust', 'Sea Green', 'Silver', 'Skin', 'Steel', 'Tan', 'Taupe', 'Teal', 'Turquoise Blue', 'White', 'Yellow']
    usage = ['', 'Casual', 'Ethnic', 'Formal', 'Home', 'NA', 'Party', 'Smart Casual', 'Sports', 'Travel']
    masterCategory = ['Accessories', 'Apparel', 'Footwear', 'Free Items', 'Home', 'Personal Care', 'Sporting Goods']
