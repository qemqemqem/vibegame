#!/usr/bin/env python3
"""
DALL-E Image Generation Script for World Building
Generates images for characters, locations, and items using OpenAI's DALL-E API
"""

import os
import json
import requests
from pathlib import Path
from openai import OpenAI
import time

class WorldImageGenerator:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.world_path = Path(__file__).parent.parent.parent / 'world'
        
    def generate_image(self, prompt, filename, size="1024x1024", quality="standard"):
        """Generate an image using DALL-E and save it"""
        try:
            print(f"🎨 Generating image: {filename}")
            print(f"📝 Prompt: {prompt}")
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Download and save the image
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(img_response.content)
                print(f"✅ Saved: {filename}")
                return True
            else:
                print(f"❌ Failed to download image for {filename}")
                return False
                
        except Exception as e:
            print(f"❌ Error generating image for {filename}: {e}")
            return False
    
    def generate_character_image(self, character_data, campaign="default"):
        """Generate image for a character entity"""
        character_id = character_data['id']
        name = character_data['name']
        
        # Create character-specific prompt
        prompt = f"Fantasy sci-fi character portrait of {name}, whimsical Shakespearean style, fallen technology magic, detailed face, colorful clothing with tech elements, fantasy RPG art style"
        
        filename = self.world_path / f"campaigns/{campaign}/characters/{character_id}_portrait.png"
        filename.parent.mkdir(parents=True, exist_ok=True)
        
        return self.generate_image(prompt, filename)
    
    def generate_location_image(self, location_data, campaign="default"):
        """Generate image for a location entity"""
        location_id = location_data['id']
        name = location_data['name']
        
        prompt = f"Fantasy sci-fi location of {name}, Shakespearean architecture with futuristic technology, magical energy, whimsical but mysterious atmosphere, detailed environment art"
        
        filename = self.world_path / f"campaigns/{campaign}/locations/{location_id}_image.png"
        filename.parent.mkdir(parents=True, exist_ok=True)
        
        return self.generate_image(prompt, filename)
    
    def generate_item_image(self, item_data, campaign="default"):
        """Generate image for an item entity"""
        item_id = item_data['id']
        name = item_data['name']
        
        prompt = f"Fantasy sci-fi item: {name}, magical technology artifact, Shakespearean elegance with futuristic elements, detailed object art, glowing effects"
        
        filename = self.world_path / f"campaigns/{campaign}/items/{item_id}_image.png"
        filename.parent.mkdir(parents=True, exist_ok=True)
        
        return self.generate_image(prompt, filename)
    
    def generate_all_images_for_campaign(self, campaign="default"):
        """Generate images for all entities in a campaign"""
        campaign_path = self.world_path / f"campaigns/{campaign}"
        
        # Generate character images
        characters_path = campaign_path / "characters"
        if characters_path.exists():
            for json_file in characters_path.glob("*.json"):
                if not json_file.name.endswith("_stats.json") and not json_file.name.endswith("_relationships.json"):
                    try:
                        with open(json_file, 'r') as f:
                            character_data = json.load(f)
                        self.generate_character_image(character_data, campaign)
                        time.sleep(1)  # Rate limiting
                    except Exception as e:
                        print(f"❌ Error processing {json_file}: {e}")
        
        # Generate location images
        locations_path = campaign_path / "locations"
        if locations_path.exists():
            for json_file in locations_path.glob("*.json"):
                if not json_file.name.endswith("_inhabitants.json"):
                    try:
                        with open(json_file, 'r') as f:
                            location_data = json.load(f)
                        self.generate_location_image(location_data, campaign)
                        time.sleep(1)  # Rate limiting
                    except Exception as e:
                        print(f"❌ Error processing {json_file}: {e}")
        
        # Generate item images
        items_path = campaign_path / "items"
        if items_path.exists():
            for json_file in items_path.glob("*.json"):
                if not json_file.name.endswith("_stats.json"):
                    try:
                        with open(json_file, 'r') as f:
                            item_data = json.load(f)
                        self.generate_item_image(item_data, campaign)
                        time.sleep(1)  # Rate limiting
                    except Exception as e:
                        print(f"❌ Error processing {json_file}: {e}")

def main():
    generator = WorldImageGenerator()
    
    # Check if API key is available
    if not generator.client.api_key:
        print("❌ OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        return
    
    print("🚀 Starting image generation for Shakespeare sci-fantasy world...")
    generator.generate_all_images_for_campaign("shakespeare_scifi")
    print("✅ Image generation complete!")

if __name__ == "__main__":
    main()