## Instructions

1. `pip install -r requirements.txt`
2. Download dataset from [Kaggle](https://www.kaggle.com/paramaggarwal/fashion-product-images-small) and extract
3. Create a directory called `data`
4. Ensure your `data` dir looks like:

```data
├── images
└── styles.csv
```

5. `python app.py`

Now you'll see Jina index the dataset then pop up images of the default search terms (Dress, shoe, shirt) as specified in `config.py`

## TODO

- Streamlit frontend
- Separate indexing and querying
- Switch out to higher-res dataset for nicer pics
- Index more by default
