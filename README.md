# Multimodal Fashion Search with Jina

![](./demo.gif)

Multimodal search lets you use one type of data (in this case, text) to search another type of data (in this case, images). This example leverages core Jina technologies that make it simpler to build and run your search, including:

- Executors from [Jina Hub](https://hub.jina.ai), so we don't have to manually integrate deep learning models
- [Jina Client](https://docs.jina.ai/api/jina.clients/), so we don't have to worry about how best to format the REST request

## Instructions

1. `pip install -r requirements.txt`
2. Download dataset from [Kaggle](https://www.kaggle.com/paramaggarwal/fashion-product-images-small) and extract
3. Create a directory called `data`
4. Ensure your `data` directory looks like:

```data
├── images
└── styles.csv
```

5. `python app.py -t index -n 10` (where `10` is the number of files you want to index)
6. `python app.py -t search`
7. Open a new terminal window/tab, return to same directory
8. `streamlit run frontend.py`

## TODO

- [X] Streamlit frontend
- [X] Separate indexing and querying
- [X] Index more by default
- [ ] Switch out to higher-res dataset for nicer pics
