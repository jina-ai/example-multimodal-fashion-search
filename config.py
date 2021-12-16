# indexing data
CSV_FILE = "./data/styles.csv"
DATA_DIR = "./data/images"
MAX_DOCS = 100
WORKSPACE_DIR = "workspace"
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
PORT = 12345

# client
TOP_K = 10
IMAGE_RESIZE_FACTOR = 3
