from jina import Flow
from docarray import DocumentArray
from helper import get_columns
from config import MAX_DOCS, WORKSPACE_DIR, CSV_FILE, DIMS, TIMEOUT_READY
from executor import FashionSearchPreprocessor
import json
import click

# Load existing column schema - needed for PQLiteIndexer
with open("columns.json", "r") as file:
    columns = json.load(file)

flow = (
    Flow(port_expose=12345, protocol="http")
    .add(
        # uses=FashionSearchPreprocessor,
        uses="jinahub://FashionSearchPreprocessor/v0.4",
        name="preprocessor",
        uses_with={
            "data_dir": "../data/images/",
            "tensor_shape": (80, 60),
            "rating_range": (0, 5),
            "price_range": (0, 200),
        },
    )
    .add(
        uses="jinahub://CLIPEncoder/v0.3.0",
        name="encoder",
        install_requirements=True,
        uses_metas={"timeout_ready": TIMEOUT_READY},
    )
    .add(
        name="TensorDeleter",
        uses="jinahub://TensorDeleter",
    )
    .add(
        uses="jinahub://PQLiteIndexer/latest",
        name="indexer",
        uses_with={
            "dim": DIMS,
            "columns": columns,
            # "metric": "cosine",
            # "include_metadata": True,
        },
        uses_metas={"workspace": WORKSPACE_DIR},
        volumes=f"./{WORKSPACE_DIR}:/workspace/workspace",
        install_requirements=True,
    )
)


def index(csv_file, num_docs):
    print(f"Indexing {num_docs} documents")
    docs = DocumentArray.from_csv(csv_file, size=num_docs)

    # Commented code doesn't really work since doesn't pull metadata that is created by FashionSearchPreprocessor
    # Get all the column info from first doc
    # columns = get_columns(docs[0])

    # Pickle values so search fn can pick up later
    # with open("columns.json", "w") as file:
    # json.dump(columns, file)

    with flow:
        docs = flow.index(inputs=docs, show_progress=True, return_results=True)

    docs.summary()


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
    type=click.Choice(["index", "serve"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=MAX_DOCS)
def main(task: str, num_docs):
    if task == "index":
        index(CSV_FILE, num_docs=num_docs)
    elif task == "serve":
        serve()
    else:
        print("Please add '-t index' or '-t serve' to your command")


if __name__ == "__main__":
    main()
