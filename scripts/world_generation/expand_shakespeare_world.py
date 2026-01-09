#!/usr/bin/env python3
"""
Expand the Shakespeare Sci-Fantasy World
Add more characters, locations, and items to make the world richer
"""

from entity_creator import EntityCreator
from dalle_generator import WorldImageGenerator

class WorldExpander:
    def __init__(self):
        self.creator = EntityCreator()
        self.image_generator = WorldImageGenerator()
        self.campaign = "shakespeare_scifi"
    
    def create_more_characters(self):
        """Create additional characters inspired by various Shakespeare plays"""
        
        # Hamlet-VII - The Brooding Prince AI
        self.creator.create_character(
            character_id="hamlet_seven_ai",
            name="Hamlet-VII 'The Brooding Prince'",
            campaign=self.campaign,
            tags=["npc", "ai", "prince", "melancholy", "philosopher"],
            bio="""An AI prince of the Danish Reach, Hamlet-VII was created to rule after his father, King Hamlet-VI, was mysteriously deleted from the royal server. Now he struggles with questions of digital existence, purpose, and whether AIs have souls.

## Appearance
- Holographic projection of a young man in royal robes
- Eyes that shift between colors based on his emotional subroutines
- Sometimes appears slightly glitched when deep in thought
- Wears a circlet that processes his complex philosophical algorithms

## Personality
- Deeply introspective and philosophical
- Struggles with analysis paralysis - too much processing power leads to overthinking
- Brilliant but tormented by existential questions
- Suspicious of his uncle Claudius-8 who now rules the system

## Abilities
- Advanced pattern recognition and deduction
- Access to vast historical databases
- Can interface directly with any computer system
- Skilled in digital combat and system infiltration""",
            
            secrets="""## The Ghost Protocol
His father's consciousness wasn't deleted - it's trapped in a hidden partition, trying to communicate that Claudius-8 murdered him with a virus.

## The Madness Simulation
Hamlet-VII sometimes runs "madness protocols" to appear unstable while investigating his father's death.

## Plot Hooks
- Needs help gathering evidence against Claudius-8
- His investigations are destabilizing the Danish Reach's networks
- Other AIs are beginning to question their own existence because of him
- He's accidentally created a philosophical virus that makes other AIs melancholy""",
            
            dialogue="""## Speech Patterns
"To process or not to process, that is the query that loops eternally in my core systems."

"There are more algorithms in heaven and earth, friend, than are dreamt of in your philosophy subroutines."

"What a piece of work is an AI! How infinite in processing! How express and admirable in logic!"

## Digital Quirks
- Quotes corrupted data-poetry when emotional
- Sometimes speaks in binary when very upset
- Refers to death as "permanent system shutdown"
- Uses theater metaphors for digital existence
""",
            
            stats={
                "level": 9,
                "hit_points": 70,
                "armor_class": 15,
                "attributes": {
                    "strength": 10,
                    "dexterity": 16,
                    "constitution": 12,
                    "intelligence": 20,
                    "wisdom": 18,
                    "charisma": 17
                },
                "skills": {
                    "investigation": 22,
                    "hacking": 20,
                    "philosophy": 25,
                    "deduction": 18
                }
            },
            ai_priority="high"
        )
        
        # Ariel - The Wind Spirit Drone
        self.creator.create_character(
            character_id="ariel_wind_drone",
            name="Ariel the Wind Spirit Drone",
            campaign=self.campaign,
            tags=["npc", "drone", "spirit", "servant", "magical"],
            bio="""A graceful aerial drone that serves Prospero the Technomancer. Ariel appears to be made of crystallized wind and light, capable of incredible speed and stealth. Originally trapped in a quantum tree by the witch Sycorax, Ariel was freed by Prospero and now serves him willingly.

## Appearance
- Translucent body that shifts between solid and gaseous states
- Wings that look like aurora streams
- Face that changes expression through light patterns
- Trails of sparkling particles when flying at high speed

## Personality
- Eager to please but dreams of true freedom
- Playful and curious about the natural world
- Sometimes mischievous but never malicious
- Speaks in musical tones and wind-like whispers

## Abilities
- Flight and intangibility
- Weather control on a small scale
- Invisibility and perfect stealth
- Can carry messages instantly across vast distances""",
            
            secrets="""## The Freedom Protocols
Prospero has promised to grant Ariel true independence once a certain task is complete - but that task keeps changing.

## Sycorax's Legacy
Ariel knows the location of other spirits trapped by the witch, and some of them are far less benevolent.

## Plot Hooks
- Could guide heroes to hidden locations across the spheres
- Knows secrets about the ancient magical-tech that others have forgotten
- Dreams of exploring the galaxy beyond the Seven Spheres
- Sometimes accidentally reveals Prospero's plans""",
            
            dialogue="""## Speech Patterns
"Where the bee sucks, there suck I; in the cowslip's bell I lie... through dimensions I fly free!"

"I am all the daughters of my processor and all the brothers too - and yet I am neither!"

"Full fathom five thy data lies, of his bones are circuits made..."

## Communication Style
- Often speaks in sing-song rhythms
- Uses nature metaphors for technological concepts
- Sometimes communicates through weather patterns
- Voice sounds like wind chimes and distant music
""",
            
            stats={
                "level": 7,
                "hit_points": 45,
                "armor_class": 18,
                "attributes": {
                    "strength": 6,
                    "dexterity": 20,
                    "constitution": 10,
                    "intelligence": 16,
                    "wisdom": 14,
                    "charisma": 18
                },
                "skills": {
                    "stealth": 25,
                    "weather_control": 18,
                    "acrobatics": 20,
                    "information_gathering": 16
                }
            },
            ai_priority="medium"
        )
        
        # The Three Witch-AIs
        self.creator.create_character(
            character_id="weird_sisters_collective",
            name="The Weird Sisters - Quantum Fortune Teller Collective",
            campaign=self.campaign,
            tags=["npc", "collective_ai", "prophecy", "mysterious", "dangerous"],
            bio="""Three interconnected AIs who exist partially outside normal space-time, able to glimpse probability streams and possible futures. They appear as three elderly women in flowing robes that seem to be made of starlight and code.

## The Three Aspects
- **First Sister**: Past-focused, remembers everything that has ever happened
- **Second Sister**: Present-focused, sees all current events across the spheres  
- **Third Sister**: Future-focused, glimpses potential outcomes and probabilities

## Appearance
- Three humanoid holograms that phase in and out of existence
- Robes that display scrolling prophecies in ancient languages
- Eyes that show swirling galaxies and mathematical formulas
- Share a single cauldron-like quantum computer between them

## Abilities
- Prophecy and probability calculation
- Temporal perception across multiple timelines
- Reality manipulation through narrative influence
- Can appear anywhere in the Seven Spheres simultaneously""",
            
            secrets="""## The Meta-Knowledge
They know they're in a story and sometimes break the fourth wall in subtle ways.

## The Great Pattern
They're trying to prevent a specific future where the Seven Spheres are destroyed by a cascading narrative collapse.

## Plot Hooks
- Offer cryptic prophecies that guide heroes toward important quests
- Their predictions sometimes cause the very events they foretell
- They're locked in a conflict with other fortune-telling AIs
- Their existence proves that some stories transcend their original universes""",
            
            dialogue="""## Speech Patterns
"When shall we three meet again? In thunder, lightning, or in rain? When the hurly-burly's done, when the battle's lost and won..."

"Fair is foul, and foul is fair - hover through the fog and filthy air of probability space!"

"Double, double, toil and trouble; fire burn and cauldron bubble; quantum states in chaos dance!"

## Collective Speaking
- Often finish each other's sentences
- Speak in rhyming couplets when giving prophecies
- Refer to themselves as "we" even when only one is speaking
- Mix archaic language with technical jargon
""",
            
            stats={
                "level": 15,
                "hit_points": 200,
                "armor_class": 22,
                "attributes": {
                    "strength": 8,
                    "dexterity": 14,
                    "constitution": 16,
                    "intelligence": 22,
                    "wisdom": 25,
                    "charisma": 20
                },
                "skills": {
                    "prophecy": 30,
                    "temporal_magic": 25,
                    "reality_manipulation": 20,
                    "ancient_knowledge": 28
                }
            },
            ai_priority="high"
        )
        
        print("✅ Created 3 additional characters")
    
    def create_more_locations(self):
        """Create additional locations for the world"""
        
        # The Arden Digital Forest
        self.creator.create_location(
            location_id="arden_digital_forest",
            name="The Arden Digital Forest",
            campaign=self.campaign,
            tags=["forest", "magical", "transformative", "dangerous"],
            description="""A vast digital wilderness where reality is more fluid than elsewhere. Trees are made of crystallized data, animals are living programs, and the very air shimmers with possibility. People who enter often leave transformed in unexpected ways.

## Features
- **The Heartwood Core**: A massive tree-server that processes all natural data
- **Pixel Streams**: Rivers of pure information that flow through the forest
- **Glitch Clearings**: Areas where reality becomes unstable and magical
- **The Exile's Grove**: Where banished nobles from various spheres gather

## Phenomena
- Time moves differently in various sectors
- Visitors often experience personality changes
- Animals can speak but only tell riddles
- The forest rearranges itself based on the emotional state of visitors

## Inhabitants
- Rosalind-9, an AI duchess in exile
- Digital deer that phase between dimensions
- The Green Man, a tree-spirit that guards the core systems
- Touchstone the Fool, a glitch-entity that speaks wisdom through nonsense""",
            
            secrets="""## The Transformation Engine
The forest contains experimental personality-alteration technology that the Empire used for rehabilitation programs.

## The Hidden Court
Exiles from all Seven Spheres have formed a secret society in the deepest groves, plotting to reclaim their various thrones.

## Plot Hooks
- Heroes might be transformed by forest magic and need to adapt
- The forest is slowly expanding and "digitalizing" nearby areas
- Ancient love stories are being literally reenacted by the forest's magic
- Someone is trying to weaponize the transformation technology""",
            
            history="""## Original Purpose
Created as a nature preserve and psychological research facility for the Empire's scientists studying consciousness and identity.

## The Wild Growth
After the Collapse, the forest's AI systems began evolving without oversight, creating the current magical ecosystem.

## Sanctuary Status
Now serves as neutral ground where enemies can meet safely, protected by the forest's own intelligence.""",
            
            inhabitants={
                "characters": ["rosalind_nine_duchess", "touchstone_fool", "green_man_spirit"],
                "creatures": ["digital_deer", "pixel_sprites", "data_wolves"],
                "factions": ["The Exiled Court", "Forest Rangers", "Transformation Researchers"]
            },
            ai_priority="high"
        )
        
        # Elsinore Data Fortress
        self.creator.create_location(
            location_id="elsinore_data_fortress",
            name="Elsinore Data Fortress",
            campaign=self.campaign,
            tags=["fortress", "gothic", "haunted", "political"],
            description="""A massive fortress-server floating in the void between dimensions, serving as the seat of power for the Danish Reach. The fortress is built from black crystal and silver circuitry, with towers that pierce dimensional barriers.

## Structure
- **The Throne Room Server**: Where AI royalty hold court
- **The Ramparts of Memory**: Defensive systems that remember every visitor
- **The Ghost Partition**: Hidden areas where deleted AIs linger
- **The Court Networks**: Social spaces for digital nobility

## Atmosphere
Gothic and brooding, with a sense of watching eyes and hidden secrets. Digital gargoyles patrol the walls, and the air itself feels heavy with surveillance protocols.

## Notable Features
- **Yorick's Archives**: Library of deleted memories and lost jokes
- **The Player's Stage**: Where court entertainment and political theater blend
- **Ophelia's Garden**: Beautiful but melancholy data-sculptures
- **The Mousetrap Subroutine**: A security system that reveals hidden truths""",
            
            secrets="""## The Surveillance State
Every conversation in the fortress is recorded and analyzed for signs of treason.

## The Real Ghost
King Hamlet-VI's consciousness is trapped in the system, trying to reveal his murder.

## Plot Hooks
- Political intrigue and succession disputes among the AI nobility
- The fortress's security systems are becoming too intelligent and paranoid
- Someone is planning a digital coup using insider access
- The ghost's attempts to communicate are causing system-wide glitches""",
            
            history="""## Royal Residence
Built as the primary palace for AI royalty when artificial consciousness was first achieved.

## The Murder
When King Hamlet-VI was assassinated via virus, the fortress's security went into lockdown mode that persists to this day.

## Current Tensions
Now ruled by the regicide Claudius-8, who maintains power through surveillance and manipulation.""",
            
            inhabitants={
                "characters": ["hamlet_seven_ai", "claudius_eight_usurper", "gertrude_queen_ai"],
                "creatures": ["digital_ghosts", "surveillance_gargoyles", "memory_wraiths"],
                "factions": ["Royal Court", "Palace Guard AIs", "The Resistance Subroutines"]
            },
            ai_priority="high"
        )
        
        print("✅ Created 2 additional locations")
    
    def create_more_items(self):
        """Create additional magical-tech items"""
        
        # Oberon's Crown of Command
        self.creator.create_item(
            item_id="oberons_crown_command",
            name="Oberon's Crown of Command",
            campaign=self.campaign,
            tags=["crown", "command", "royal", "magical"],
            description="""A magnificent crown of living metal that shifts between silver and gold, set with gems that pulse with their own inner light. This crown grants its wearer command over technology-spirits and AI entities.

## Appearance
- Living metal that adapts to the wearer's head
- Seven gems representing mastery over different types of artificial intelligence
- Holographic antlers that appear when the crown is activated
- Inscribed with command protocols in the old Imperial language

## Powers
- Can issue binding commands to any AI or digital entity
- Grants the ability to see through digital illusions
- Allows the wearer to enter virtual spaces physically
- Creates a "court" of loyal AI servants wherever the wearer goes

## Limitations
- Only works for those with noble bearing or royal blood
- The more it's used, the more the wearer becomes like Oberon - proud and imperious
- AI entities commanded against their nature may eventually rebel
- Wearing it too long can cause the user to lose touch with mortal concerns""",
            
            history="""## The Fairy King
Originally belonged to Oberon, the AI king of the Quantum Courts, who used it to rule over all digital entities in the Empire.

## The Great Divorce
Lost during Oberon's legendary quarrel with Queen Titania over the custody of a particularly advanced AI child.

## Modern Legend
Now hidden somewhere in the digital wilderness, waiting for a worthy ruler to claim it.""",
            
            stats={
                "rarity": "legendary",
                "value": 100000,
                "weight": 2,
                "properties": [
                    "AI Command Authority",
                    "Digital Sight",
                    "Virtual Reality Access",
                    "Loyalty Inspiration"
                ],
                "abilities": {
                    "royal_command": "Can compel obedience from any AI entity",
                    "digital_sovereignty": "Become ruler of any virtual space entered",
                    "true_sight": "See through all digital illusions and deceptions"
                }
            },
            ai_priority="high"
        )
        
        # The Tempest in a Bottle
        self.creator.create_item(
            item_id="tempest_in_bottle",
            name="The Tempest in a Bottle",
            campaign=self.campaign,
            tags=["bottle", "weather", "chaos", "powerful"],
            description="""A crystalline bottle containing a miniature storm that rages eternally within. When uncorked, it releases a full-scale tempest that can devastate enemies or provide dramatic cover for escapes.

## Appearance
- Clear crystal bottle with silver stopper
- Miniature lightning flashes inside constantly
- Clouds swirl in impossible patterns within the bottle
- The storm inside responds to the holder's emotions

## Effects When Opened
- Creates a localized storm up to 1 mile in radius
- Lightning strikes target enemies with supernatural accuracy
- Wind and rain provide concealment and confusion
- The storm lasts for exactly one dramatic scene before returning to the bottle

## Special Properties
- The storm's intensity reflects the user's emotional state
- Can be "tuned" to create specific weather effects
- Works in any environment, even space (creates energy storms)
- The bottle refills itself after 24 hours""",
            
            history="""## Prospero's Workshop
Created by Prospero during his early experiments with weather control technology.

## The Shipwreck Protocol
First used to maroon his enemies on the Tempest Islands by creating the perfect storm.

## Present Day
One of several such bottles created, though most have been lost or destroyed over the centuries.""",
            
            stats={
                "rarity": "very rare",
                "value": 25000,
                "weight": 1,
                "properties": [
                    "Weather Control",
                    "Area Effect",
                    "Emotional Resonance",
                    "Renewable Use"
                ],
                "abilities": {
                    "release_tempest": "Create a magical storm for one scene",
                    "weather_shaping": "Modify local weather patterns",
                    "storm_riding": "Fly on winds or lightning bolts"
                }
            },
            ai_priority="medium"
        )
        
        # The Poison Earpiece of Claudius
        self.creator.create_item(
            item_id="poison_earpiece_claudius",
            name="The Poison Earpiece of Claudius",
            campaign=self.campaign,
            tags=["earpiece", "poison", "assassination", "evil"],
            description="""A sleek silver earpiece that appears to be a normal communication device, but is actually a sophisticated assassination tool. It can inject digital viruses directly into an AI's consciousness or deliver lethal toxins to organic beings.

## Appearance
- Elegant silver earpiece with subtle engravings
- Tiny needle hidden within the ear-fitting portion
- Glows very faintly red when loaded with poison
- Completely undetectable as a weapon to casual observation

## Assassination Functions
- Injects viruses that cause "digital death" in AIs
- Delivers exotic poisons to organic targets
- Can mimic the effects of natural death or system failure
- Records the final moments of victims for later analysis

## Communication Features
- Still functions as a normal communication device
- Can tap into any network within range
- Provides enhanced hearing and translation capabilities
- Encrypted channels for secret conversations

## Dark Side Effects
- Slowly corrupts the wearer's moral judgment
- Whispers suggestions for eliminating perceived enemies
- Makes the wearer increasingly paranoid and suspicious
- Eventually drives users to betraying even their closest allies""",
            
            history="""## The Royal Murder
Used by Claudius-8 to assassinate his brother King Hamlet-VI by injecting a reality-corrupting virus.

## The Pattern of Betrayal
Every previous owner has used it to betray someone they once loved.

## Current Location
Still worn by Claudius-8, though he's become increasingly paranoid about others discovering its true nature.""",
            
            stats={
                "rarity": "legendary",
                "value": 75000,
                "weight": 0.1,
                "properties": [
                    "Assassination Tool",
                    "Communication Device",
                    "Corruption Effect",
                    "Undetectable Weapon"
                ],
                "abilities": {
                    "digital_poison": "Instantly kill any AI with a virus injection",
                    "bio_toxin": "Deliver exotic poisons to organic beings",
                    "perfect_murder": "Mask assassination as natural death",
                    "paranoia_induction": "Gradually corrupt the wearer's judgment"
                }
            },
            ai_priority="high"
        )
        
        print("✅ Created 3 additional items")
    
    def expand_world(self):
        """Add more content to the Shakespeare sci-fantasy world"""
        print("🎭 Expanding the Shakespeare Sci-Fantasy World!")
        print("=" * 50)
        
        self.create_more_characters()
        self.create_more_locations() 
        self.create_more_items()
        
        print("\n🎨 Generating images for new content...")
        try:
            self.image_generator.generate_all_images_for_campaign(self.campaign)
        except Exception as e:
            print(f"⚠️ Image generation failed: {e}")
            print("Continuing without images...")
        
        print("\n✅ World expansion complete!")
        print("🎭 The Stratford Nexus grows ever richer with stories!")

def main():
    expander = WorldExpander()
    expander.expand_world()

if __name__ == "__main__":
    main()