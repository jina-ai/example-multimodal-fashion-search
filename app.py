from jina import Flow
from helper import input_docs_from_csv
from config import DEVICE, MAX_DOCS, WORKSPACE_DIR, PORT, CSV_FILE
import click


def index(csv_file=CSV_FILE, max_docs=MAX_DOCS):
    docs = input_docs_from_csv(file_path=csv_file, max_docs=max_docs)

    flow_index = (
        Flow()
        .add(
            uses="jinahub+docker://DocCache", 
            name="deduplicator"
        )
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
        flow_index.index(inputs=docs, show_progress=True)


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
def main(task: str, num_docs: int):
    if task == "index":
        index(max_docs=num_docs)
    elif task == "search":
        search()


if __name__ == "__main__":
    main()
