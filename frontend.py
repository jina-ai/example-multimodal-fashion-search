import streamlit as st
from helper import get_matches, generate_price
from jina import Client, Document
from jina.types.request import Response
from config import PORT, SERVER, TOP_K

title = "👕 Multimodal fashion search with Jina"

st.set_page_config(page_title=title, layout="wide")

# Sidebar
st.sidebar.title("About")
st.sidebar.markdown("""This example lets you use a *textual* description to search through *images* of fashion items using [Jina](https://github.com/jina-ai/jina/)

#### Why does the price change each time?

The dataset doesn't provide pricing info, so it's randomly generated from the frontend on each search""")

st.sidebar.title("Options")
limit = st.sidebar.slider(label="Results", min_value=int(TOP_K/3), max_value=TOP_K*3, value=TOP_K)
# use_hi_res = st.sidebar.checkbox(label="Show hi-res images") # WIP

st.sidebar.markdown("[Repo link](https://github.com/alexcg1/jina-multimodal-fashion-search)")

# Main area
st.title(title)
query = st.text_input(label="Search term", placeholder="Blue dress")

search_button = st.button("Search")

if search_button:
    matches = get_matches(input=query, limit=limit)

if "matches" in locals():
    for match in matches:
        pic_cell, desc_cell, price_cell = st.columns([1,6,1])
        pic_cell.image(match.uri, use_column_width="auto", width=400)
        desc_cell.markdown(f"##### {match.tags['productDisplayName']}")
        desc_cell.markdown(f"*{match.tags['masterCategory']}*, *{match.tags['subCategory']}*, *{match.tags['articleType']}*, *{match.tags['baseColour']}*, *{match.tags['season']}*, *{match.tags['usage']}*")
        price_cell.button(key=match.tags['id'], label=generate_price())

    # This is old way of showing results. Prettier but can't take number of results in account
    # cell1, cell2, cell3, cell4 = st.columns(4)
    # cell5, cell6, cell7, cell8 = st.columns(4)
    # cell9, cell10, cell11, cell12 = st.columns(4)
    # all_cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9, cell10, cell11, cell12]

    # for cell, match in zip(all_cells, matches):
        # cell.image(match.uri, use_column_width="auto")
        # cell.markdown(f"##### {match.tags['productDisplayName']}")
        # cell.markdown(f"*{match.tags['masterCategory']}*")

