from listing_generator import generate_listings
from vector_search import create_listing_embedding, get_embedding
from personalization import personalize_description
from database import get_db
from image_processor import ImageProcessor
from interactive_search import get_user_preferences
import json
import numpy as np
import os

def combine_embeddings(text_embedding, image_embedding, weight=0.7):
    """Combine text and image embeddings with weighting"""
    text_embedding = np.array(text_embedding)
    image_embedding = np.array(image_embedding)
    
    # Normalize embeddings
    text_embedding = text_embedding / np.linalg.norm(text_embedding)
    image_embedding = image_embedding / np.linalg.norm(image_embedding)
    
    # Combine with weights
    combined = weight * text_embedding + (1 - weight) * image_embedding
    return combined / np.linalg.norm(combined)

def main():
    # Print current working directory for debugging
    print(f"Current working directory: {os.getcwd()}")
    print(f"Images directory exists: {os.path.exists('images')}")
    
    # Initialize image processor
    image_processor = ImageProcessor()
    
    # Generate listings
    print("Generating listings...")
    listings = generate_listings(10)
    
    # Get database connection
    collection = get_db()
    
    # Store listings with combined embeddings
    print("Creating embeddings and storing listings...")
    for i, listing in enumerate(listings):
        try:
            print(f"\nProcessing listing {i+1}...")
            # Create text embedding
            text_embedding = create_listing_embedding(listing)
            
            # Get image embedding
            print(f"Processing image: {listing['image_url']}")
            image_embedding = image_processor.get_image_embedding(listing['image_url'])
            
            # Combine embeddings
            final_embedding = combine_embeddings(text_embedding, image_embedding)
            
            # Convert to list for storage
            final_embedding_list = final_embedding.tolist()
            
            collection.add(
                documents=[json.dumps(listing)],
                embeddings=[final_embedding_list],
                ids=[f"listing_{i}"]
            )
            print(f"Successfully processed listing {i+1}")
            
        except Exception as e:
            print(f"Error processing listing {i+1}: {e}")
            continue
    
    while True:
        try:
            # Get user preferences
            preferences = get_user_preferences()
            
            # Search for matches
            print("\nSearching for matches...")
            preference_embedding = get_embedding(preferences)
            results = collection.query(
                query_embeddings=[preference_embedding],
                n_results=3
            )
            
            # Personalize descriptions for matches
            print("\nPersonalized Listings:")
            for i, (doc, distance) in enumerate(zip(results['documents'][0], results['distances'][0])):
                listing = json.loads(doc)
                personalized_desc = personalize_description(listing, preferences)
                print(f"\nMatch {i+1} (Similarity: {1-distance:.2f}):")
                print(personalized_desc)
                print(f"Image: {listing['image_url']}")
                print("-" * 80)
            
        except Exception as e:
            print(f"Error during search: {e}")
            print(f"Error details: {str(e)}")
        
        # Ask if user wants to search again
        again = input("\nWould you like to search again? (yes/no): ").lower()
        if again != 'yes':
            break

    print("\nThank you for using HomeMatch!")

if __name__ == "__main__":
    main()