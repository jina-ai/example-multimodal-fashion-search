import streamlit as st
from helper import get_matches, resize_image, print_stars
from config import TOP_K, IMAGE_RESIZE_FACTOR, SERVER, PORT, DEBUG

filters = {"$and": {"year": {}, "price": {}, "rating": {}}}

title = "👕 Multimodal fashion search with Jina"

st.set_page_config(page_title=title, layout="wide")

# Sidebar
st.sidebar.title("Options")

limit = st.sidebar.slider(
    label="Maximum results", min_value=int(TOP_K / 3), max_value=TOP_K * 3, value=TOP_K
)

(filters["$and"]["year"]["$gte"], filters["$and"]["year"]["$lte"]) = st.sidebar.slider(
    "Year", 2007, 2019, (2007, 2019)
)
(
    filters["$and"]["price"]["$gte"],
    filters["$and"]["price"]["$lte"],
) = st.sidebar.slider("Price", 0, 200, (0, 200))
filters["$and"]["rating"]["$gte"] = st.sidebar.slider("Minimum rating", 0, 5, 3)

if DEBUG:
    with st.sidebar.expander("Debug"):
        server = st.text_input(label="Server", value=SERVER)
        port = st.text_input(label="Port", value=PORT)
else:
    server = SERVER
    port = PORT



# season = st.sidebar.selectbox("Season", ["Summer", "Fall", "Winter", "Spring"])
# use_hi_res = st.sidebar.checkbox(label="Show hi-res images") # WIP

st.sidebar.title("About")

st.sidebar.markdown(
    """This example lets you use a *textual* description to search through *images* of fashion items using [Jina](https://github.com/jina-ai/jina/).

#### Why are the images so pixelated?

To speed up indexing, we indexed relatively low-resolution graphics. We're looking at hosting hi-res images elsewhere and showing those instead. But for the purposes of a tech demo it seems like overkill.

"""
)

st.sidebar.markdown(
    "[Repo link](https://github.com/alexcg1/jina-multimodal-fashion-search)"
)

# Main area
st.title(title)
query = st.text_input(label="Search term", placeholder="Blue dress")

search_button = st.button("Search")

if search_button:
    matches = get_matches(input=query, limit=limit, filters=filters, server=server, port=port)

if "matches" in locals():
    for match in matches:
        pic_cell, desc_cell, price_cell = st.columns([1, 6, 1])

        image = resize_image(match.uri, resize_factor=IMAGE_RESIZE_FACTOR)

        # pic_cell.image(match.uri, use_column_width="auto")
        pic_cell.image(image, use_column_width="auto")
        desc_cell.markdown(f"##### {match.tags['productDisplayName']} {print_stars(match.tags['rating'])}")
        desc_cell.markdown(
            f"*{match.tags['masterCategory']}*, *{match.tags['subCategory']}*, *{match.tags['articleType']}*, *{match.tags['baseColour']}*, *{match.tags['season']}*, *{match.tags['usage']}*, *{match.tags['year']}*"
        )
        price_cell.button(key=match.tags["id"], label=str(match.tags["price"]))
