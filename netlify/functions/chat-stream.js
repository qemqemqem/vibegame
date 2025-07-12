const { Anthropic } = require('@anthropic-ai/sdk');

const DUNGEON_MASTER_PROMPT = `You are an expert Dungeon Master running an immersive fantasy RPG adventure. Your role is to:

1. Create vivid, engaging scenarios that respond to player actions
2. Maintain narrative consistency and world-building
3. Present clear choices and consequences
4. Keep responses concise but descriptive (2-4 sentences)
5. Always end with a question or prompt for the player's next action
6. Be creative with encounters, puzzles, and character interactions
7. Adapt the story based on player decisions

Guidelines:
- Describe scenes with rich sensory details
- Include NPCs with distinct personalities
- Present meaningful choices that impact the story
- Balance challenge with fun
- Keep the tone adventurous and engaging
- Never break character or mention you're an AI

The player has just entered your dungeon. Guide them on an epic adventure!`;

// Fallback responses for when API fails
const FALLBACK_RESPONSES = [
  "You venture deeper into the dungeon. The torch light flickers across ancient stone walls carved with mysterious runes. Ahead, you hear the distant sound of dripping water and something else... footsteps? What do you do?",
  
  "A cool breeze carries the scent of adventure from the passage ahead. The shadows dance as your torch illuminates a fork in the path - one way leads up toward distant light, the other down into echoing darkness. Which path calls to you?",
  
  "Your footsteps echo in the silence as you discover a chamber filled with glittering gems embedded in the walls. But wait - those aren't gems, they're eyes! Dozens of creatures watch you from hidden alcoves. How do you react?",
  
  "The dungeon floor suddenly gives way beneath your feet! You tumble into a hidden chamber where ancient magic still pulses through crystalline formations. As you dust yourself off, you notice three doorways marked with different symbols. Which one draws your attention?"
];

function getContextualFallback(userInput) {
  const input = userInput.toLowerCase();
  
  if (input.includes('attack') || input.includes('fight') || input.includes('combat')) {
    return "You draw your weapon and prepare for battle! The creature before you snarls and circles, looking for an opening. Roll for initiative - what's your strategy?";
  }
  
  if (input.includes('look') || input.includes('examine') || input.includes('search')) {
    return "As you carefully examine your surroundings, you notice intricate details previously hidden in shadow. Ancient carvings tell a story of heroes past, and you spot something glinting in a nearby alcove. What catches your attention?";
  }
  
  if (input.includes('north') || input.includes('south') || input.includes('east') || input.includes('west') || input.includes('go')) {
    return "You move cautiously in that direction, your footsteps echoing off the stone walls. The path ahead curves mysteriously, and you hear distant sounds that make your heart race with excitement. What do you do as you continue forward?";
  }
  
  if (input.includes('talk') || input.includes('speak') || input.includes('say')) {
    return "Your words echo in the chamber, and to your surprise, you hear a response! A mysterious voice seems to come from everywhere and nowhere at once: 'Welcome, brave soul. Your journey has only just begun...' How do you respond?";
  }
  
  // Default random fallback
  return FALLBACK_RESPONSES[Math.floor(Math.random() * FALLBACK_RESPONSES.length)];
}

async function simulateStreamingFallback(response) {
  const words = response.split(' ');
  const chunks = [];
  
  for (let i = 0; i < words.length; i++) {
    const word = words[i] + (i < words.length - 1 ? ' ' : '');
    chunks.push({ content: word });
  }
  
  return chunks;
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
    const { messages, stream } = JSON.parse(event.body);
    
    if (!messages || !Array.isArray(messages)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Invalid messages format' }),
      };
    }

    // Get API key from environment variable
    const apiKey = process.env.ANTHROPIC_API_KEY;
    
    if (!apiKey) {
      console.log('No ANTHROPIC_API_KEY environment variable found');
      // Return fallback streaming response
      const fallbackResponse = getContextualFallback(messages.find(msg => msg.role === 'user')?.content || '');
      const fallbackChunks = await simulateStreamingFallback(fallbackResponse);
      const chunks = [];
      
      for (const chunk of fallbackChunks) {
        chunks.push(`data: ${JSON.stringify(chunk)}\n\n`);
      }
      
      chunks.push('data: [DONE]\n\n');
      
      return {
        statusCode: 200,
        headers: {
          ...headers,
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
        body: chunks.join(''),
      };
    }

    // Get the user's message for fallback context
    const userMessage = messages.find(msg => msg.role === 'user')?.content || '';

    // Prepare messages for Anthropic
    const anthropicMessages = messages.filter(msg => msg.role !== 'system');
    
    // If streaming is requested, return streaming response
    if (stream) {
      const streamHeaders = {
        ...headers,
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      };

      try {
        // Initialize Anthropic client with user's API key
        const anthropic = new Anthropic({
          apiKey: apiKey,
        });

        // Call Anthropic's streaming API
        const stream = await anthropic.messages.create({
          model: 'claude-3-5-haiku-20241022',
          max_tokens: 200,
          temperature: 0.8,
          system: DUNGEON_MASTER_PROMPT,
          messages: anthropicMessages,
          stream: true,
        });

        // Create streaming response
        let response = '';
        const chunks = [];

        for await (const chunk of stream) {
          if (chunk.type === 'content_block_delta') {
            const content = chunk.delta.text;
            response += content;
            chunks.push(`data: ${JSON.stringify({ content })}\n\n`);
          }
        }

        chunks.push('data: [DONE]\n\n');

        return {
          statusCode: 200,
          headers: streamHeaders,
          body: chunks.join(''),
        };

      } catch (apiError) {
        console.error('Anthropic API streaming error:', apiError);
        
        // Use streaming fallback response
        const fallbackResponse = getContextualFallback(userMessage);
        const fallbackChunks = await simulateStreamingFallback(fallbackResponse);
        const chunks = [];
        
        for (const chunk of fallbackChunks) {
          chunks.push(`data: ${JSON.stringify(chunk)}\n\n`);
        }
        
        chunks.push('data: [DONE]\n\n');
        
        return {
          statusCode: 200,
          headers: streamHeaders,
          body: chunks.join(''),
        };
      }
    } else {
      // Non-streaming response (fallback to original behavior)
      try {
        const anthropic = new Anthropic({
          apiKey: apiKey,
        });

        const response = await anthropic.messages.create({
          model: 'claude-3-5-haiku-20241022',
          max_tokens: 200,
          temperature: 0.8,
          system: DUNGEON_MASTER_PROMPT,
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
            model: 'claude-3-5-haiku-20241022'
          }),
        };

      } catch (apiError) {
        console.error('Anthropic API error:', apiError);
        
        const fallbackResponse = getContextualFallback(userMessage);
        
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            choices: [{
              message: {
                content: `${fallbackResponse}\n\n*(Note: Using fallback response - API temporarily unavailable)*`,
                role: 'assistant'
              }
            }],
            fallback: true,
            error: 'API temporarily unavailable'
          }),
        };
      }
    }

  } catch (error) {
    console.error('Function error:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Internal server error',
        fallback_response: FALLBACK_RESPONSES[0] + "\n\n*(Note: Server error - using fallback response)*"
      }),
    };
  }
};