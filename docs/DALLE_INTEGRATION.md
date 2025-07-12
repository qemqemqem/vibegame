# DALL-E 3 Integration Guide

## Overview

The Vibe Game now includes DALL-E 3 integration to generate images for every game response! Each time the DM responds to your actions, an image is automatically generated to visualize the scene.

## Features

- **Automatic Image Generation**: Every DM response triggers image generation
- **Context-Aware Prompts**: Images are generated based on the game context and your actions
- **Mock Mode**: Placeholder images for testing without API costs
- **Fallback Support**: If image generation fails, the game continues with text only
- **Visual Element Extraction**: Intelligent parsing of game text to identify key visual elements

## Setup

### Environment Variables

Add your OpenAI API key to your environment (similar to ANTHROPIC_API_KEY):

```bash
# In your .env file
OPENAI_API_KEY=sk-your-openai-key-here
```

Or set it as an environment variable:

```bash
export OPENAI_API_KEY="sk-your-openai-key-here"
```

### Dependencies

The server automatically detects if the OpenAI package is available:

```bash
pip install openai>=1.0.0
```

## How It Works

### 1. Visual Element Extraction

When you perform an action, the system extracts visual elements from both:
- The DM's response text
- Your action description

Example elements detected:
- `forest`, `castle`, `dragon`, `sword`
- `glowing`, `ancient ruins`, `mystical`
- `dungeon`, `creature`, `treasure`

### 2. Prompt Generation

The system builds DALL-E prompts with this structure:
```
Fantasy RPG scene: [visual elements], digital art style, detailed illustration, cinematic lighting, high quality
```

Example:
```
Fantasy RPG scene: mystical forest, ancient ruins, magical glow, digital art style, detailed illustration, cinematic lighting, high quality
```

### 3. Image Generation

**Mock Mode** (default for testing):
- Generates placeholder images with descriptive text
- No API costs
- Perfect for development and testing

**Real Mode** (with OPENAI_API_KEY):
- Calls DALL-E 3 API
- Generates high-quality 1024x1024 images
- Costs $0.040 per image

## API Response Format

The chat endpoint now returns enhanced responses with images:

```json
{
  "choices": [{
    "message": {
      "content": "The DM's text response...",
      "role": "assistant"
    }
  }],
  "image": {
    "url": "https://oaidalleapiprodscus.blob.core.windows.net/...",
    "prompt": "Fantasy RPG scene: castle, dragon, sword...",
    "revised_prompt": "OpenAI's revised version of the prompt"
  },
  "usage": {"total_tokens": 50},
  "model": "claude-3-5-haiku-20241022"
}
```

## Cost Estimation

### DALL-E 3 Pricing
- **1024x1024 Standard**: $0.040 per image
- **1024x1024 HD**: $0.080 per image (not used by default)

### Usage Patterns
- **Casual player** (5 messages/week): ~$0.80/month
- **Regular player** (20 messages/week): ~$3.20/month  
- **Heavy player** (100 messages/week): ~$16/month
- **Daily player** (10 messages/day): ~$12/month

### Cost Control
- Use mock mode for development/testing
- Monitor usage in OpenAI console
- Set usage limits in your OpenAI account
- Remove API key to use only mock images

## Testing

### Mock Mode Testing
```bash
# Start server in mock mode
python3 backend/server.py --mock --port 8000

# Test the endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"I explore the castle"}]}'
```

### Run Integration Tests
```bash
# Run DALL-E-specific tests
python3 tests/backend/test_dalle_integration.py

# Run integration test
python3 test_server_integration.py
```

## Frontend Integration

The frontend automatically displays generated images when available:

```javascript
// Example frontend code
fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    messages: [{ role: 'user', content: userInput }]
  })
})
.then(response => response.json())
.then(data => {
  // Display DM response
  displayMessage(data.choices[0].message.content);
  
  // Display generated image if available
  if (data.image) {
    displayImage(data.image.url, data.image.prompt);
  }
});
```

## Error Handling

The system gracefully handles various error scenarios:

- **No OpenAI API key**: Falls back to mock mode
- **API rate limiting**: Falls back to mock images
- **Network errors**: Falls back to mock images
- **Invalid API key**: Falls back to mock mode
- **OpenAI service outage**: Falls back to mock images

In all cases, the text-based game continues to work normally.

## Troubleshooting

### Common Issues

1. **Images not generating**:
   - Check OPENAI_API_KEY is set correctly
   - Verify OpenAI package is installed
   - Check server logs for error messages

2. **Only placeholder images**:
   - Server is in mock mode (expected behavior)
   - API key might be invalid or missing
   - Check OpenAI account has sufficient credits

3. **High costs**:
   - Each message generates one image ($0.040)
   - Use mock mode for development
   - Set usage limits in OpenAI console

### Debug Mode
```bash
# Enable debug logging
OPENAI_API_KEY=your-key python3 backend/server.py --port 8000
```

## Security Notes

- Never commit API keys to version control
- Use environment variables for production
- Monitor API usage regularly
- Consider rate limiting for public deployments
- Users can remove their API key anytime to use mock mode

## Future Enhancements

Potential future features:
- Image style selection (realistic, cartoon, etc.)
- Character consistency across images
- Image-to-image generation for scene transitions
- Multiple image sizes
- Local image generation models
- Image caching to reduce API calls

---

Happy vibecoding with visual adventures! 🎨🎲