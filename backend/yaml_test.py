from jina import Flow
from docarray import Document, DocumentArray

flow = Flow.load_config("flow.yml")

docs = DocumentArray.empty(10)

docs.summary()

with flow:
    flow.block()
