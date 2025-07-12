# 🎲 Vibe Game - AI Dungeon Master

A modern browser-based dungeon master game powered by AI. Chat with an intelligent DM that creates immersive adventures on the fly!

## ✨ Features

- **Mobile-First Design**: Optimized for vibecoding on any device
- **AI-Powered Storytelling**: Dynamic responses using LiteLLM integration
- **Comprehensive Testing**: Full test suite for reliable development
- **Zero Setup**: Works in browser with fallback responses
- **Clean Architecture**: Organized structure for easy feature additions

## 🚀 Quick Start

### Play the Game
```bash
# Clone and run locally
git clone https://github.com/qemqemqem/vibegame.git
cd vibegame
python backend/server.py --mock
```
Then open http://localhost:8000

### Live Demo
🌐 **[Play Now](https://qemqemqem.github.io/vibegame/)** (GitHub Pages)

## 🏗️ Development

### Project Structure
```
vibegame/
├── frontend/          # Game interface (HTML/CSS/JS)
├── backend/           # Python server with LiteLLM
├── tests/             # Comprehensive test suite
├── config/            # Configuration files
└── docs/              # Documentation
```

### Local Development
```bash
# Backend with mock responses (great for testing)
python backend/server.py --mock

# Backend with real LLM (requires API keys)
python backend/server.py

# Frontend only (static files)
cd frontend && python -m http.server 8000

# Run all tests
python run_tests.py
```

### Available Scripts
```bash
# From config/ directory
npm run dev           # Start frontend server
npm run dev:backend   # Start backend in mock mode
npm run dev:full      # Start backend with real LLM
npm run test          # Run all tests
```

## 🧪 Testing

**"Track the bugs before they track you!"** - Our comprehensive testing strategy:

- **Backend Tests**: Unit tests for mock responses and server logic
- **Frontend Tests**: Browser-based testing suite
- **E2E Testing**: Complete user journey validation
- **CI/CD Pipeline**: Automated testing on every commit

```bash
# Run specific test suites
python run_tests.py                    # All tests
python -m pytest tests/backend/       # Backend only
open tests/frontend/test_game_logic.html  # Frontend tests
```

## 🎮 Game Features

### Current Gameplay
- **Chat Interface**: Type actions, get AI responses
- **Context Awareness**: DM remembers your journey
- **Mobile Optimized**: Perfect for vibecoding anywhere
- **Fallback Responses**: Works even without API access

### AI Integration
- **LiteLLM Support**: Easy switching between AI providers
- **Mock Mode**: Comprehensive fallback responses for testing
- **Contextual Responses**: Different responses for combat, exploration, social interactions

## 🚀 Deployment

### GitHub Pages (Auto-Deploy)
1. Push to main branch
2. GitHub Actions runs tests
3. Auto-deploys to https://qemqemqem.github.io/vibegame/

### Manual Deployment
```bash
# Deploy frontend anywhere
cp -r frontend/* /your/web/server/

# Full-stack deployment
# Deploy backend to Railway/Render/Heroku
# Update frontend API URLs
```

## 🛠️ Configuration

### Environment Variables
```bash
# For real LLM integration
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
```

### LiteLLM Setup
```python
# backend/server.py supports multiple providers
model = "gpt-3.5-turbo"      # OpenAI
model = "claude-3-sonnet"    # Anthropic  
model = "gemini-pro"         # Google
```

## 📋 Development Roadmap

### Planned Features
- [ ] Character creation and stats
- [ ] Inventory management
- [ ] Save/load game state
- [ ] Multiple story campaigns
- [ ] Combat system
- [ ] Multiplayer sessions

### Technical Improvements
- [ ] WebSocket real-time updates
- [ ] Voice input/output
- [ ] Image generation for scenes
- [ ] Performance optimization

## 🤝 Contributing

Ready to vibecode? Here's how to add features:

1. **Fork the repository**
2. **Write tests first** (we're test-driven!)
3. **Implement features** following existing patterns
4. **Run the test suite** to ensure quality
5. **Submit a pull request**

### Code Style
- **Clean code is happy code**
- **Test first, code second**
- **Mobile-first design**
- **Follow existing patterns**

## 📚 Documentation

- [Project Structure](docs/PROJECT_STRUCTURE.md) - Complete codebase overview
- [Testing Strategy](notes/testing_ideas.md) - Comprehensive testing approach
- [Deployment Progress](notes/progress/deployment.md) - Current deployment status

## 🎯 Tech Stack

- **Frontend**: Vanilla HTML/CSS/JavaScript (mobile-first)
- **Backend**: Python with HTTP server
- **AI Integration**: LiteLLM (multi-provider support)
- **Testing**: pytest + custom browser tests
- **Deployment**: GitHub Actions + GitHub Pages
- **Development**: Hot reload, comprehensive mocking

## 📄 License

MIT License - Feel free to use this for your own vibecoding adventures!

## 🎮 Credits

Built with **[Claude Code](https://claude.ai/code)** using XP programming methodology:
- *"Swift and decisive"* development
- *"Test first, code second"* approach  
- *"Clean code is happy code"* principles

---

**Ready to start your adventure? [Play Now](https://qemqemqem.github.io/vibegame/) or `git clone` and vibecode!** 🚀
