from jina import Flow, Executor, requests, Document
from helper import input_docs_from_csv
import sys

DEVICE = "cpu"

class GetDocCount(Executor):
    @requests
    def get_count(self, docs, **kwargs):
        print(f"\n\nThere are {len(docs)} in the DocumentArray\n\n")


docs = input_docs_from_csv("data/styles.csv", 10)

if sys.argv[1] == "index":
    flow_index = (
        Flow()
        .add(
            uses="jinahub+docker://CLIPImageEncoder",
            name="image_encoder",
            uses_with={"device": "cpu"},
        )
        # .add(uses=GetDocCount)
        .add(
            uses="jinahub://PQLiteIndexer/latest",
            uses_with={
                "dim": 512,
                "metric": "cosine",
                "columns": [
                    ("year", "int"),
                    ("baseColour", "str"),
                    ("masterCategory", "str"),
                ],
                "include_metadata": True,
            },
            uses_metas={"workspace": "./workspace"},
            install_requirements=True,
        )
    )

    with flow_index:
        flow_index.index(inputs=docs, show_progress=True)
    # flow.port_expose=12345
    # flow.protocol="http"
    # flow.block()

elif sys.argv[1] == "search":
    flow_search = (
        Flow()
        .add(
            uses="jinahub+docker://CLIPTextEncoder",
            name="text_encoder",
            uses_with={"device": DEVICE},
            install_requirements=True,
        )
        .add(
            uses="jinahub://PQLiteIndexer/latest",
            uses_with={
                "dim": 512,
                "metric": "cosine",
                "columns": [
                    ("year", "int"),
                    ("baseColour", "str"),
                    ("masterCategory", "str"),
                ],
                "include_metadata": True,
            },
            uses_metas={"workspace": "./workspace"},
            install_requirements=True,
        )
    )

    with flow_search:
        response = flow_search.search(inputs=Document(text="blue shoes"), return_results=True)

    matches = response[0].docs[0].matches
    for match in matches:
        print(match)
