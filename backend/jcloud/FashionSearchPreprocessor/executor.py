from jina import Executor, DocumentArray, requests
import numpy as np
import random


class FashionSearchPreprocessor(Executor):
    def __init__(
        self,
        data_dir="./data",
        tensor_shape=(80, 60),
        rating_range=(0, 5),
        price_range=(10, 200),
        file_ext="jpg",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.data_dir = data_dir
        self.tensor_shape = tensor_shape
        self.price_range = price_range
        self.rating_range = rating_range
        self.file_ext = file_ext

    @requests(on="/index")
    def process_index_document(self, docs: DocumentArray, **kwargs):
        for doc in docs:
            doc = self._generate_uri(doc)
            doc = self._preproc(doc)
            doc = self._add_metadata(doc)

    @requests(on="/search")
    def process_search_document(self, docs: DocumentArray, **kwargs):
        for doc in docs:
            doc = self._preproc(doc)
            print(doc)

    def _generate_price(self):
        price = random.randrange(self.price_range[0], self.price_range[1])

        return price

    def _generate_uri(self, doc):
        doc.uri = f"{self.data_dir}/{doc.id}.{self.file_ext}"

        return doc

    def _preproc(self, doc):
        if not doc.text:
            # ensure we have a tensor
            if doc.uri:
                doc.load_uri_to_image_tensor()
            elif doc.blob:
                doc.convert_blob_to_image_tensor()

            # Apply settings to tensor
            doc.tensor = doc.tensor.astype(np.uint8)
            doc.set_image_tensor_shape(shape=self.tensor_shape)
            doc.set_image_tensor_normalization()

        return doc

    def _add_metadata(self, doc):
        # Fix uri
        # if not self.data_dir:
        # self.data_dir = "."

        # if hasattr(doc, "id"):
        # filename = f"{self.data_dir}/{doc.id}.jpg"
        # doc.uri = filename

        # Generate fake price
        if self.price_range:
            doc.tags["price"] = self._generate_price()

        # Generate fake rating based on id
        if self.rating_range:
            random.seed(int(doc.id))  # Ensure reproducability
            doc.tags["rating"] = random.randrange(
                self.rating_range[0], self.rating_range[1]
            )

        return doc
