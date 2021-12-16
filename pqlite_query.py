from jina import Document, Client
from config import SERVER, PORT, TOP_K


def get_matches(input, server=SERVER, port=PORT, limit=TOP_K):
    client = Client(host=server, protocol="http", port=port)
    response = client.search(Document(text=input), return_results=True, parameters={"limit": limit}, show_progress=True)
    matches = response[0].docs[0].matches

    return matches

matches = get_matches("blue shoes")
print(matches)

for match in matches:
    print(match.uri)
