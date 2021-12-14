import glob
import os
from docarray.array.document import DocumentArray
import matplotlib.pyplot as plt
from jina.types.request import Request
from config import MAX_DOCS, SERVER, PORT, DATA_DIR
from jina import Client, Document

search_terms = ("Dress", "Shirt", "Shoe")

# Server

def plot_search_results(resp: Request):
    for doc in resp.docs:
        print(f'Query text: {doc.text}')
        print(f'Matches:')
        print('-'*10)
        show_docs(doc.matches[:3])

def input_docs(data_path, max_docs):
    for fn in glob.glob(os.path.join(data_path, '*'))[:MAX_DOCS]:
        doc = Document(uri=fn, tags={'filename': fn})
        doc.load_uri_to_image_blob()
        yield doc 

def input_docs_from_csv(file_path, max_docs):
    docs = DocumentArray()
    import csv
    from itertools import islice
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in islice(reader, max_docs):
            filename = f"{DATA_DIR}/{row['id']}.jpg"
            doc = Document(uri=filename, tags=row)
            doc.load_uri_to_image_blob()
            docs.append(doc)

    return docs

def show_docs(docs):
  for doc in docs:
      plt.imshow(doc.blob)
      plt.show()


# Client

def get_matches(input, server=SERVER, port=PORT, max_docs=20):
    client = Client(host=SERVER, protocol="http", port=PORT)
    response = client.search(Document(text=input), return_results=True)
    matches = response[0].docs[0].matches

    return matches
