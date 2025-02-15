import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import os
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def get_image_embedding(self, image_path):
        try:
            # Normalize path separators for Windows
            image_path = image_path.replace('/', os.path.sep)
            abs_path = os.path.abspath(image_path)
            
            print(f"Looking for image at: {abs_path}")
            
            if not os.path.exists(abs_path):
                print(f"Warning: Image not found at {abs_path}")
                # Return zeros array of the same dimension as text embeddings (1536)
                return np.zeros(1536)
            
            print(f"Found image at: {abs_path}")
            
            # Open and process the image
            image = Image.open(abs_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            image_features = self.model.get_image_features(**inputs)
            
            # Resize the image features to match text embedding size (1536)
            image_features_np = image_features.detach().cpu().numpy()[0]
            resized_features = np.zeros(1536)
            # Pad or repeat the features to match the size
            resized_features[:len(image_features_np)] = image_features_np
            
            print(f"Successfully processed image: {image_path}")
            return resized_features
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            print(f"Current working directory: {os.getcwd()}")
            return np.zeros(1536)  # Return zeros array of correct size