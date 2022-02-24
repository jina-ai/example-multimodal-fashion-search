from docarray import DocumentArray
from jina import Flow
from helper import get_columns
from config import WORKSPACE_DIR, DIMS, DOCARRAY_PULL_NAME
import pickle


def index_from_cloud(dataset):
    """
    Pull a dataset from Jina Cloud. This will be a DocumentArray with embeddings that someone has pushed there. This saves you having to embed everything yourself, which is computationally expensive.
    """

    print(f"Pulling dataset {dataset}")
    docs = DocumentArray.pull(dataset)

    # Pickle values so search fn can pick up later
    columns = get_columns(docs[0])  # Get all the column info from first doc
    pickle.dump(columns, open("../columns.p", "wb"))

    flow = Flow().add(
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

    with flow:
        docs = flow.index(inputs=docs, show_progress=True, return_results=True)


if __name__ == "__main__":
    index_from_cloud(dataset=DOCARRAY_PULL_NAME)
