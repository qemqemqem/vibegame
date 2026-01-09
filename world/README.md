# World Data Directory

This directory contains all RPG world data organized using the entity-based architecture described in `docs/WORLD_ARCHITECTURE.md`.

## Quick Start

### Creating a New Character
1. Copy `templates/character_template.json`
2. Update the entity information
3. Create referenced content files
4. Place in appropriate campaign directory

### Directory Structure
```
world/
├── campaigns/default/    # Default campaign entities
├── shared/              # Cross-campaign entities  
├── templates/           # Templates for new entities
└── schema/              # JSON validation schemas
```

### Example Entity
See `campaigns/default/characters/john_blacksmith.json` and associated files for a complete example.

### File Naming
- Master files: `{entity_id}.json`
- Content files: `{entity_id}_{content_type}.{extension}`

## Documentation
For complete architecture details, see `docs/WORLD_ARCHITECTURE.md`