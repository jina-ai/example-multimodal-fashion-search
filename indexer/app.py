from jina import Flow
from helper import get_columns, csv_to_docarray
from config import DEVICE, MAX_DOCS, WORKSPACE_DIR, CSV_FILE, DIMS, TIMEOUT_READY
import json
import sys

if DEVICE == "cuda":
    gpu_bool = "-gpu"
else:
    gpu_bool = ""

if len(sys.argv) == 2:
    MAX_DOCS = int(sys.argv[1])

print(f"Indexing {MAX_DOCS} documents")

def index(csv_file, max_docs):
    docs = csv_to_docarray(file_path=csv_file, max_docs=max_docs)

    # Get all the column info from first doc
    columns = get_columns(docs[0])  

    # Pickle values so search fn can pick up later
    with open("columns.json", "w") as file:
        json.dump(columns, file)

    flow = (
        Flow()
        .add(
            uses=f"jinahub://CLIPEncoder/v0.3.0{gpu_bool}",
            name="encoder",
            uses_with={"device": DEVICE},
            install_requirements=True,
            uses_metas={"timeout_ready": TIMEOUT_READY},
            # replicas=2,
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

    with flow:
        docs = flow.index(inputs=docs, show_progress=True, return_results=True)

    print(f"Indexed {len(docs)} Documents")


if __name__ == "__main__":
    index(csv_file=CSV_FILE, max_docs=MAX_DOCS)
