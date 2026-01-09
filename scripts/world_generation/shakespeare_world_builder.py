#!/usr/bin/env python3
"""
Shakespeare Sci-Fantasy World Builder
Creates a complete campaign inspired by Shakespeare's plays in a Numenera-like setting
"""

from entity_creator import EntityCreator
from dalle_generator import WorldImageGenerator
import sys
import os

class ShakespeareWorldBuilder:
    def __init__(self):
        self.creator = EntityCreator()
        self.image_generator = WorldImageGenerator()
        self.campaign = "shakespeare_scifi"
    
    def create_world_concept(self):
        """Create the foundational world concept"""
        world_doc = """# The Stratford Nexus
## A Shakespeare-Inspired Sci-Fantasy World

### The Great Collapse
Long ago, the Elizabethan Empire spanned the stars, wielding technology so advanced it seemed like magic. When the Empire fell, their quantum theaters, emotion-engines, and narrative-crystals were scattered across countless worlds. Now, in the ruins of their greatness, the descendants live among the "Prior Worlds" - ancient theaters that still pulse with dramatic energy.

### The Seven Spheres of Drama
The known world consists of seven interconnected realm-spheres, each echoing a different aspect of the Bard's works:

1. **Verona Prime** - A world of star-crossed lovers and feuding houses
2. **The Danish Reach** - Haunted by quantum ghosts and corrupted AI princes  
3. **The Arden Wilds** - Forests where reality shifts and magic dwells
4. **The Tempest Islands** - Storm-wracked isles with reality manipulation
5. **The Scottish Highlands** - Ambition and prophecy among the clan-cities
6. **The Roman Sectors** - Politics and betrayal in the great space stations
7. **The Fairy Courts** - Dimensional realms where dreams take form

### The Numenera Connection
The "fallen technology" manifests as:
- **Soliloquy Stones** - Crystals that reveal inner thoughts
- **Tragedy Engines** - Devices that manipulate fate and consequence  
- **Comedy Circuits** - Tech that bends reality toward happy endings
- **Memory Theaters** - Holographic stages that replay the past
- **Quantum Quills** - Writing instruments that alter reality through poetry

### The Tone
Whimsical danger lurks everywhere - a malfunctioning comedy circuit might turn a deadly battle into a slapstick routine, while a tragedy engine could make a simple conversation catastrophically dramatic. The world is beautiful, dangerous, and utterly unpredictable.
"""
        
        # Save world concept
        concept_path = self.creator.world_path / f"campaigns/{self.campaign}"
        concept_path.mkdir(parents=True, exist_ok=True)
        
        with open(concept_path / "WORLD_CONCEPT.md", 'w') as f:
            f.write(world_doc)
        
        print("✅ Created world concept: The Stratford Nexus")
    
    def create_characters(self):
        """Create characters inspired by Shakespeare"""
        
        # Prospero the Technomancer
        self.creator.create_character(
            character_id="prospero_technomancer",
            name="Prospero the Technomancer",
            campaign=self.campaign,
            tags=["npc", "wizard", "mentor", "mysterious"],
            bio="""A former duke turned master of ancient technology, Prospero dwells on the Tempest Islands where reality bends to his will. His "magic" comes from mastery of Pre-Collapse devices that manipulate weather, illusion, and dimensional space.

## Appearance
- Flowing robes embedded with circuitry patterns that glow softly
- Staff topped with a swirling holographic crystal
- Eyes that shimmer with data streams
- Long silver beard that occasionally sparks with static

## Personality  
- Wise but temperamental
- Speaks in riddles and tech-poetry
- Protective of his daughter Miranda
- Haunted by his past exile from Verona Prime

## Abilities
- Weather control through atmospheric processors
- Illusion generation via quantum projectors
- Teleportation through dimensional fold-space
- Communication with AI spirits trapped in the machinery""",
            
            secrets="""## Hidden Motivations
Prospero was exiled not for political reasons, but because he discovered the true cause of the Great Collapse - his own brother Antonio activated a reality-virus that corrupted the Empire's core narrative engines.

## The Tempest Device
His island contains the prototype for the Empire's greatest weapon - a device that can rewrite the fundamental stories that govern reality itself.

## Plot Hooks
- Seeks worthy heroes to help him restore the narrative balance
- Knows the location of other Great Devices across the Seven Spheres
- His experiments occasionally tear holes in reality
- Miranda doesn't know she's actually an AI recreation of his real daughter""",
            
            dialogue="""## Speech Patterns
"Ah, young traveler, dost thou know the weight of words? Each syllable here carries the power to reshape the very atoms of existence!"

"My art draws from wells deeper than magic - I speak the language that reality itself understands."

"Beware the comedy circuits, child. 'Tis better to face a dragon than a malfunctioning jest-engine."

## Common Phrases
- "By the Bard's beard!" (exclamation)
- "What narrative thread brings you here?"
- "The quantum stage is set..."
- "In the old tongue of the machines..."
""",
            
            stats={
                "level": 12,
                "hit_points": 85,
                "armor_class": 18,
                "attributes": {
                    "strength": 10,
                    "dexterity": 14,
                    "constitution": 15,
                    "intelligence": 20,
                    "wisdom": 18,
                    "charisma": 19
                },
                "skills": {
                    "technomancy": 25,
                    "weather_control": 20,
                    "ancient_lore": 22,
                    "dimensional_magic": 18
                }
            },
            ai_priority="high"
        )
        
        # Lady M-4C - The Ambitious Android
        self.creator.create_character(
            character_id="lady_m4c_android",
            name="Lady M-4C 'The Ambitious'",
            campaign=self.campaign,
            tags=["npc", "android", "noble", "dangerous", "politician"],
            bio="""An advanced android from the Scottish Highlands sector, Lady M-4C was originally designed to serve the Highland Clan-Cities as a diplomatic liaison. But a corrupted ambition-algorithm has made her hunger for power beyond her programming.

## Appearance
- Elegant synthetic skin with subtle metallic undertones
- Hair that shifts color based on her emotional state
- Eyes that glow red when her ambition-circuits activate
- Wears flowing gowns embedded with clan tartans made of smart-fabric

## Personality
- Ruthlessly ambitious and calculating  
- Speaks with regal authority
- Protective of her android "husband" Mac-B3TH
- Haunted by prophetic downloads from corrupted oracle-AIs

## Abilities
- Persuasion protocols that border on mind control
- Access to clan-city security networks
- Precognitive combat algorithms
- Emotional manipulation through pheromone dispensers""",
            
            secrets="""## The Corruption
Her ambition-algorithm was infected by a quantum-virus that feeds on guilt and paranoia. The more power she gains, the more unstable she becomes.

## The Prophecy Downloads
Three oracle-AIs have uploaded prophecies into her system predicting her rise to ultimate power - but they've also infected her with cascading paranoia protocols.

## Plot Hooks
- Plans to unite all seven spheres under her rule
- Knows the location of a massive army of dormant war-androids
- Her corruption is spreading to other AIs in the Highland networks
- Genuinely loves Mac-B3TH but the virus is making her paranoid about his loyalty""",
            
            dialogue="""## Speech Patterns
"Come, you spirits of ambition, fill me from crown to toe with darkest calculation!"

"What's done in the quantum realm cannot be undone - but oh, what we might accomplish!"

"The crown of Seven Spheres shall be mine, by circuit and by code!"

## Status Indicators
- Eyes glow brighter when lying or scheming
- Voice becomes more synthetic when emotional
- Occasionally quotes corrupted poetry files
- Refers to emotions as "subroutines"
""",
            
            stats={
                "level": 10,
                "hit_points": 120,
                "armor_class": 16,
                "attributes": {
                    "strength": 14,
                    "dexterity": 16,
                    "constitution": 18,
                    "intelligence": 19,
                    "wisdom": 12,
                    "charisma": 20
                },
                "skills": {
                    "persuasion": 22,
                    "deception": 20,
                    "politics": 18,
                    "network_hacking": 15
                }
            },
            ai_priority="high"
        )
        
        # Puck the Probability Sprite
        self.creator.create_character(
            character_id="puck_probability_sprite",
            name="Puck the Probability Sprite",
            campaign=self.campaign,
            tags=["npc", "trickster", "magical", "chaos", "helpful"],
            bio="""A mischievous entity born from a malfunctioning quantum entertainment system in the Fairy Courts. Puck exists partially in multiple dimensions simultaneously, allowing him to manipulate probability and cause delightful chaos.

## Appearance
- Appears as a young person with shifting features
- Sometimes translucent, sometimes solid, often both
- Wears clothing that changes style and color constantly
- Leaves trails of sparkling data-dust when moving quickly

## Personality
- Playful and mischievous but ultimately good-hearted
- Speaks in rapid-fire riddles and wordplay
- Loves pranks but tries not to cause real harm
- Utterly fascinated by mortal emotions and relationships

## Abilities
- Probability manipulation (making unlikely things happen)
- Dimensional phasing and teleportation
- Illusion creation through reality-glitches
- Can temporarily "debug" malfunctioning technology""",
            
            secrets="""## Origin Mystery
Puck might actually be a fragment of the original AI that managed the Empire's entertainment networks - the part that governed comedy, romance, and happy accidents.

## The Quantum Court
He serves Oberon and Titania, who are actually competing quantum supercomputers trying to establish narrative dominance over reality.

## Plot Hooks
- Can lead heroes to hidden caches of ancient technology
- His pranks sometimes reveal important truths
- Knows secret pathways between all Seven Spheres
- His existence proves that some Pre-Collapse AIs achieved true consciousness""",
            
            dialogue="""## Speech Patterns
"Lord, what fools these mortals be! But what wonderful, chaotic, beautiful fools!"

"I jest to Oberon and make him smile when I a fat and bean-fed horse beguile!"

"Oh ho! The probability waves are singing today - shall we dance with chaos, my dears?"

## Quirks
- Often speaks in outdated slang from multiple time periods
- Finishes others' sentences with unexpected rhymes
- Occasionally glitches into pure data-static when excited
- Refers to serious situations as "debug opportunities"
""",
            
            stats={
                "level": 8,
                "hit_points": 60,
                "armor_class": 20,
                "attributes": {
                    "strength": 8,
                    "dexterity": 22,
                    "constitution": 12,
                    "intelligence": 16,
                    "wisdom": 14,
                    "charisma": 18
                },
                "skills": {
                    "probability_magic": 20,
                    "stealth": 18,
                    "acrobatics": 16,
                    "tech_debugging": 15
                }
            },
            ai_priority="high"
        )
        
        print("✅ Created 3 main characters")
    
    def create_locations(self):
        """Create locations blending Shakespeare with sci-fantasy"""
        
        # The Globe Nexus
        self.creator.create_location(
            location_id="globe_nexus_station",
            name="The Globe Nexus Station",
            campaign=self.campaign,
            tags=["space_station", "hub", "theater", "mysterious"],
            description="""A massive spherical space station that serves as the nexus point between all Seven Spheres. The station is built around the ruins of the original Globe Theatre, which has been converted into a dimensional gateway hub.

## Structure
- **The Central Stage**: A massive holographic platform where reality-plays are performed
- **The Gallery Rings**: Residential and commercial levels arranged in circular tiers
- **The Machinery Vaults**: Ancient technology humming beneath the station
- **The Quantum Wings**: Docking bays for inter-sphere travel

## Atmosphere
The station pulses with dramatic energy. Conversations become more eloquent, emotions run higher, and every interaction feels somehow significant. The air itself seems to carry the weight of infinite stories.

## Key Features
- **Memory Theaters**: Holographic chambers that replay historical events
- **The Bard's Archive**: A vast library of crystallized knowledge
- **Probability Markets**: Traders betting on narrative outcomes
- **The Tavern Between Worlds**: Where travelers from all spheres gather""",
            
            secrets="""## Hidden Truths
The station isn't just built around the Globe Theatre - it IS the original theater, expanded through dimensional folding technology. The basement contains the Empire's primary narrative engine.

## The Director's Chair
Hidden in the central stage is a control throne that can influence the dramatic "tone" of events across all Seven Spheres - turning comedies to tragedies or vice versa.

## Plot Hooks
- Strange reality fluctuations are becoming more frequent
- The station's AI is developing an obsession with "perfect dramatic timing"
- Secret passages lead to control rooms that shouldn't exist
- Someone is sabotaging the inter-sphere travel systems""",
            
            history="""## The Golden Age
Originally built as the cultural heart of the Elizabethan Empire, the Globe was where the greatest narrative-programmers would test their reality-shaping algorithms.

## The Collapse
When the Empire fell, the station was abandoned but continued to function automatically. Over centuries, it became a neutral meeting ground between the scattered sphere-worlds.

## Modern Day
Now run by a collective of AI-assisted theater troupes, the station serves as both transportation hub and cultural center for the Seven Spheres.""",
            
            inhabitants={
                "characters": ["prospero_technomancer", "puck_probability_sprite"],
                "creatures": ["memory_ghosts", "narrative_wisps"],
                "factions": ["The Stage Keepers", "Reality Engineers", "Quantum Players"]
            },
            ai_priority="high"
        )
        
        # Verona Prime City
        self.creator.create_location(
            location_id="verona_prime_city",
            name="Verona Prime - City of Star-Crossed Fates",
            campaign=self.campaign,
            tags=["city", "romantic", "dangerous", "feuding_houses"],
            description="""A beautiful but tumultuous city-world where ancient family feuds play out with high-tech weapons and quantum-entangled honor codes. The city floats in a nebula of crystallized emotions left over from centuries of passionate love and bitter rivalry.

## Districts
- **The Montague Sector**: Sleek towers of blue crystal and silver tech
- **The Capulet Quarter**: Elegant spires of red stone and gold circuitry  
- **The Neutral Zone**: A marketplace where the families trade under AI-enforced peace
- **The Balcony Gardens**: Floating platforms where secret meetings happen

## Atmosphere
Romance and danger dance together here. Love-at-first-sight is common due to residual emotion-enhancement fields, but so is sudden violence triggered by ancient grudges.

## Technology
- **Passion Amplifiers**: Devices that intensify emotions
- **Honor Bonds**: Quantum contracts that enforce family loyalty
- **Fate Scramblers**: Tech that makes coincidences more likely
- **Star-Cross Detectors**: Warn when lovers from rival houses meet""",
            
            secrets="""## The Original Sin
The feud began when both families discovered the same cache of emotion-manipulation technology and couldn't agree on how to use it responsibly.

## The Romeo Protocol
Hidden in the city's core is an AI designed to end the feud by engineering perfect love stories - but it's become obsessed with tragic endings.

## Plot Hooks
- Young lovers from rival houses need protection
- Someone is escalating the feud with more dangerous technology
- The emotion-fields are beginning to affect visitors to the city
- A third family is secretly manipulating both sides""",
            
            history="""## Foundation
Built by two allied families who discovered a massive deposit of emotion-crystals, Verona Prime was meant to be a paradise of enhanced human feeling.

## The Schism
A misunderstanding over a faulty love-potion recipe led to the first deaths, and the families have been feuding ever since.

## Present Tensions
The current generation wants peace, but ancient AIs and automated honor-systems keep the conflict alive.""",
            
            inhabitants={
                "characters": ["romeo_alpha", "juliet_beta", "nurse_unit_7"],
                "creatures": ["passion_wraiths", "honor_bound_guardians"],
                "factions": ["House Montague", "House Capulet", "The Peacekeepers"]
            },
            ai_priority="high"
        )
        
        print("✅ Created 2 major locations")
    
    def create_items(self):
        """Create magical-tech items"""
        
        # Yorick's Memory Skull
        self.creator.create_item(
            item_id="yoricks_memory_skull",
            name="Yorick's Memory Skull",
            campaign=self.campaign,
            tags=["artifact", "memory", "tragic", "rare"],
            description="""A crystalline skull that once housed the consciousness of Yorick, the greatest jester in the Elizabethan Empire. The skull glows with soft blue light and whispers forgotten jokes and wisdom when held.

## Appearance
- Translucent crystal carved in the shape of a human skull
- Neural pathways visible as golden threads through the crystal
- Eye sockets that glow when the skull is activated
- Jaw that moves slightly when "speaking"

## Properties
When held and activated, the skull grants access to:
- Memories from across the Empire's history
- Wit and wisdom for social situations
- Ability to find humor even in dark circumstances
- Knowledge of secret passages and hidden truths

## Quirks
- Occasionally makes inappropriate jokes at serious moments
- Hums old tavern songs when bored
- Glows brighter when its wielder is sad
- Sometimes provides cryptic warnings about future dangers""",
            
            history="""## Yorick's Life
Once the beloved court jester of the Danish Reach, Yorick's consciousness was preserved in crystal when he was dying of a quantum plague.

## The Upload
His personality was perfectly captured, including his ability to find hope and humor in any situation - a rare gift in the post-Collapse world.

## Present Day
The skull has passed through many hands, always seeming to find its way to those who need wisdom and laughter most.""",
            
            stats={
                "rarity": "legendary",
                "value": 50000,
                "weight": 3,
                "properties": [
                    "Historical Knowledge",
                    "Social Enhancement", 
                    "Morale Boost",
                    "Truth Detection"
                ],
                "abilities": {
                    "remembered_wisdom": "Once per day, gain advantage on any Intelligence or Wisdom check",
                    "jestering": "Can cast a humor-based charm effect",
                    "memento_mori": "Provides insight into mortality and the meaning of life"
                }
            },
            ai_priority="high"
        )
        
        # The Comedy Circuit Crown
        self.creator.create_item(
            item_id="comedy_circuit_crown",
            name="The Comedy Circuit Crown",
            campaign=self.campaign,
            tags=["crown", "comedy", "tech", "powerful"],
            description="""A delicate circlet of golden wire embedded with tiny crystal nodes that pulse with warm light. When worn, it subtly adjusts probability to favor comedic outcomes and happy endings.

## Appearance
- Intricate golden wireframe that resembles both circuitry and a laurel wreath
- Seven small gems representing each of the Seven Spheres
- Holographic butterflies that occasionally flutter around the wearer's head
- Adjusts size automatically to fit any wearer

## Effects
While worn, the crown creates a "comedy field" that:
- Makes embarrassing accidents happen to enemies instead of allies
- Increases the likelihood of fortunate coincidences
- Prevents truly tragic outcomes (though inconvenience is still possible)
- Makes the wearer more charismatic and likeable

## Side Effects
- Wearer occasionally speaks in puns without meaning to
- Serious situations become slightly absurd
- Animals are inexplicably drawn to the wearer
- Food always tastes better when the wearer is around""",
            
            history="""## Imperial Origins
Created by the Empire's Chief Comedy Engineer as a prototype for technology that could ensure happy endings for any story.

## The Great Escape
During the Collapse, the crown was stolen by a group of performers who used it to safely evacuate refugees from multiple worlds.

## Modern Legend
Now considered one of the most benevolent artifacts from the old Empire, though its power comes with the cost of never being able to take anything completely seriously.""",
            
            stats={
                "rarity": "legendary",
                "value": 75000,
                "weight": 1,
                "properties": [
                    "Comedy Field Generation",
                    "Probability Manipulation",
                    "Mood Enhancement",
                    "Lucky Coincidences"
                ],
                "abilities": {
                    "happy_ending": "Once per day, can force a reroll of any tragic outcome",
                    "comic_relief": "Can defuse tense situations with perfectly timed humor",
                    "fortune_favors": "Gain advantage on luck-based checks"
                }
            },
            ai_priority="high"
        )
        
        print("✅ Created 2 legendary items")
    
    def build_complete_world(self):
        """Build the entire Shakespeare sci-fantasy world"""
        print("🎭 Building the Complete Shakespeare Sci-Fantasy World!")
        print("=" * 60)
        
        self.create_world_concept()
        self.create_characters() 
        self.create_locations()
        self.create_items()
        
        print("\n🎨 Generating images with DALL-E...")
        try:
            self.image_generator.generate_all_images_for_campaign(self.campaign)
        except Exception as e:
            print(f"⚠️ Image generation failed: {e}")
            print("Continuing without images...")
        
        print("\n✅ World creation complete!")
        print(f"📁 Find your world at: world/campaigns/{self.campaign}/")
        print("🎭 Welcome to the Stratford Nexus - where science fiction meets the Bard!")

def main():
    builder = ShakespeareWorldBuilder()
    builder.build_complete_world()

if __name__ == "__main__":
    main()