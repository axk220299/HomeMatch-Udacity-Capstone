from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_API_BASE

client = OpenAI(
    base_url=OPENAI_API_BASE,
    api_key=OPENAI_API_KEY
)

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

def create_listing_embedding(listing):
    text_to_embed = f"{listing['description']} {listing['neighborhood_info']} {' '.join(listing['features'])}"
    return get_embedding(text_to_embed)