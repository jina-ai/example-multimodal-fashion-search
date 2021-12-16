from jina import Flow, Executor, requests
from helper import input_docs_from_csv

class GetDocCount(Executor):
    @requests
    def get_count(self, docs, **kwargs):
        print(f"\n\nThere are {len(docs)} in the DocumentArray\n\n")


docs = input_docs_from_csv("data/styles.csv", 10)


flow = (
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

with flow:
    flow.index(inputs=docs, show_progress=True)
    flow.port_expose=12345
    flow.protocol="http"
    flow.block()
