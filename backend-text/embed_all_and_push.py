from jina import Flow
from helper import input_docs_from_csv
from config import DEVICE, CSV_FILE, TIMEOUT_READY

MAX_DOCS = 999999

pushed_name = "fashion-product-images-clip-all"

def embed_docs(csv_file=CSV_FILE, max_docs=MAX_DOCS):
    docs = input_docs_from_csv(file_path=csv_file, max_docs=max_docs)

    flow = (
        Flow()
        .add(
            uses=f"jinahub://CLIPImageEncoder/v0.4",
            name="image_encoder",
            uses_with={"device": DEVICE},
            install_requirements=True,
            uses_metas={"timeout_ready": TIMEOUT_READY},
            replicas=2,
        )
        # .add(
            # uses="jinahub://PQLiteIndexer/latest",
            # name="indexer",
            # uses_with={
                # "dim": DIMS,
                # "columns": columns,
                # "metric": "cosine",
                # "include_metadata": True,
            # },
            # uses_metas={"workspace": WORKSPACE_DIR},
            # volumes=f"./{WORKSPACE_DIR}:/workspace/workspace",
            # install_requirements=True,
        # )
    )

    with flow:
        docs = flow.index(inputs=docs, show_progress=True, return_results=True)

    return docs

embedded_docs = embed_docs()

for doc in embedded_docs:
    doc.tensor = None

embedded_docs.push(pushed_name)
