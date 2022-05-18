from jina import Flow, Client
from docarray import DocumentArray, Document
from helper import process_docs, print_results
from config import MAX_DOCS, CSV_FILE, CLOUD_HOST
import click

flow = Flow.load_config("flow.yml")


def index(csv_file, num_docs):
    print(f"Indexing {num_docs} documents")
    docs = DocumentArray.from_csv(csv_file, size=num_docs)

    with flow:
        docs = flow.index(inputs=docs, show_progress=True, return_results=True)

    print_results(docs, show_matches=False)


def cloud_index(host, csv_file, num_docs):
    client = Client(host=host)
    docs = DocumentArray.from_csv(csv_file, size=num_docs)
    process_docs(docs)
    client.post("/update", docs, show_progress=True)


def cloud_search(host):
    query = input("What do you want to search? ")
    client = Client(host=host)
    doc = Document(text=query)

    response = client.search(doc, show_progress=True)

    print_results(response)


def serve():
    """
    Open RESTful front-end for searching or indexing
    """
    with flow:
        flow.block()


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(
        ["index", "serve", "cloud_index", "cloud_search"], case_sensitive=False
    ),
)
@click.option("--num_docs", "-n", default=MAX_DOCS)
def main(task: str, num_docs):
    if task == "index":
        index(CSV_FILE, num_docs=num_docs)
    elif task == "cloud_index":
        cloud_index(host=CLOUD_HOST, csv_file=CSV_FILE, num_docs=num_docs)
    elif task == "cloud_search":
        cloud_search(host=CLOUD_HOST)
    elif task == "serve":
        serve()
    else:
        print("Please add '-t index' or '-t serve' to your command")


if __name__ == "__main__":
    main()
