# indexing data
DATA_DIR = "../data/images" # Where are the files?
CSV_FILE = "../data/styles.csv" # Where's the metadata?
WORKSPACE_DIR = "../embeddings" # So we can share index with text-to-image backend
MAX_DOCS = 100
DEVICE = "cpu"

# PQLiteIndexer
COLUMNS = [
    ("gender", "str"),
    ("masterCategory", "str"),
    ("subCategory", "str"),
    ("articleType", "str"),
    ("baseColour", "str"),
    ("season", "str"),
    ("usage", "str"),
    ("year", "int"),
]
DIMS = 512 # This should be same shape as vector embedding

# searching via gRPC
search_terms = ("Dress", "Shirt", "Shoe")

# serving via REST
SERVER = "0.0.0.0" # remove http://
PORT = 60000
