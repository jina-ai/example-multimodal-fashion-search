from config import IMAGE_ROOT_URL
from executors import FashionSearchPreprocessor
import os


def process_docs(docs):

    preproc = FashionSearchPreprocessor()
    preproc.process_index_document(docs)

    # Some rows in our CSV may contain refs to files that don't exist. Let's remove those Documents
    for doc in docs:
        if os.path.isfile(doc.uri):
            add_image_url(doc)
        else:
            print(f"{doc.uri} can't be found. Removing")
            del docs[doc.id]


def add_image_url(doc):
    filename = doc.uri.split("/")[-1]
    doc.tags["image_url"] = f"{IMAGE_ROOT_URL}{filename}"


def print_results(docs, show_summary=True, show_matches=True, **kwargs):
    """
    Print results
    """
    if show_summary:
        docs.summary()
    for doc in docs:
        if show_matches:
            for match in doc.matches:
                print(match.uri)
                print(match.tags)
