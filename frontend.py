import streamlit as st
from helper import get_matches
from jina import Client, Document
from jina.types.request import Response
from config import PORT, SERVER

title = "Multimodal fashion search with Jina"

st.set_page_config(page_title=title, layout="wide")
st.title(title)

query = st.text_input(label="Search term", placeholder="Blue dress")

search_button = st.button("Search")

if search_button:
    matches = get_matches(input=query)

if "matches" in locals():
    cell1, cell2, cell3, cell4 = st.columns(4)
    cell5, cell6, cell7, cell8 = st.columns(4)
    cell9, cell10, cell11, cell12 = st.columns(4)
    all_cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9, cell10, cell11, cell12]

    for cell, match in zip(all_cells, matches):
        cell.image(match.uri, use_column_width="auto")
        cell.markdown(f"##### {match.tags['productDisplayName']}")
        cell.markdown(f"*{match.tags['masterCategory']}*")
