# 🚀 Netlify Deployment Guide

## Overview
The Vibe Game is now configured to use server-side API key management through Netlify environment variables. This provides a better user experience by eliminating the need for users to provide their own API keys.

## Setting Up Environment Variables

### Step 1: Get Your Anthropic API Key
1. Visit [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in to your account
3. Go to "API Keys" section
4. Create a new API key
5. Copy the API key (starts with `sk-ant-api`)

### Step 2: Configure Netlify Environment Variables
1. Go to your Netlify site dashboard
2. Navigate to **Site settings** → **Environment variables**
3. Click **Add a variable**
4. Set the following:
   - **Key**: `ANTHROPIC_API_KEY`
   - **Value**: Your Anthropic API key (the full `sk-ant-api...` string)
   - **Scopes**: Select both "Build" and "Runtime" (or just "Runtime" if available)
5. Click **Save**

### Step 3: Deploy
1. Push your changes to your repository
2. Netlify will automatically rebuild and deploy
3. The game will now use your server-side API key

## How It Works

### With API Key Configured
- Users can play immediately without any setup
- All AI responses come from Claude 3.5 Haiku
- API costs are controlled by you (the site owner)
- Users get a seamless experience

### Without API Key (Fallback Mode)
- The game automatically uses mock responses
- Users can still play and enjoy the game
- No API costs incurred
- Perfect for testing and development

## API Cost Management

### Estimated Costs (Claude 3.5 Haiku)
- **Input tokens**: ~$0.0001 per 1K tokens
- **Output tokens**: ~$0.0005 per 1K tokens
- **Average message**: ~$0.0008 per exchange
- **Daily usage**: For 100 messages/day = ~$0.08/day

### Cost Control Strategies
1. **Rate Limiting**: The function naturally limits rapid requests
2. **Response Length**: Limited to 200 tokens per response
3. **Monitoring**: Check Netlify Functions usage in your dashboard
4. **Fallback**: Game gracefully handles API failures

## Testing Your Deployment

### Verify Environment Variable
1. Check your Netlify site dashboard
2. Go to **Site settings** → **Environment variables**
3. Confirm `ANTHROPIC_API_KEY` is listed

### Test the Game
1. Visit your deployed site
2. Try sending a message
3. Check the browser console for logs:
   - `🤖 Using live AI responses` = API key working
   - `🎭 Using mock mode` = No API key or fallback mode

### Debug Issues
If the game uses fallback responses when you expect AI responses:

1. **Check Environment Variable**:
   - Ensure `ANTHROPIC_API_KEY` is set correctly
   - Verify the API key format (starts with `sk-ant-api`)

2. **Check Netlify Function Logs**:
   - Go to **Site settings** → **Functions**
   - Click on the `chat` function
   - Check the execution logs for errors

3. **Test API Key Manually**:
   ```bash
   curl -X POST https://api.anthropic.com/v1/messages \
     -H "Content-Type: application/json" \
     -H "x-api-key: YOUR_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -d '{"model": "claude-3-5-haiku-20241022", "max_tokens": 10, "messages": [{"role": "user", "content": "Hello"}]}'
   ```

## Security Benefits

### Server-Side API Key Management
- API keys never exposed to client browsers
- No risk of API key theft from client-side code
- Centralized key management
- Easy to rotate keys without affecting users

### Fallback Safety
- Game works even if API fails
- Graceful degradation to mock responses
- No broken user experience

## Maintenance

### Monitoring Usage
- Check Netlify Functions dashboard for usage
- Monitor API costs in Anthropic console
- Set up billing alerts if needed

### Updating the API Key
1. Generate new API key in Anthropic console
2. Update the `ANTHROPIC_API_KEY` environment variable in Netlify
3. The change takes effect immediately (no rebuild needed)

### Scaling Considerations
- Claude 3.5 Haiku is designed for high throughput
- Netlify Functions can handle concurrent requests
- Consider upgrading to Claude 3.5 Sonnet for better responses if needed

## Alternative Deployment Options

### GitHub Pages (Fallback Mode Only)
If you prefer GitHub Pages, the game will automatically use mock responses since GitHub Pages doesn't support server-side environment variables.

### Self-Hosted
You can run the Python backend server with environment variables:
```bash
export ANTHROPIC_API_KEY=your_key_here
python backend/server.py
```

## Troubleshooting

### Common Issues
1. **"Using mock mode"**: API key not set or invalid
2. **"API temporarily unavailable"**: Rate limiting or API issues
3. **Function timeout**: Increase timeout in `netlify.toml` if needed

### Getting Help
- Check the browser console for detailed error messages
- Review Netlify Function logs
- Verify your API key is active in Anthropic console

---

🎲 **Happy Gaming!** Your players can now enjoy seamless AI-powered adventures without any setup required.