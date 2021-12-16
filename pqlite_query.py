from jina import Document, Client
from pprint import pprint
from config import SERVER, PORT, TOP_K


def get_matches(input, server=SERVER, port=PORT, limit=TOP_K):
    client = Client(host=server, protocol="http", port=port)
    response = client.search(
        Document(text=input),
        return_results=True,
        parameters={"limit": limit, "filter": {"year": {"$eq": 2012}}},
        show_progress=True,
    )
    matches = response[0].docs[0].matches

    return response
    # return matches


matches = get_matches("blue shoes")
matches = matches[0].docs[0].matches
print(matches)

for match in matches:
    # print(match)
    # print(match.id)
    print(match.uri)
    tags = match.tags.to_dict()
    pprint(tags)
    print("---")
