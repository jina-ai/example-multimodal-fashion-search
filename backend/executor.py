from jina import Executor, DocumentArray, requests
import os
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

    @requests(on=["/index", "/update"])
    def process_index_document(self, docs: DocumentArray, **kwargs):
        # docs.apply(self._debug)
        for doc in docs:
            self._preproc(doc)
            self._add_metadata(doc)
        # docs.apply(self._preproc)
        # docs.apply(self._add_metadata)

    @requests(on="/search")
    def process_search_document(self, docs: DocumentArray, **kwargs):
        for doc in docs:
            doc = self._preproc(doc)

    def _generate_price(self):
        price = random.randrange(self.price_range[0], self.price_range[1])

        return price

    def _debug(self, doc):
        if type(doc) is None:
            print("It's none")
            breakpoint()
        if hasattr(doc, "id"):
            print(doc.uri)
        else:
            print(doc)
            print("wtf")
            breakpoint()


    def _preproc(self, doc):
        # if doc.uri:
        if hasattr(doc, "id"):
            print(doc.uri)

            if os.path.isfile(doc.uri):
                doc.load_uri_to_image_tensor()

                # Apply settings to tensor
                doc.tensor = doc.tensor.astype(np.uint8)
                doc.set_image_tensor_shape(shape=self.tensor_shape)
                doc.set_image_tensor_normalization()

                doc.convert_uri_to_datauri()
                return doc
            else:
                print(f"Can't find {doc.uri}")
                del doc
        else:
            print(doc)
            print("wtf")
            breakpoint()


    # def _preproc(self, doc):
        # doc.load_uri_to_image_tensor()

        # # Apply settings to tensor
        # doc.tensor = doc.tensor.astype(np.uint8)
        # doc.set_image_tensor_shape(shape=self.tensor_shape)
        # doc.set_image_tensor_normalization()

        # doc.convert_uri_to_datauri()
        # return doc


    def _add_metadata(self, doc):
        # Generate fake price
        if self.price_range:
            doc.tags["price"] = self._generate_price()

        # Generate fake rating based on id
        if self.rating_range:
            random.seed(int(doc.id))  # Ensure reproducability
            doc.tags["rating"] = random.randrange(
                self.rating_range[0], self.rating_range[1]
            )

        # Store original file info
        doc.tags["original_filename"] = f"{doc.id}.{self.file_ext}"
        doc.tags["original_uri"] = f"{self.data_dir}/{doc.id}.{self.file_ext}"

        return doc
