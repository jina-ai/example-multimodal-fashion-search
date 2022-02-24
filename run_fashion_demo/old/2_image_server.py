from jina import Flow
from docarray import Document
from config import DEVICE, WORKSPACE_DIR, PORT, DIMS
import click
import pickle

columns = pickle.load(open("../columns.p", "rb"))

# We only use one Flow for searching by image, since we already created our embeddings when we ran `app.py -t index` from `backend-text`

flow = (
    Flow(port_expose=PORT, protocol="http")
    .add(
        uses="jinahub://CLIPImageEncoder/",
        name="text_encoder",
        uses_with={"device": DEVICE},
        install_requirements=True,
    )
    .add(
        uses="jinahub://PQLiteIndexer/",
        name="indexer",
        uses_with={
            "dim": DIMS,
            "columns": columns,
            "metric": "cosine",
            "include_metadata": True,
        },
        uses_metas={"workspace": WORKSPACE_DIR},
        volumes=f"./{WORKSPACE_DIR}:/workspace/workspace",
        install_requirements=True,
    )
)


def search():
    with flow:
        flow.block()


def search_grpc():

    query_doc = Document(uri="../data/images/20000.jpg")
    query_doc.load_uri_to_image_tensor()

    with flow:
        response = flow.search(query_doc, return_result=True)

    print([match.uri for match in response[0].matches])


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "search", "search_grpc"], case_sensitive=False),
)
def main(task: str):
    if task == "search":
        search()
    elif task == "search_grpc":
        search_grpc()


if __name__ == "__main__":
    main()
