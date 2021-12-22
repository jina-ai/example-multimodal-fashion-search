from jina import Document, Client
from pprint import pprint
from config import SERVER, PORT, TOP_K

search_term = "blue sports shoes"

filter = {
    "$and": {
        "year": {"$gte": 2011, "$lte": 2014},
        "price": {"$gte": 100, "$lte": 200},
        "rating": {"$gte": 3},
        "baseColour": {"$one_of": ['White', 'Blue', 'Black']},
        "season": {"$all_of": ['Summer', 'Spring', 'Fall']},
    },
}


def get_matches(input, server=SERVER, port=PORT, limit=TOP_K):
    client = Client(host=server, protocol="http", port=port)
    response = client.search(
        Document(text=input),
        return_results=True,
        parameters={"limit": limit, "filter": filter},
        show_progress=True,
    )
    matches = response[0].docs[0].matches

    return matches


matches = get_matches(search_term)

for match in reversed(matches):
    tags = match.tags.to_dict()
    pprint(tags)
    print("---")
