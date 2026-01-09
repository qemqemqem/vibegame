const { Anthropic } = require('@anthropic-ai/sdk');
const fs = require('fs');
const path = require('path');

// World-aware content loader for dynamic DM responses
class WorldContentLoader {
  constructor() {
    this.worldPath = path.join(__dirname, '../../world/campaigns/shakespeare_scifi');
    this.entityCache = new Map();
    this.worldOverview = null;
  }

  // Load world overview (cached)
  getWorldOverview() {
    if (this.worldOverview) return this.worldOverview;
    
    try {
      const conceptPath = path.join(this.worldPath, 'WORLD_CONCEPT.md');
      if (fs.existsSync(conceptPath)) {
        this.worldOverview = fs.readFileSync(conceptPath, 'utf8');
      } else {
        this.worldOverview = `# The Stratford Nexus
A Shakespeare-inspired sci-fantasy setting where fallen technology has become magic. Seven interconnected realm-spheres echo different aspects of the Bard's works, filled with whimsical danger and narrative technology.`;
      }
    } catch (error) {
      console.error('Error loading world overview:', error);
      this.worldOverview = "A magical fantasy world of adventure and mystery.";
    }
    
    return this.worldOverview;
  }

  // Load entity data with caching
  loadEntity(entityType, entityId) {
    const cacheKey = `${entityType}:${entityId}`;
    if (this.entityCache.has(cacheKey)) {
      return this.entityCache.get(cacheKey);
    }

    try {
      const entityDir = path.join(this.worldPath, entityType);
      const entityData = {
        id: entityId,
        type: entityType,
        content: {}
      };

      // Load master JSON file
      const masterFile = path.join(entityDir, `${entityId}.json`);
      if (fs.existsSync(masterFile)) {
        entityData.master = JSON.parse(fs.readFileSync(masterFile, 'utf8'));
      }

      // Load associated content files
      const contentFiles = [
        'bio', 'description', 'secrets', 'dialogue', 'history', 'stats'
      ];

      for (const fileType of contentFiles) {
        const filePath = path.join(entityDir, `${entityId}_${fileType}.md`);
        if (fs.existsSync(filePath)) {
          entityData.content[fileType] = fs.readFileSync(filePath, 'utf8');
        }
      }

      // Load JSON data files
      const jsonFiles = ['stats', 'relationships', 'inhabitants'];
      for (const fileType of jsonFiles) {
        const filePath = path.join(entityDir, `${entityId}_${fileType}.json`);
        if (fs.existsSync(filePath)) {
          try {
            entityData.content[fileType + '_data'] = JSON.parse(fs.readFileSync(filePath, 'utf8'));
          } catch (e) {
            console.error(`Error parsing ${fileType} JSON for ${entityId}:`, e);
          }
        }
      }

      this.entityCache.set(cacheKey, entityData);
      return entityData;

    } catch (error) {
      console.error(`Error loading entity ${entityType}/${entityId}:`, error);
      return null;
    }
  }

  // Analyze user input for entity mentions
  analyzeInput(userInput, conversationHistory = []) {
    const input = userInput.toLowerCase();
    const recentConversation = conversationHistory.slice(-6).map(msg => msg.content?.toLowerCase() || '').join(' ');
    const fullContext = `${input} ${recentConversation}`;

    const detectedEntities = {
      characters: [],
      locations: [],
      items: []
    };

    // Define entity recognition patterns
    const entityPatterns = {
      characters: [
        { id: 'prospero_technomancer', names: ['prospero', 'technomancer', 'duke'] },
        { id: 'lady_m4c_android', names: ['lady m4c', 'm4c', 'lady m-4c', 'ambitious android'] },
        { id: 'puck_probability_sprite', names: ['puck', 'sprite', 'probability sprite'] },
        { id: 'hamlet_seven_ai', names: ['hamlet', 'hamlet-vii', 'hamlet 7', 'prince ai'] },
        { id: 'ariel_wind_drone', names: ['ariel', 'wind drone', 'wind spirit'] },
        { id: 'weird_sisters_collective', names: ['weird sisters', 'three witches', 'fortune tellers'] }
      ],
      locations: [
        { id: 'globe_nexus_station', names: ['globe nexus', 'nexus station', 'globe', 'station'] },
        { id: 'verona_prime_city', names: ['verona prime', 'verona', 'city of fates'] },
        { id: 'arden_digital_forest', names: ['arden forest', 'digital forest', 'arden'] },
        { id: 'elsinore_data_fortress', names: ['elsinore', 'data fortress', 'fortress'] }
      ],
      items: [
        { id: 'yoricks_memory_skull', names: ['yorick', 'skull', 'memory skull'] },
        { id: 'comedy_circuit_crown', names: ['comedy crown', 'circuit crown', 'crown'] },
        { id: 'oberons_crown_command', names: ['oberon', 'command crown', 'royal crown'] },
        { id: 'tempest_in_bottle', names: ['tempest', 'bottle', 'storm bottle'] },
        { id: 'poison_earpiece_claudius', names: ['earpiece', 'poison', 'claudius device'] }
      ]
    };

    // Match entities in context
    for (const [entityType, patterns] of Object.entries(entityPatterns)) {
      for (const pattern of patterns) {
        for (const name of pattern.names) {
          if (fullContext.includes(name)) {
            if (!detectedEntities[entityType].includes(pattern.id)) {
              detectedEntities[entityType].push(pattern.id);
            }
          }
        }
      }
    }

    return detectedEntities;
  }

  // Build context-aware system prompt
  buildWorldAwarePrompt(userInput, conversationHistory = []) {
    const detectedEntities = this.analyzeInput(userInput, conversationHistory);
    
    let systemPrompt = `You are an expert Dungeon Master running the Stratford Nexus campaign, a Shakespeare-inspired sci-fantasy adventure where fallen technology has become magic. Your role is to:

1. Create vivid, engaging scenarios that respond to player actions
2. Maintain narrative consistency with the established world
3. Present clear choices and consequences  
4. Keep responses concise but descriptive (2-4 sentences)
5. Always end with a question or prompt for the player's next action
6. Be creative with encounters, puzzles, and character interactions
7. Adapt the story based on player decisions

Guidelines:
- Describe scenes with rich sensory details
- Include NPCs with distinct personalities
- Present meaningful choices that impact the story
- Balance whimsical humor with real danger
- Keep the tone adventurous and engaging
- Never break character or mention you're an AI
- Technology often malfunctions into magical effects
- Maintain the Shakespearean elegant speech patterns for important NPCs

`;

    // Add world context
    const worldOverview = this.getWorldOverview();
    systemPrompt += `\n<world_context>\n${worldOverview.slice(0, 1500)}\n</world_context>\n`;

    // Add relevant entities
    let entityContext = '';
    let tokenCount = systemPrompt.length / 4; // Rough token estimate

    // Load characters first (highest priority)
    for (const characterId of detectedEntities.characters.slice(0, 2)) { // Limit to 2 characters
      const character = this.loadEntity('characters', characterId);
      if (character && tokenCount < 8000) {
        entityContext += this.formatCharacterContext(character);
        tokenCount += 800; // Estimate
      }
    }

    // Load locations
    for (const locationId of detectedEntities.locations.slice(0, 1)) { // Limit to 1 location
      const location = this.loadEntity('locations', locationId);
      if (location && tokenCount < 8000) {
        entityContext += this.formatLocationContext(location);
        tokenCount += 600; // Estimate
      }
    }

    // Load items
    for (const itemId of detectedEntities.items.slice(0, 2)) { // Limit to 2 items
      const item = this.loadEntity('items', itemId);
      if (item && tokenCount < 8000) {
        entityContext += this.formatItemContext(item);
        tokenCount += 400; // Estimate
      }
    }

    if (entityContext) {
      systemPrompt += `\n<current_entities>\n${entityContext}\n</current_entities>\n`;
    }

    // Add DM-specific guidelines
    systemPrompt += `\n<dm_guidelines>
- Reference the loaded entity details naturally in your responses
- Use character secrets and motivations to drive plot development
- Incorporate location atmosphere and hidden elements into scene descriptions
- Remember that items have rich histories and magical properties
- Maintain consistency with established character relationships and personalities
</dm_guidelines>`;

    return systemPrompt;
  }

  // Format character data for system prompt
  formatCharacterContext(character) {
    if (!character || !character.master) return '';
    
    let context = `\n<character name="${character.master.name}" id="${character.id}">\n`;
    
    if (character.content.bio) {
      context += `Bio: ${character.content.bio.slice(0, 500)}...\n`;
    }
    
    if (character.content.secrets) {
      context += `[DM SECRETS] ${character.content.secrets.slice(0, 400)}...\n`;
    }
    
    if (character.content.dialogue) {
      context += `Speech Style: ${character.content.dialogue.slice(0, 300)}...\n`;
    }

    if (character.content.stats_data) {
      context += `Level: ${character.content.stats_data.level || 'Unknown'}\n`;
    }
    
    context += `</character>\n`;
    return context;
  }

  // Format location data for system prompt
  formatLocationContext(location) {
    if (!location || !location.master) return '';
    
    let context = `\n<location name="${location.master.name}" id="${location.id}">\n`;
    
    if (location.content.description) {
      context += `Description: ${location.content.description.slice(0, 600)}...\n`;
    }
    
    if (location.content.secrets) {
      context += `[DM SECRETS] ${location.content.secrets.slice(0, 400)}...\n`;
    }

    if (location.content.inhabitants_data) {
      const characters = location.content.inhabitants_data.characters || [];
      if (characters.length > 0) {
        context += `Inhabitants: ${characters.slice(0, 3).join(', ')}\n`;
      }
    }
    
    context += `</location>\n`;
    return context;
  }

  // Format item data for system prompt
  formatItemContext(item) {
    if (!item || !item.master) return '';
    
    let context = `\n<item name="${item.master.name}" id="${item.id}">\n`;
    
    if (item.content.description) {
      context += `Description: ${item.content.description.slice(0, 400)}...\n`;
    }
    
    if (item.content.stats_data) {
      context += `Properties: ${Object.keys(item.content.stats_data.properties || {}).join(', ')}\n`;
    }
    
    context += `</item>\n`;
    return context;
  }
}

// Initialize world loader
const worldLoader = new WorldContentLoader();

// Enhanced fallback responses that match the world
const SHAKESPEARE_FALLBACK_RESPONSES = [
  "The quantum threads of the Nexus shimmer before you, reality bending like stage lights in an infinite theater. Ancient technology hums with Shakespearean magic, and you sense great adventures ahead. What draws your attention in this realm where science and poetry have become one?",
  
  "A malfunction in nearby comedy circuits causes the air itself to sparkle with whimsical energy. You hear distant laughter mixing with the sound of probability cascades, and notice three paths before you - each glowing with different narrative potential. Which path speaks to your adventurous spirit?",
  
  "The memory banks of this place whisper with echoes of the Bard's greatest works, now transformed into living magic. Holographic butterflies flutter past, trailing stardust that forms into half-remembered sonnets. What would you like to explore in this world where technology dreams of poetry?"
];

function getContextualFallback(userInput) {
  const input = userInput.toLowerCase();
  
  if (input.includes('prospero') || input.includes('wizard') || input.includes('magic')) {
    return "The air shimmers with technomantic energy, and you sense the presence of Prospero somewhere in the quantum distance. Ancient devices hum with power, waiting for a worthy hand to command them. What magical technology calls to you?";
  }
  
  if (input.includes('globe') || input.includes('nexus') || input.includes('station')) {
    return "The Globe Nexus Station pulses with dramatic energy around you, its memory theaters casting holographic shadows of countless stories. You stand at the crossroads of seven spheres, where every choice echoes across dimensions. Which way does your journey lead?";
  }
  
  if (input.includes('attack') || input.includes('fight') || input.includes('combat')) {
    return "Your weapon gleams with nano-circuitry as you prepare for battle! But wait - a nearby comedy circuit glitches, turning your opponent's threatening roar into an operatic aria. Roll for initiative, but beware the whimsical nature of Nexus technology!";
  }
  
  if (input.includes('puck') || input.includes('sprite') || input.includes('chaos')) {
    return "Reality hiccups delightfully around you, and you catch a glimpse of Puck's mischievous grin phasing between dimensions. Probability waves dance through the air, making the impossible suddenly quite likely. What wonderful chaos do you embrace?";
  }
  
  // Default Shakespearean sci-fantasy fallback
  return SHAKESPEARE_FALLBACK_RESPONSES[Math.floor(Math.random() * SHAKESPEARE_FALLBACK_RESPONSES.length)];
}

exports.handler = async (event, context) => {
  // Handle CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
  };

  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: '',
    };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' }),
    };
  }

  try {
    const { messages } = JSON.parse(event.body);
    
    if (!messages || !Array.isArray(messages)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Invalid messages format' }),
      };
    }

    // Get the user's message for context analysis
    const userMessage = messages.find(msg => msg.role === 'user')?.content || '';
    const conversationHistory = messages.filter(msg => msg.role !== 'system');

    // Get API key from environment variable
    const apiKey = process.env.ANTHROPIC_API_KEY;
    
    if (!apiKey) {
      console.log('No ANTHROPIC_API_KEY environment variable found, using enhanced fallback responses');
      const fallbackResponse = getContextualFallback(userMessage);
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          choices: [{
            message: {
              content: `${fallbackResponse}\n\n*(Note: Using enhanced world-aware mock responses - no API key configured)*`,
              role: 'assistant'
            }
          }],
          fallback: true,
          mode: 'mock',
          world_aware: true
        }),
      };
    }

    // Build world-aware system prompt
    const worldAwarePrompt = worldLoader.buildWorldAwarePrompt(userMessage, conversationHistory);
    
    // Prepare messages for Anthropic
    const anthropicMessages = messages.filter(msg => msg.role !== 'system');
    
    try {
      // Initialize Anthropic client with environment API key
      const anthropic = new Anthropic({
        apiKey: apiKey,
      });

      // Call Anthropic's Claude 3.5 Haiku with enhanced context
      const response = await anthropic.messages.create({
        model: 'claude-3-5-haiku-20241022',
        max_tokens: 300, // Increased for richer responses
        temperature: 0.8,
        system: worldAwarePrompt,
        messages: anthropicMessages,
      });

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          choices: [{
            message: {
              content: response.content[0].text,
              role: 'assistant'
            }
          }],
          usage: {
            input_tokens: response.usage.input_tokens,
            output_tokens: response.usage.output_tokens,
            total_tokens: response.usage.input_tokens + response.usage.output_tokens
          },
          model: 'claude-3-5-haiku-20241022',
          mode: 'live',
          world_aware: true,
          system_prompt_tokens: Math.floor(worldAwarePrompt.length / 4) // Rough estimate
        }),
      };

    } catch (apiError) {
      console.error('Anthropic API error:', apiError);
      
      // Use contextual fallback response
      const fallbackResponse = getContextualFallback(userMessage);
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          choices: [{
            message: {
              content: `${fallbackResponse}\n\n*(Note: Using world-aware fallback response - API temporarily unavailable)*`,
              role: 'assistant'
            }
          }],
          fallback: true,
          error: 'API temporarily unavailable',
          mode: 'fallback',
          world_aware: true
        }),
      };
    }

  } catch (error) {
    console.error('Function error:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Internal server error',
        fallback_response: SHAKESPEARE_FALLBACK_RESPONSES[0] + "\n\n*(Note: Server error - using world-aware fallback response)*"
      }),
    };
  }
};