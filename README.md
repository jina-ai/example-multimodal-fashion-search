# Multimodal Fashion Search with Jina

![](./.github/images/demo.gif)

Multimodal search lets you use one type of data (in this case, text) to search another type of data (in this case, images). This example leverages core Jina technologies that make it simpler to build and run your search, including:

- **[DocumentArray](https://docarray.jina.ai)** - let's us concurrently process Documents and push/pull them between machines. Useful for creating embeddings on remote machine with GPU and then indexing and querying locally
- **[Jina Hub](https://hub.jina.ai)** Executors, so we don't have to manually integrate deep learning models
- **[Jina Client](https://docs.jina.ai/api/jina.clients/)**, so we don't have to worry about how best to format the REST request
- **[PQLite](https://hub.jina.ai/executor/pn1qofsj)** allowing us to pre-filter results by season, price, rating, etc

The front-end is built in [Streamlit](https://streamlit.io/).

## Play with the search engine now

We've got a [live demo](https://examples.jina.ai/fashion) for you to play with.

## Run the fashion search engine yourself

There are multiple ways you can run this:

- Deploy on [JCloud](https://github.com/jina-ai/jcloud/)
- Run with Docker-Compose
- Run on bare metal

### First steps

- **Clone this repo**: `git clone https://github.com/jina-ai/example-multimodal-fashion-search.git`
- **Download data**: `python ./get_data.py`

### Run on JCloud

JCloud lets you run the fashion backend Jina Flow on the cloud, without having to use your own compute.

```sh
pip install jcloud
cd backend
jc login
jc deploy jcloud
```

After that you can use [Jina Client](https://docs.jina.ai/fundamentals/flow/client/#connect-client-to-a-flow) to connect and search/index your data.

### Run with Docker-Compose

This will spin up:

- Indexer: saves embeddings and metadata to `/backend/workspace`. You can tweak how many Documents to index in `docker-compose.yml`. You can also comment out the `backend-index` section in `docker-compose.yml` if you've already indexed and don't want to re-index.
- Searcher: searches the embeddings/metadata stored on disk
- Frontend: Streamlit frontend to make user experience easier

```sh
docker-compose up
```

### Run on bare metal

```sh
pip install -r requirements.txt
```

Then, in `backend`:

- **Build your index**: `python app.py -t index -n 1000 # index 1000 images`
- **Open up RESTful interface for searching/indexing**: `python app.py -t serve`

To open the frontend, go to the `frontend` directory and run `streamlit run frontend.py`

## Tips

- Index using the [small dataset](https://www.kaggle.com/paramaggarwal/fashion-product-images-small), then swap out the `data` directory for that of the [hi-res dataset](https://www.kaggle.com/paramaggarwal/fashion-product-images-dataset) for nicer-looking results.

## Troubleshooting

### I get the error `stacks: "sqlite3.IntegrityError: UNIQUE constraint failed: table_0._doc_id\n"`

This is because you're trying to index data that's already been indexed. The database we use has a `UNIQUE` constraint that means it won't index duplicate data. You can fix this by:

- Deleting `backend/workspace` (this will delete your entire index)
- Commenting out the `backend-index` section from `docker-compose.yml`
