from jina import (
    Document,
    DocumentArray,
    Flow,
)

from helper import input_docs, plot_search_results
from config import DATA_DIR, DEVICE, WORKSPACE_DIR, search_terms


def index():
    docs = input_docs(DATA_DIR)

    flow_index = (
        Flow()
        .add(
            uses="jinahub+docker://CLIPImageEncoder",
            name="image_encoder",
            uses_with={"device": DEVICE},
            install_requirements=True,
        )
        .add(
            uses="jinahub+docker://SimpleIndexer",
            name="indexer",
            workspace="workspace",
            uses_with={"index_file_name": "index"},
            uses_metas={"workspace": WORKSPACE_DIR},
            volumes=f"./{WORKSPACE_DIR}:/workspace/workspace",
            install_requirements=True,
        )
    )

    with flow_index:
        flow_index.index(inputs=docs, request_size=1)


def search():
    flow_search = (
        Flow()
        .add(
            uses="jinahub+docker://CLIPTextEncoder",
            name="text_encoder",
            uses_with={"device": DEVICE},
            install_requirements=True,
        )
        .add(
            uses="jinahub+docker://SimpleIndexer",
            name="indexer",
            workspace="workspace",
            uses_with={"index_file_name": "index"},
            uses_metas={"workspace": WORKSPACE_DIR},
            volumes=f"./{WORKSPACE_DIR}:/workspace/workspace",
            install_requirements=True,
        )
    )

    with flow_search:
        docs = DocumentArray()
        for term in search_terms:
            doc = Document(text=term)
            docs.append(doc)

        resp = flow_search.search(
            inputs=docs,
            on_done=plot_search_results,
        )


index()
search()
