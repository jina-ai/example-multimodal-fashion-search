# Run fashion search demo

## Instructions

To run our fashion search demo on your own machine:

1. In root of this repo run `python get_data.py`
2. Come back to `run_fashion_demo` folder
3. `python 1_create_index.py` will download a DocumentArray including about 44,000 fashion image embeddings and create a PQLite index on-disk. You only need to do this **once**.
%%4. `python 2_text_server.py -t <task>` and/or `python 2_image_server.py -t <task>` to start the search servers for text or image search. You'll need to run these **once per session**. When you keep them open users can make multiple search queries to each. `<task>` can be either:
  %%- `search` - opens up RESTful search interface for frontends or `curl` to talk to
  %%- `search_grpc` - runs a test search via gRPC to ensure basic search is working
%%5. Go to `../frontend` and run `streamlit frontend.py` to spin up the frontend.

## Notes

- `x_embed_all_and_push.py` is the file to create embeddings for all the image files in the dataset. This has already been run by Jina and pushed to the cloud, so you don't need to run it. We keep it here as a reference.
