# World Generation Scripts

Automated tools for creating rich, immersive RPG worlds with AI-generated content and images.

## Scripts Overview

### 🎭 `shakespeare_world_builder.py`
Creates a complete Shakespeare-inspired sci-fantasy campaign called "The Stratford Nexus"
- **Characters**: Prospero the Technomancer, Lady M-4C, Puck the Probability Sprite
- **Locations**: Globe Nexus Station, Verona Prime City
- **Items**: Yorick's Memory Skull, Comedy Circuit Crown
- **Images**: Auto-generates portraits and scene art using DALL-E

### 🌟 `expand_shakespeare_world.py`
Adds more content to the Shakespeare world:
- **Characters**: Hamlet-VII AI, Ariel Wind Drone, Weird Sisters Collective
- **Locations**: Arden Digital Forest, Elsinore Data Fortress
- **Items**: Oberon's Crown, Tempest in a Bottle, Poison Earpiece

### 🛠️ `entity_creator.py`
Core utility for creating world entities:
- `create_character()` - Complete character with bio, secrets, stats
- `create_location()` - Locations with descriptions, history, inhabitants
- `create_item()` - Items with stats, lore, and magical properties

### 🎨 `dalle_generator.py`
DALL-E integration for automated image generation:
- Character portraits
- Location environmental art
- Item illustrations
- Batch processing for entire campaigns

## Quick Start

```bash
# Create the complete Shakespeare world
python shakespeare_world_builder.py

# Expand it with more content
python expand_shakespeare_world.py

# Check your new world
ls ../world/campaigns/shakespeare_scifi/
```

## The Stratford Nexus World

A whimsical but dangerous sci-fantasy setting where fallen technology has become magic:

### Core Concept
- **Seven Spheres**: Interconnected realm-worlds based on Shakespeare plays
- **Fallen Empire**: Advanced Elizabethan space civilization left magical-tech ruins
- **Narrative Technology**: Devices that manipulate story, fate, and reality itself

### Key Locations
- **Globe Nexus Station**: Dimensional hub built around the original Globe Theatre
- **Verona Prime**: City of star-crossed lovers and feuding tech-houses
- **Danish Reach**: Haunted by quantum ghosts and AI princes
- **Arden Digital Forest**: Where reality shifts and exile-nobles gather
- **Tempest Islands**: Prospero's domain of weather control and illusion

### Notable Characters
- **Prospero**: Technomancer master of weather control and dimensional magic
- **Lady M-4C**: Ambitious android corrupted by power-hungry algorithms
- **Puck**: Probability-manipulating sprite born from quantum entertainment systems
- **Hamlet-VII**: Brooding AI prince investigating his father's digital murder
- **Weird Sisters**: Quantum fortune-tellers who glimpse multiple timelines

### Magical Technology
- **Soliloquy Stones**: Crystals that reveal inner thoughts
- **Comedy Circuits**: Reality-bending tech that favors happy endings
- **Memory Theaters**: Holographic stages that replay history
- **Narrative Engines**: Devices that can rewrite the fundamental stories of reality

## Configuration

### Required Setup
1. OpenAI API key in `.env` file for DALL-E image generation
2. Python environment with openai library

### File Structure Created
```
world/campaigns/shakespeare_scifi/
├── characters/          # NPCs and important figures
├── locations/           # Places and realms
├── items/              # Magical-tech artifacts
└── WORLD_CONCEPT.md    # Complete world overview
```

## Customization

### Creating Your Own World Builder
1. Copy `shakespeare_world_builder.py` as a template
2. Modify the `create_world_concept()` method with your theme
3. Update character, location, and item creation methods
4. Adjust DALL-E prompts in `dalle_generator.py` for your art style

### Adding New Entity Types
1. Add new creation methods to `EntityCreator`
2. Update the directory structure in `world/templates/`
3. Add image generation support in `WorldImageGenerator`

## Integration with Game

These scripts create world data compatible with the main Vibe Game:
- JSON master files reference all content
- Markdown files provide rich descriptions for AI dungeon master
- Images enhance visual storytelling
- Structure supports easy AI integration for dynamic storytelling

## Example Usage

```python
from entity_creator import EntityCreator
from dalle_generator import WorldImageGenerator

creator = EntityCreator()
image_gen = WorldImageGenerator()

# Create a new character
creator.create_character(
    character_id="merlin_ai",
    name="Merlin the Code Wizard", 
    campaign="my_campaign",
    bio="A wizard who speaks in programming languages..."
)

# Generate portrait
character_data = {"id": "merlin_ai", "name": "Merlin the Code Wizard"}
image_gen.generate_character_image(character_data, "my_campaign")
```

The scripts demonstrate the power of combining AI creativity with systematic world-building to create rich, interconnected fantasy universes ready for adventuring!