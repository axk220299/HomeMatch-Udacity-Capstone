import chromadb
from chromadb.config import Settings

def get_db():
    client = chromadb.Client(Settings(allow_reset=True))
    collection = client.get_or_create_collection("real_estate_listings")
    return collection