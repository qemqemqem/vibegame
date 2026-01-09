# World Data Architecture

## Overview

The `world/` directory contains all RPG world data organized as a flexible, AI-friendly system. Each entity (character, location, item, etc.) consists of a master JSON file that references associated content files.

## Design Principles

**🎯 Entity-Driven**: Everything is an entity with consistent structure  
**🔗 Reference-Based**: JSON master files link to content, not embed it  
**📁 Campaign Isolation**: Support multiple worlds/campaigns  
**🤖 AI-Friendly**: Structure optimized for AI dungeon master integration  
**📈 Scalable**: Easy to add new entity types and content  

## Directory Structure

```
world/
├── campaigns/                    # Campaign-specific data
│   ├── default/                 # Default campaign world
│   │   ├── characters/          # NPCs and important characters
│   │   ├── locations/           # Places, dungeons, regions
│   │   ├── items/               # Weapons, artifacts, equipment
│   │   ├── creatures/           # Monsters, animals, beings
│   │   ├── quests/              # Storylines, missions, plots
│   │   ├── organizations/       # Guilds, factions, governments
│   │   └── events/              # Historical events, timeline
│   └── custom_campaign/         # Additional campaigns
├── shared/                      # Cross-campaign entities
│   ├── items/                   # Generic items (sword, potion)
│   └── creatures/               # Standard monsters (orc, dragon)
├── templates/                   # Templates for new entities
│   ├── character_template.json
│   ├── location_template.json
│   └── item_template.json
└── schema/                      # JSON schemas for validation
    ├── character.schema.json
    ├── location.schema.json
    └── base_entity.schema.json
```

## Entity Structure

### Master JSON File
Every entity has a master JSON file containing metadata and file references:

```json
{
  "id": "john_blacksmith",
  "type": "character",
  "name": "John the Blacksmith",
  "campaign": "default",
  "tags": ["npc", "craftsman", "friendly"],
  "files": {
    "portrait": "john_portrait.png",
    "public_bio": "john_bio.md",
    "secrets": "john_secrets.md",
    "stats": "john_stats.json",
    "dialogue": "john_dialogue.md",
    "relationships": "john_relationships.json"
  },
  "metadata": {
    "created": "2024-01-15",
    "last_modified": "2024-01-20",
    "status": "active",
    "ai_priority": "high"
  }
}
```

### Associated Files
- **Markdown Files**: Text content (descriptions, lore, secrets)
- **JSON Files**: Structured data (stats, relationships, mechanics)
- **Image Files**: Visual content (portraits, maps, illustrations)

## Entity Types

### Characters
NPCs, important figures, party members
```
characters/
├── john_blacksmith.json         # Master file
├── john_portrait.png            # Character portrait
├── john_bio.md                  # Public biography
├── john_secrets.md              # DM secrets and plot hooks
├── john_stats.json              # Combat stats and abilities
├── john_dialogue.md             # Speech patterns and quotes
└── john_relationships.json      # Connections to other entities
```

### Locations
Places, regions, dungeons, buildings
```
locations/
├── moonhaven_village.json       # Master file
├── moonhaven_map.png            # Village map
├── moonhaven_description.md     # Public description
├── moonhaven_secrets.md         # Hidden locations and plots
├── moonhaven_history.md         # Historical background
└── moonhaven_inhabitants.json   # References to character entities
```

### Items
Equipment, artifacts, consumables
```
items/
├── flame_sword.json             # Master file
├── flame_sword_image.png        # Item illustration
├── flame_sword_description.md   # Lore and appearance
├── flame_sword_stats.json       # Game mechanics
└── flame_sword_history.md       # Origin story
```

### Creatures
Monsters, animals, magical beings
```
creatures/
├── ancient_dragon.json          # Master file
├── ancient_dragon_image.png     # Creature illustration
├── ancient_dragon_description.md # Appearance and behavior
├── ancient_dragon_stats.json    # Combat statistics
├── ancient_dragon_lore.md       # Background and motivations
└── ancient_dragon_lair.json     # Reference to location entity
```

### Quests
Storylines, missions, plot threads
```
quests/
├── save_the_village.json        # Master file
├── save_the_village_overview.md # Quest description
├── save_the_village_stages.json # Quest progression
└── save_the_village_rewards.json # Completion rewards
```

## File Naming Conventions

**Entity IDs**: `snake_case` identifiers  
**Master Files**: `{entity_id}.json`  
**Content Files**: `{entity_id}_{content_type}.{extension}`  
**Images**: `{entity_id}_{image_type}.{png|jpg|webp}`  

## AI Integration

### Context Loading
The AI can load entity context by:
1. Reading the master JSON file
2. Loading referenced content files as needed
3. Following entity relationships

### Dynamic References
Entities reference each other through IDs:
```json
{
  "relationships": {
    "allies": ["village_guard_captain", "mayor_aldric"],
    "enemies": ["bandit_leader"],
    "location": "moonhaven_village"
  }
}
```

### AI Prompt Integration
The DM system can inject entity data into prompts:
- Load character secrets when they're encountered
- Reference location descriptions for scene setting
- Access item stats for gameplay mechanics

## Content Guidelines

### Markdown Files
- **Public Content**: Information available to players
- **Secrets**: DM-only information, plot hooks, hidden motivations
- **Rich Descriptions**: Sensory details for immersive storytelling

### JSON Files
- **Stats**: Game mechanics (HP, AC, damage, etc.)
- **Relationships**: Connections between entities
- **Metadata**: System information for AI processing

### Images
- **Portraits**: Character faces and expressions
- **Maps**: Location layouts and geography
- **Illustrations**: Items, creatures, scenes
- **Format**: PNG preferred, optimized for web display

## Development Workflow

### Creating New Entities
1. Copy appropriate template from `templates/`
2. Update entity metadata and file references
3. Create referenced content files
4. Validate against JSON schema
5. Test AI integration

### Content Updates
1. Modify content files directly
2. Update `last_modified` in master JSON
3. Test affected game scenarios

### Campaign Management
1. Create new campaign directory
2. Copy or reference shared entities
3. Customize for campaign-specific needs

## Future Enhancements

### Planned Features
- **Version Control**: Track entity changes over time
- **Validation Tools**: Automated schema checking
- **Import/Export**: Campaign sharing and backup
- **Search System**: Full-text search across world data
- **AI Generation**: Auto-generate entities from prompts

### Technical Improvements
- **Lazy Loading**: Load entity data on-demand
- **Caching**: Performance optimization for frequently accessed entities
- **Compression**: Optimize file sizes for web delivery
- **Backup System**: Automated world data preservation

## Best Practices

**🧪 Test First**: Create entities with game scenarios in mind  
**📝 Document Everything**: Rich descriptions enable better AI responses  
**🔗 Link Entities**: Build interconnected world through relationships  
**🎭 Maintain Consistency**: Follow established naming and structure patterns  
**🔄 Iterate Often**: Refine entities based on gameplay experience  

This architecture supports the game's roadmap for character creation, inventory systems, multiple campaigns, and complex world-building while maintaining the clean, testable patterns established in the codebase.