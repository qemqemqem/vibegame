# 🔐 API Key Setup for Live Claude Integration

## Overview
Your Vibe Game now uses **Claude 3.5 Haiku** (Anthropic's fastest & cheapest model) for real AI dungeon mastering! Here's how to set up the API key securely.

## 🚀 Quick Setup Guide

### 1. Get Your Anthropic API Key
1. Go to https://console.anthropic.com/
2. Sign up/login to your account
3. Navigate to "API Keys" section
4. Create a new API key
5. Copy the key (starts with `sk-ant-api...`)

### 2. For GitHub Pages Deployment (Current Setup)

**⚠️ Important**: GitHub Pages only serves static files, so we need to switch to Netlify for the serverless function to work.

#### Option A: Deploy to Netlify (Recommended)
```bash
# 1. Install Netlify CLI
npm install -g netlify-cli

# 2. Login to Netlify
netlify login

# 3. Deploy your site
netlify deploy --prod --dir=frontend --functions=netlify/functions

# 4. Set the API key securely
netlify env:set ANTHROPIC_API_KEY your-api-key-here
```

#### Option B: Keep GitHub Pages + External API
- Deploy the serverless function to Vercel/Railway separately
- Update frontend to point to that API endpoint

### 3. For Local Development
```bash
# Create a .env file (this will be gitignored)
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env

# Run with environment variables
export ANTHROPIC_API_KEY="your-api-key-here"
python backend/server.py
```

### 4. Security Configuration

#### Environment Variables (NEVER commit API keys!)
```bash
# ✅ GOOD - Environment variables
export ANTHROPIC_API_KEY="sk-ant-api..."

# ❌ BAD - Never put in code
const apiKey = "sk-ant-api...";  // NEVER DO THIS!
```

#### .gitignore Update
```bash
# Add to .gitignore
.env
.env.local
.env.production
*.key
secrets/
```

## 🏗️ Deployment Options

### Option 1: Netlify (Recommended for this setup)
```bash
# 1. Connect your GitHub repo to Netlify
# 2. Set build settings:
#    - Build command: (leave empty)
#    - Publish directory: frontend
#    - Functions directory: netlify/functions
# 3. Add environment variable:
#    - Key: ANTHROPIC_API_KEY
#    - Value: your-api-key
# 4. Deploy!
```

### Option 2: Vercel
```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy
vercel

# 3. Set environment variable
vercel env add ANTHROPIC_API_KEY
```

### Option 3: Railway (Full Backend)
```bash
# 1. Connect GitHub repo to Railway
# 2. Set environment variable in Railway dashboard
# 3. Deploy backend/server.py
# 4. Update frontend API URL
```

## 💰 Cost Management

### Claude 3.5 Haiku Pricing
- **Input**: $0.80 per million tokens
- **Output**: $4.00 per million tokens
- **Typical game response**: ~100-200 tokens ($0.0008 - $0.0016 per response)

### Cost Estimation
```
100 players × 10 messages each × 200 tokens = 200,000 tokens
Cost: ~$0.80 for input + $0.80 for output = $1.60 total
```

### Rate Limiting (Built into the function)
```javascript
// The serverless function automatically handles:
// - CORS headers
// - Error handling with fallbacks
// - Proper request validation
```

## 🧪 Testing

### Test with Mock Responses
```bash
# Local testing without API key
python backend/server.py --mock
```

### Test with Real API
```bash
# Set your API key and test
export ANTHROPIC_API_KEY="your-key"
# Visit your deployed site and try chatting!
```

## 🔧 Troubleshooting

### Common Issues

#### "API key not found"
- Check environment variable is set correctly
- Restart your deployment after setting the key
- Verify the key starts with `sk-ant-api`

#### "CORS errors"
- Netlify function handles CORS automatically
- For other deployments, ensure CORS headers are set

#### "Function not found"
- Check `netlify.toml` configuration
- Verify function is in `netlify/functions/` directory
- Ensure function exports `handler`

### Fallback Behavior
The game automatically falls back to mock responses if:
- API key is missing
- API is down
- Rate limits exceeded
- Network errors

## 🎯 Current Status

- ✅ **Frontend**: Updated to use serverless endpoint
- ✅ **Serverless Function**: Created with Claude 3.5 Haiku
- ✅ **Fallback System**: Comprehensive mock responses
- ✅ **Security**: Environment variable based API key
- 🚧 **Deployment**: Ready for Netlify (requires API key setup)

## 🚀 Next Steps

1. **Choose deployment platform** (Netlify recommended)
2. **Set up API key** in environment variables
3. **Deploy and test** live AI integration
4. **Monitor usage** and costs
5. **Scale up** when ready!

---

**Ready to bring your dungeon master to life with Claude 3.5 Haiku!** 🎲