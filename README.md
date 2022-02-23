# Multimodal Fashion Search with Jina

![](./demo.gif)

Multimodal search lets you use one type of data (in this case, text) to search another type of data (in this case, images). This example leverages core Jina technologies that make it simpler to build and run your search, including:

- **[Jina Hub](https://hub.jina.ai)** Executors, so we don't have to manually integrate deep learning models
- **[Jina Client](https://docs.jina.ai/api/jina.clients/)**, so we don't have to worry about how best to format the REST request
- **[PQLite](https://hub.jina.ai/executor/pn1qofsj)** allowing us to pre-filter results by season, price, rating, etc

The front-end is built in [Streamlit](https://streamlit.io/).

## Instructions

### Download data

Run `python get_data.py`

### Index data using `backend-text`

To be honest, it was arbitrary where to put the indexing code. But I wanted to stay DRY so only did it in one place

1. `cd backend-text`
2. `pip install -r requirements.txt`
3. `python app.py -t index -n 10` (where `10` is the number of files you want to index)

### Start search Flows

Depending on which Flows you want you can spin up RESTful interface(s) for the frontend to talk to:

1. `cd backend-<image/text>`
2. `python app.py -t search`

Both of these Flows use the same index, but have different ports for the frontend to talk to. If you want both image and text search you'll have to run both search Flows.

### Run frontend

1. Open a new terminal window/tab, return to same directory
2. `cd frontend`
3. `pip install -r requirements.txt`
4. `streamlit run frontend.py`

## With Docker-compose

1. First index the data as stated above
2. In the repo's root directory, run `docker-compose up` 

## Tips

- Index using the [small dataset](https://www.kaggle.com/paramaggarwal/fashion-product-images-small), then swap out the data directory for that of the [hi-res dataset](https://www.kaggle.com/paramaggarwal/fashion-product-images-dataset) for nicer-looking results.

## Debugging

### Search using gRPC

This is a good way to test quickly, instead of going through frontend. It'll take either a string ("shoes") or one of the images from the dataset (depending on whether you do image or text search) and use that as a query.

1. Index your data
2. `cd backend-text` or `cd backend-image`
3. `pip install -r requirements.txt`
4. `python app.py -t search_grpc`

It should then print out the `uri`s of the matching Documents.

## TODO

- [X] Streamlit frontend
- [X] Separate indexing and querying
- [X] Index more by default
- [X] Add image-to-image search
- [X] Switch out to higher-res dataset for nicer pics (on examples.jina.ai only)
