from docarray import DocumentArray

docs = DocumentArray.pull("fashion-product-images-clip-all")

for doc in docs[0:10]:
    print(doc.id)
    print(doc.tags)
    print(doc.embedding)

print(f"Pulled {len(docs)} Documents")
