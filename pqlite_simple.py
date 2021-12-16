from jina import Flow, Executor, requests, Document, Client
from helper import input_docs_from_csv


class DimGetter(Executor):
    @requests
    def get_dims(self, docs, **kwargs):
        print(docs[0].embedding.shape)


def get_matches(input, server=SERVER, port=PORT, limit=MAX_DOCS):
    client = Client(host=server, protocol="http", port=port)
    response = client.search(
        Document(text=input),
        return_results=True,
        parameters={"limit": limit},
        show_progress=True,
    )
    matches = response[0].docs[0].matches

    return matches


docs = input_docs_from_csv("data/styles.csv", 10)


flow = (
    Flow()
    .add(
        uses="jinahub+docker://CLIPImageEncoder",
        name="image_encoder",
        uses_with={"device": "cpu"},
    )
    .add(
        uses=DimGetter,
        # name="image_encoder",
        # uses_with={"device": "cpu"},
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

query = Document(text="blue dress")

with flow:
    flow.index(inputs=docs, show_progress=True)
    results = flow.search(inputs=query, return_results=True)
