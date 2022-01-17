import os

# indexing data
DATA_DIR = "../data/images"

# client
TOP_K = 10
IMAGE_RESIZE_FACTOR = 3
DEBUG = True

# serving via REST - text to image
TEXT_IMAGE_SERVER = os.getenv("TEXT_BACKEND_SERVER", "0.0.0.0")
TEXT_IMAGE_PORT = 12345

# serving via REST - image to image
IMAGE_IMAGE_SERVER = os.getenv("IMAGE_BACKEND_SERVER", "0.0.0.0")
IMAGE_IMAGE_PORT = 60000
