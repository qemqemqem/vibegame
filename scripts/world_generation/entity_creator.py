#!/usr/bin/env python3
"""
Entity Creation Script for World Building
Creates characters, locations, and items with proper file structure
"""

import json
import os
from pathlib import Path
from datetime import datetime

class EntityCreator:
    def __init__(self, world_path=None):
        self.world_path = Path(world_path or Path(__file__).parent.parent.parent / 'world')
        self.templates_path = self.world_path / 'templates'
    
    def create_character(self, character_id, name, campaign, tags=None, bio="", secrets="", dialogue="", **kwargs):
        """Create a complete character entity with all files"""
        tags = tags or ["npc"]
        campaign_path = self.world_path / f"campaigns/{campaign}/characters"
        campaign_path.mkdir(parents=True, exist_ok=True)
        
        # Create master JSON file
        character_data = {
            "id": character_id,
            "type": "character",
            "name": name,
            "campaign": campaign,
            "tags": tags,
            "files": {
                "portrait": f"{character_id}_portrait.png",
                "public_bio": f"{character_id}_bio.md",
                "secrets": f"{character_id}_secrets.md",
                "stats": f"{character_id}_stats.json",
                "dialogue": f"{character_id}_dialogue.md",
                "relationships": f"{character_id}_relationships.json"
            },
            "metadata": {
                "created": datetime.now().isoformat()[:10],
                "last_modified": datetime.now().isoformat()[:10],
                "status": "active",
                "ai_priority": kwargs.get("ai_priority", "medium")
            }
        }
        
        # Save master file
        with open(campaign_path / f"{character_id}.json", 'w') as f:
            json.dump(character_data, f, indent=2)
        
        # Create bio file
        with open(campaign_path / f"{character_id}_bio.md", 'w') as f:
            f.write(f"# {name}\n\n{bio}")
        
        # Create secrets file
        with open(campaign_path / f"{character_id}_secrets.md", 'w') as f:
            f.write(f"# {name}'s Secrets\n\n{secrets}")
        
        # Create dialogue file
        with open(campaign_path / f"{character_id}_dialogue.md", 'w') as f:
            f.write(f"# {name}'s Dialogue\n\n{dialogue}")
        
        # Create basic stats file
        stats = kwargs.get("stats", {
            "level": 5,
            "hit_points": 50,
            "armor_class": 14,
            "attributes": {
                "strength": 12,
                "dexterity": 14,
                "constitution": 13,
                "intelligence": 15,
                "wisdom": 12,
                "charisma": 16
            }
        })
        
        with open(campaign_path / f"{character_id}_stats.json", 'w') as f:
            json.dump(stats, f, indent=2)
        
        # Create relationships file
        relationships = kwargs.get("relationships", {"allies": [], "enemies": [], "neutral": []})
        with open(campaign_path / f"{character_id}_relationships.json", 'w') as f:
            json.dump(relationships, f, indent=2)
        
        print(f"✅ Created character: {name} ({character_id})")
        return character_data
    
    def create_location(self, location_id, name, campaign, tags=None, description="", secrets="", history="", **kwargs):
        """Create a complete location entity with all files"""
        tags = tags or ["location"]
        campaign_path = self.world_path / f"campaigns/{campaign}/locations"
        campaign_path.mkdir(parents=True, exist_ok=True)
        
        # Create master JSON file
        location_data = {
            "id": location_id,
            "type": "location",
            "name": name,
            "campaign": campaign,
            "tags": tags,
            "files": {
                "map": f"{location_id}_map.png",
                "image": f"{location_id}_image.png",
                "description": f"{location_id}_description.md",
                "secrets": f"{location_id}_secrets.md",
                "history": f"{location_id}_history.md",
                "inhabitants": f"{location_id}_inhabitants.json"
            },
            "metadata": {
                "created": datetime.now().isoformat()[:10],
                "last_modified": datetime.now().isoformat()[:10],
                "status": "active",
                "ai_priority": kwargs.get("ai_priority", "medium")
            }
        }
        
        # Save master file
        with open(campaign_path / f"{location_id}.json", 'w') as f:
            json.dump(location_data, f, indent=2)
        
        # Create description file
        with open(campaign_path / f"{location_id}_description.md", 'w') as f:
            f.write(f"# {name}\n\n{description}")
        
        # Create secrets file
        with open(campaign_path / f"{location_id}_secrets.md", 'w') as f:
            f.write(f"# {name} - Hidden Secrets\n\n{secrets}")
        
        # Create history file
        with open(campaign_path / f"{location_id}_history.md", 'w') as f:
            f.write(f"# History of {name}\n\n{history}")
        
        # Create inhabitants file
        inhabitants = kwargs.get("inhabitants", {"characters": [], "creatures": []})
        with open(campaign_path / f"{location_id}_inhabitants.json", 'w') as f:
            json.dump(inhabitants, f, indent=2)
        
        print(f"✅ Created location: {name} ({location_id})")
        return location_data
    
    def create_item(self, item_id, name, campaign, tags=None, description="", history="", **kwargs):
        """Create a complete item entity with all files"""
        tags = tags or ["item"]
        campaign_path = self.world_path / f"campaigns/{campaign}/items"
        campaign_path.mkdir(parents=True, exist_ok=True)
        
        # Create master JSON file
        item_data = {
            "id": item_id,
            "type": "item",
            "name": name,
            "campaign": campaign,
            "tags": tags,
            "files": {
                "image": f"{item_id}_image.png",
                "description": f"{item_id}_description.md",
                "stats": f"{item_id}_stats.json",
                "history": f"{item_id}_history.md"
            },
            "metadata": {
                "created": datetime.now().isoformat()[:10],
                "last_modified": datetime.now().isoformat()[:10],
                "status": "active",
                "ai_priority": kwargs.get("ai_priority", "medium")
            }
        }
        
        # Save master file
        with open(campaign_path / f"{item_id}.json", 'w') as f:
            json.dump(item_data, f, indent=2)
        
        # Create description file
        with open(campaign_path / f"{item_id}_description.md", 'w') as f:
            f.write(f"# {name}\n\n{description}")
        
        # Create history file
        with open(campaign_path / f"{item_id}_history.md", 'w') as f:
            f.write(f"# History of {name}\n\n{history}")
        
        # Create stats file
        stats = kwargs.get("stats", {
            "rarity": "common",
            "value": 100,
            "weight": 1,
            "properties": []
        })
        
        with open(campaign_path / f"{item_id}_stats.json", 'w') as f:
            json.dump(stats, f, indent=2)
        
        print(f"✅ Created item: {name} ({item_id})")
        return item_data

def main():
    creator = EntityCreator()
    print("🛠️ Entity Creator ready! Use the create_character(), create_location(), and create_item() methods.")

if __name__ == "__main__":
    main()