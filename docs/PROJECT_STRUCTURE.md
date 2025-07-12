# Vibe Game - Project Structure

## Directory Organization

```
vibegame/
├── frontend/                   # Client-side code
│   ├── index.html             # Main game interface
│   ├── style.css              # Game styling
│   └── script.js              # Game logic and API calls
│
├── backend/                   # Server-side code
│   ├── server.py              # Main Python server with LiteLLM
│   ├── requirements.txt       # Python dependencies
│   └── api/                   # API handlers (for serverless)
│       └── chat.js            # Serverless function for chat
│
├── tests/                     # Test files
│   ├── frontend/              # Frontend tests
│   ├── backend/               # Backend tests
│   └── e2e/                   # End-to-end tests
│
├── config/                    # Configuration files
│   ├── package.json           # Node.js configuration
│   └── .env.example           # Environment variables template
│
├── docs/                      # Documentation
│   ├── PROJECT_STRUCTURE.md   # This file
│   └── API.md                 # API documentation
│
├── notes/                     # Development notes
│   ├── testing_ideas.md       # Testing strategy
│   ├── mobile_deployment_ideas.md
│   ├── CLAUDE.md              # Development notes
│   └── venv/                  # Python virtual environment
│
├── .github/                   # GitHub configuration
│   └── workflows/             # CI/CD workflows
│       └── deploy.yml         # Deployment workflow
│
└── README.md                  # Project overview
```

## Development Setup

### Local Development
```bash
# Backend (Python)
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python server.py --mock  # Run with mock responses

# Frontend (Static)
cd frontend
python -m http.server 8080  # Or use the backend server
```

### Testing
```bash
# Run backend in mock mode for testing
python backend/server.py --mock --port 8000

# Frontend tests (when implemented)
npm test

# E2E tests (when implemented)
npm run test:e2e
```

## Deployment

### GitHub Pages (Frontend Only)
- Frontend files are deployed automatically via GitHub Actions
- Backend API calls use serverless functions

### Full Stack (Backend + Frontend)
- Deploy backend to services like Railway, Render, or Heroku
- Frontend can still use GitHub Pages with backend API URLs

## File Purposes

### Frontend
- `index.html`: Main game interface with chat UI
- `style.css`: Mobile-first responsive styling
- `script.js`: Game logic, chat handling, API integration

### Backend
- `server.py`: Full Python server with LiteLLM integration and mocking
- `api/chat.js`: Serverless function alternative for static deployments
- `requirements.txt`: Python dependencies

### Configuration
- `package.json`: Node.js scripts and metadata
- `.env`: Environment variables (API keys, etc.)

### Tests
- `tests/frontend/`: Unit tests for JavaScript
- `tests/backend/`: Unit tests for Python server
- `tests/e2e/`: End-to-end browser tests

## Key Features

1. **Mock Mode**: Backend can run with mock LLM responses for testing
2. **Dual Deployment**: Supports both static (GitHub Pages) and full-stack deployment
3. **Mobile-First**: Responsive design optimized for mobile devices
4. **Testing-Ready**: Structure supports comprehensive testing strategy
5. **LiteLLM Integration**: Easy switching between different LLM providers