import os
import subprocess
import sys
from zipfile import ZipFile
import shutil
import csv

data_dir = "../data"
dataset_name = "paramaggarwal/fashion-product-images-small"
filename = "fashion-product-images-small.zip"
csv_filename = "styles.csv"


def filter_good_rows(
    desired_field_count=10, input_file=csv_filename, output_file=f"fixed_styles.csv"
):
    """
    Some CSVs may have different number of fields per row, which really messes up doc.tags. We'll remove these malformed rows
    """
    good_list = []
    wtflist = []

    # Get fields
    with open(input_file, "r") as file:
        fields_string = file.readlines()[0]
        fields_list = fields_string.split(",")
        fields_list = [field.strip() for field in fields_list]

    with open(output_file, "w") as file:
        file.write(fields_string)

    with open(input_file, "r") as in_file, open(output_file, "a") as out_file:
        reader = csv.DictReader(in_file)

        writer = csv.DictWriter(out_file, fieldnames=fields_list)
        for row in reader:
            if len(row.keys()) == desired_field_count:
                good_list.append(row)
                writer.writerow(row)
            else:
                wtflist.append(row)

    print(f"GOOD: {len(good_list)} rows with {desired_field_count} keys")
    print(f"BAD: {len(wtflist)} rows with weird number of keys")


if not os.path.isfile(f"{os.path.expanduser('~')}/.kaggle/kaggle.json"):
    print(
        "1. Please create a Kaggle account to download the dataset: https://www.kaggle.com/ \n2. Ensure ~/.kaggle/kaggle.json exists"
    )
    sys.exit()

if not os.path.isdir(data_dir):
    os.mkdir(data_dir)

os.chdir(data_dir)

if not os.path.isdir("images"):
    print("- Downloading dataset")
    subprocess.run(["kaggle", "datasets", "download", dataset_name])

    print("- Unzipping dataset")
    with ZipFile(filename, "r") as zipfile:
        zipfile.extractall(".")

    print("- Deleting unused files to free up space")
    shutil.rmtree("myntradataset")

    print("- Deleting zip file")
    os.remove(filename)

print("- Removing malformed rows")
filter_good_rows()

print(f"- Deleting original {csv_filename}")
os.remove(csv_filename)

print(f"- Renaming sanitized CSV to {csv_filename}")
os.rename("fixed_styles.csv", csv_filename)
