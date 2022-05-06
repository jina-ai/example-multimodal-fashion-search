from jina import Flow
from helper import get_columns, csv_to_docarray
from config import DEVICE, MAX_DOCS, WORKSPACE_DIR, CSV_FILE, DIMS, TIMEOUT_READY
from executor import FashionSearchPreprocessor
import json
import sys
import click

if len(sys.argv) == 2:
    MAX_DOCS = int(sys.argv[1])

with open("columns.json", "r") as file:
    columns = json.load(file)

flow = (
    Flow()
    # .add(, name="preprocessor")
    .add(
        # uses=FashionSearchPreprocessor,
        uses="jinahub://FashionSearchPreprocessor",
        name="preprocessor",
        uses_with={"data_dir": "../data/images/"},
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
            "metric": "cosine",
            "include_metadata": True,
        },
        uses_metas={"workspace": WORKSPACE_DIR},
        volumes=f"./{WORKSPACE_DIR}:/workspace/workspace",
        install_requirements=True,
    )
)


def index(csv_file, num_docs):
    print(f"Indexing {num_docs} documents")
    docs = csv_to_docarray(file_path=csv_file, max_docs=num_docs)

    # Get all the column info from first doc
    columns = get_columns(docs[0])

    # Pickle values so search fn can pick up later
    with open("columns.json", "w") as file:
        json.dump(columns, file)

    with flow:
        docs = flow.index(inputs=docs, show_progress=True, return_results=True)

    print(f"Indexed {len(docs)} Documents")


def search():
    with flow:
        flow.block()


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "search", "search_grpc"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=MAX_DOCS)
def main(task: str, num_docs):
    if task == "index":
        index(CSV_FILE, num_docs=num_docs)
    elif task == "search":
        search()
    else:
        print("Please add '-t index' or '-t search' to your command")


if __name__ == "__main__":
    main()
