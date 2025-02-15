from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_API_BASE

client = OpenAI(
    base_url=OPENAI_API_BASE,
    api_key=OPENAI_API_KEY
)

def personalize_description(listing, preferences):
    prompt = f"""
    Given the following real estate listing and buyer preferences, rewrite the description to highlight aspects that match the preferences. Keep all factual information accurate.
    
    Listing: {listing}
    
    Buyer Preferences: {preferences}
    
    Provide a personalized description that emphasizes relevant features and benefits for this specific buyer.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content