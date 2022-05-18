The does the following:

1. Creates a DocumentArray from a given dataset
2. Creates embeddings for each Document in the DocumentArray using CLIPImageEncoder. These can later be searched with *any* CLIP Encoder since they have a shared embedding space
3. Stores Documents with embeddings in `../embeddings` using PQLiteIndexer

## Next steps

Search the index using the text or image search backends and Streamlit frontend
