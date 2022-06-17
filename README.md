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

## Run on JCloud

If you want to deploy to JCloud yourself:

- `pip install jcloud`
- Login: `jc login`
- Deploy: `jc deploy backend/jcloud/flow.yml`
- Make a note of your server information

### Index data

- Edit `CLOUD_HOST` in `backend/config.py` to match the server info above
- Download data: `python ./get_data.py`
- Index: `python app.py -t cloud_index -n <300>` where 300 is the number of docs you wish to index

### Search in front-end

- Edit `docker-compose-jcloud.yml` to reflect server info
- Start frontend: `docker-compose -f docker-compose-jcloud.yml up`
