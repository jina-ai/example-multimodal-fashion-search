from docarray import Document
from jina import Flow
from config import (
    DEVICE,
    WORKSPACE_DIR,
    PORT,
    DIMS,
)
import click
import json

if DEVICE == "cuda":
    gpu_bool = "-gpu"
else:
    gpu_bool = ""

with open("columns.json", "rt") as file:
    columns = json.load(file)

flow = (
    Flow(protocol="http", port_expose=PORT)
    .add(
        uses=f"jinahub://CLIPEncoder/v0.3.0{gpu_bool}",
        name="text_encoder",
        uses_with={"device": DEVICE},
        install_requirements=True,
    )
    .add(
        uses="jinahub://PQLiteIndexer/v0.2.5",
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


def test_text():
    with flow:
        response = flow.search(Document(text="shoes"), return_results=True)

    print([match.uri for match in response[0].matches])


def test_image():
    query_doc = Document(uri="../data/images/20000.jpg")
    query_doc.load_uri_to_image_tensor()

    with flow:
        response = flow.search(query_doc, return_result=True)

    print([match.uri for match in response[0].matches])


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["search", "test_text", "test_image"], case_sensitive=False),
)
def main(task: str):
    if task == "search":
        search()
    elif task == "test_text":
        test_text()
    elif task == "test_image":
        test_image()


if __name__ == "__main__":
    main()
