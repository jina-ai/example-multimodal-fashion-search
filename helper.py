import glob
import os
from jina import Document
import matplotlib.pyplot as plt
from jina.types.request import Request
from config import MAX_DOCS

search_terms = ("Dress", "Shirt", "Shoe")


def plot_search_results(resp: Request):
    for doc in resp.docs:
        print(f'Query text: {doc.text}')
        print(f'Matches:')
        print('-'*10)
        show_docs(doc.matches[:3])

def input_docs(data_path):
    for fn in glob.glob(os.path.join(data_path, '*'))[:MAX_DOCS]:
        doc = Document(uri=fn, tags={'filename': fn})
        doc.load_uri_to_image_blob()
        yield doc 

def show_docs(docs):
  for doc in docs:
      plt.imshow(doc.blob)
      plt.show()

