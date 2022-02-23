from docarray import Document, DocumentArray
from jina import Flow
from helper import input_docs_from_csv, get_columns
from config import DEVICE, MAX_DOCS, WORKSPACE_DIR, PORT, CSV_FILE, DIMS, TIMEOUT_READY
import click
import pickle

if DEVICE == "cuda":
    gpu_bool = "-gpu"
else:
    gpu_bool = ""

def index_from_pulled_docarray():
    # docs = input_docs_from_csv(file_path=csv_file, max_docs=max_docs)
    docs = DocumentArray.pull(f'fashion-multimodal-{MAX_DOCS}')

    columns = get_columns(docs[0])  # Get all the column info from first doc
    pickle.dump(
        columns, open("../columns.p", "wb")
    )  # Pickle values so search fn can pick up later

    flow = (
        Flow()
        # .add(
            # uses=f"jinahub://CLIPImageEncoder/v0.4{gpu_bool}",
            # name="image_encoder",
            # uses_with={"device": DEVICE},
            # install_requirements=True,
            # uses_metas={"timeout_ready": TIMEOUT_READY},
        # )
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

    with flow:
        docs = flow.index(inputs=docs, show_progress=True, return_results=True)

    docs.push(f'fashion-multimodal-{MAX_DOCS}')



def index(csv_file=CSV_FILE, max_docs=MAX_DOCS):
    docs = input_docs_from_csv(file_path=csv_file, max_docs=max_docs)

    columns = get_columns(docs[0])  # Get all the column info from first doc
    pickle.dump(
        columns, open("../columns.p", "wb")
    )  # Pickle values so search fn can pick up later

    flow = (
        Flow()
        .add(
            uses=f"jinahub://CLIPImageEncoder/v0.4{gpu_bool}",
            name="image_encoder",
            uses_with={"device": DEVICE},
            install_requirements=True,
            uses_metas={"timeout_ready": TIMEOUT_READY},
            replicas=2,
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

    with flow:
        docs = flow.index(inputs=docs, show_progress=True, return_results=True)

    print(docs)
    docs.push(f'fashion-multimodal-{MAX_DOCS}')


def search():
    columns = pickle.load(open("../columns.p", "rb"))
    flow = (
        Flow(protocol="http", port_expose=PORT)
        .add(
            uses="jinahub://CLIPTextEncoder/v0.2{gpu_bool}",
            name="text_encoder",
            uses_with={"device": DEVICE},
            install_requirements=True,
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

    with flow:
        flow.block()


def search_grpc():
    columns = pickle.load(open("../columns.p", "rb"))
    flow = (
        Flow()
        .add(
            uses="jinahub://CLIPTextEncoder/v0.2",
            name="text_encoder",
            uses_with={"device": DEVICE},
            install_requirements=True,
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

    with flow:
        response = flow.search(Document(text="shoes"), return_results=True)
        print([match.uri for match in response[0].matches])


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "search", "search_grpc"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=MAX_DOCS)
def main(task: str, num_docs: int):
    if task == "index":
        index(csv_file=CSV_FILE, max_docs=num_docs)
    elif task == "search":
        search()
    elif task == "search_grpc":
        search_grpc()


if __name__ == "__main__":
    main()
