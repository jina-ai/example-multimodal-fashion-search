from jina import (
    Document,
    DocumentArray,
    Flow,
)

from helper import input_docs, input_docs_from_csv
from config import DATA_DIR, DEVICE, MAX_DOCS, WORKSPACE_DIR, search_terms, PORT, CSV_FILE
import click


# def index(data_dir=DATA_DIR, max_docs=MAX_DOCS):
def index(csv_file=CSV_FILE, max_docs=MAX_DOCS):
    # docs = input_docs(data_path=data_dir, max_docs=max_docs)
    docs = input_docs_from_csv(file_path=csv_file, max_docs=max_docs)

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
        flow_index.index(inputs=docs)


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

    # grpc
    # with flow_search:
        # docs = DocumentArray()
        # for term in search_terms:
            # doc = Document(text=term)
            # docs.append(doc)

        # resp = flow_search.search(
            # inputs=docs,
            # on_done=plot_search_results,
        # )

    # RESTful
    with flow_search:
        flow_search.port_expose = PORT
        flow_search.protocol = "http"
        flow_search.block()


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "search"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=MAX_DOCS)
@click.option("--force", "-f", is_flag=True)
def main(task: str, num_docs: int, force: bool):
    if task == "index":
        index(max_docs=num_docs)
    elif task == "search":
        search()


if __name__ == "__main__":
    main()
