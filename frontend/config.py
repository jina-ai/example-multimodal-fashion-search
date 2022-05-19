import os

# data directory
DATA_DIR = "../data/images"

# client
TOP_K = 10
IMAGE_RESIZE_FACTOR = 3
DEBUG = True

# serving via REST
IMAGE_ROOT_URL = "https://examples.jina.ai/data/fashion/images/" # where are the image files?
SERVER = os.getenv("SERVER", "https://0df596d980.wolf.jina.ai")
# PORT = 12345
