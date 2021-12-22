# Multimodal Fashion Search with Jina

![](./demo.gif)

Multimodal search lets you use one type of data (in this case, text) to search another type of data (in this case, images). This example leverages core Jina technologies that make it simpler to build and run your search, including:

- Executors from [Jina Hub](https://hub.jina.ai), so we don't have to manually integrate deep learning models
- [Jina Client](https://docs.jina.ai/api/jina.clients/), so we don't have to worry about how best to format the REST request

## Instructions

### Download data

1. Download dataset from [Kaggle](https://www.kaggle.com/paramaggarwal/fashion-product-images-small) and extract
2. Create a directory called `data`
3. Ensure your `data` directory looks like:

```data
├── images
└── styles.csv
```

### Run backend

1. `cd backend`
2. `pip install -r requirements.txt`
3. `python app.py -t index -n 10` (where `10` is the number of files you want to index)
4. `python app.py -t search`

### Run frontend

1. Open a new terminal window/tab, return to same directory
2. `cd frontend`
3. `pip install -r requirements.txt`
4. `streamlit run frontend.py`

## With Docker-compose

`docker-compose up`

## TODO

- [X] Streamlit frontend
- [X] Separate indexing and querying
- [X] Index more by default
- [ ] Switch out to higher-res dataset for nicer pics
