# indexing data
DOCARRAY_PULL_NAME = 'fashion-multimodal-all'
DATA_DIR = "../data/images" # Where are the files?
CSV_FILE = "../data/styles.csv" # Where's the metadata?
WORKSPACE_DIR = "../embeddings"
MAX_DOCS = 99999999
DEVICE = "cpu"

# PQLiteIndexer
DIMS = 512 # This should be same shape as vector embedding

# serving via REST
PORT = 12345

# metas for executors
TIMEOUT_READY = -1 # Wait forever for executor to be ready. Good for slow connections
