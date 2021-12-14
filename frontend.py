import streamlit as st
from helper import get_matches
from jina import Client, Document
from jina.types.request import Response
from config import PORT, SERVER


st.title("Multimodal fashion search")

query = st.text_input(label="Search term", placeholder="Blue dress")

search_button = st.button("Search")

if search_button:
    matches = get_matches(input=query)

if "matches" in locals():
    for match in matches:
        print(match.tags["filename"])
        st.image(match.tags["filename"])
    # st.json(matches)
