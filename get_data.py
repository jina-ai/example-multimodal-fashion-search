import os
import subprocess
import sys
from zipfile import ZipFile

data_dir = "data"
dataset_name = "paramaggarwal/fashion-product-images-small"
filename = "fashion-product-images-small.zip"

if not os.path.isfile(f"{os.path.expanduser('~')}/.kaggle/kaggle.json"):
    print(
        "1. Please create a Kaggle account to download the dataset: https://www.kaggle.com/ \n2. Ensure ~/.kaggle/kaggle.json exists"
    )
    sys.exit()

if not os.path.isdir(data_dir):
    os.mkdir(data_dir)

os.chdir(data_dir)

subprocess.run(["kaggle", "datasets", "download", dataset_name])

with ZipFile(filename, "r") as zipfile:
    zipfile.extractall(".")

os.remove(filename)
