from openai import OpenAI
import json
import os
from config import OPENAI_API_KEY, OPENAI_API_BASE

client = OpenAI(
    base_url=OPENAI_API_BASE,
    api_key=OPENAI_API_KEY
)

def get_image_path(index):
    """Helper function to find the correct image path"""
    base_path = os.path.join('images', f'house{index}')
    
    # Check different possible extensions
    possible_paths = [
        f"{base_path}.png",
        f"{base_path}.png.png",
        f"{base_path}.PNG",
        f"{base_path}.PNG.png"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found image: {path}")
            return path
            
    print(f"Warning: No image found for house {index}")
    return os.path.join('images', f'house{index}.png')  # Return default path

def generate_listings(num_listings=10):
    prompt = """Generate a detailed real estate listing with the following information in JSON format:
    {
        "address": "street address",
        "price": "price in USD",
        "square_footage": "number",
        "bedrooms": "number",
        "bathrooms": "number",
        "description": "detailed description",
        "features": ["feature1", "feature2", ...],
        "neighborhood_info": "detailed neighborhood info"
    }
    Make it realistic and diverse."""
    
    listings = []
    print("\nChecking image files...")
    for i in range(num_listings):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        listing = json.loads(response.choices[0].message.content)
        
        # Get the correct image path
        listing['image_url'] = get_image_path(i + 1)
        
        listings.append(listing)
    
    return listings