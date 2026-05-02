# Repo: getuai-ai

## README.md
```markdown
# GetU.ai AI Agent Service

This repository contains the AI Agent service for the GetU.ai platform. It's built with FastAPI and LangChain, providing intelligent chat capabilities with session management and streaming responses.

## Architecture

The GetU.ai platform follows a three-tier architecture where this AI service acts as an intermediary between the frontend and API layer:

```
Frontend (getuai-ui) → AI Agent (getuai-ai) → API Layer (getuai-api)
```

### Directory Structure
```
app/
├── api/
│   └── v1/
│       ├── __init__.py    # API routes configuration
│       └── chat.py        # Chat endpoints implementation
├── core/
│   ├── config.py         # Application configuration
│   └── session.py        # Session management
├── services/
│   ├── agent.py          # AI agent implementation
│   └── tools/            # AI tools
│       ├── __init__.py   # Tools initialization
│       └── base.py       # Base tool implementation
└── main.py              # FastAPI application entry point
```

### Key Responsibilities
- Processes chat messages using LangChain and LLM
- Manages chat memory and context per session
- Validates sessions with the API layer
- Provides streaming responses for chat messages
- Handles greeting and message processing endpoints

## Features

### Session Management
- Session validation through API layer
- Session-specific chat memory
- Automatic session creation on validation failure
- Cross-layer session coordination

### Chat Functionality
- Streaming message responses
- Context-aware conversations
- Greeting messages for new sessions
- Error handling and recovery
- Message formatting and chunking

### LLM Integration
- Uses DeepSeek as primary LLM
- LangChain for agent and memory management
- Supports both streaming and non-streaming responses
- Handles "Final Answer" responses directly

## API Endpoints

### Chat Endpoints

#### Get Greeting
```http
GET /api/v1/chat/greeting
Headers: X-Session-Id: uuid-v4
Response: {
    "message": "Hello! How can I assist you today?",
    "metadata": {
        "session_id": "uuid-v4"
    }
}
```

#### Stream Message
```http
POST /api/v1/chat/message/stream
Headers: X-Session-Id: uuid-v4
Body: {
    "content": "Your message here",
    "metadata": {
        "key": "value"  # Optional
    }
}
Response: Server-Sent Events stream
```

#### Process Message
```http
POST /api/v1/chat/message
Headers: X-Session-Id: uuid-v4
Body: {
    "content": "Your message here",
    "metadata": {
        "key": "value"  # Optional
    }
}
Response: {
    "message": "AI response here",
    "actions": [],  # Optional actions for client
    "metadata": {
        "session_id": "uuid-v4"
    }
}
```

#### Reset Chat
```http
POST /api/v1/chat/reset
Headers: X-Session-Id: uuid-v4
Response: {
    "status": "success",
    "session_id": "uuid-v4"
}
```

## Components

### Service Layer (`services/`)

#### AIAgent (`agent.py`)
- Core business logic implementation
- Manages AI model initialization and configuration
- Handles chat memory and session data
- Processes messages and generates responses
- Integrates with LangChain and tools

#### Tools (`tools/`)
- Base tool implementation for AI capabilities
- Extensible framework for adding new tools
- API integration capabilities through BaseAPITool

### API Layer (`api/v1/`)

#### Chat Implementation (`chat.py`)
- HTTP endpoint definitions
- Request/response handling
- Session validation and error handling
- Streaming response support
- Complete error handling and logging

### Core Layer (`core/`)

#### Configuration (`config.py`)
- Environment variable management
- Application settings
- LLM configuration

#### Session Management (`session.py`)
- Session validation and creation
- Session data management
- Cross-service session coordination

## Configuration

Required environment variables:
```bash
# Server Configuration
PORT=8001
API_V1_STR=/api/v1
BACKEND_URL=http://localhost:8000

# LLM Configuration
DEEPSEEK_API_KEY=your-api-key
DEEPSEEK_API_BASE=your-api-base
DEEPSEEK_MODEL=your-model-name
TEMPERATURE=0.7
MAX_TOKENS=1000

# Session Configuration
SESSION_RETENTION_MINUTES=30
```

## Development

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run development server:
```bash
uvicorn app.main:app --reload --port 8001
```

## API Documentation

Full API documentation is available at:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Chat History Viewing

The application includes a utility script for viewing saved chat histories. This is useful for debugging, support, and analysis purposes.

### Configuration

Chat history saving can be configured using the following environment variables:
```bash
# Chat History Configuration
SAVE_CHAT_HISTORY=true
CHAT_HISTORY_DIR=/path/to/chat_histories
MAX_HISTORIES_PER_USER=100
HISTORY_RETENTION_DAYS=30
```

### Usage

The `view_chat_history.py` script in the `scripts` directory provides several options for viewing chat histories:

```bash
# List all users with chat histories
python scripts/view_chat_history.py --list-users

# List all chat histories for a specific user
python scripts/view_chat_history.py --user-id USER_ID

# View a specific chat session
python scripts/view_chat_history.py --user-id USER_ID --session-id SESSION_ID

# List recent chat histories
python scripts/view_chat_history.py --user-id USER_ID --days 7

# Export chat history as JSON
python scripts/view_chat_history.py --user-id USER_ID --session-id SESSION_ID --output json
```

The script provides an interactive mode when listing sessions, allowing you to select and view specific conversations.

### Directory Structure

Chat histories are saved in the following structure:
```
/chat_histories/
  /{user_id_1}/
    /20240228_123045_session-uuid-1234.json
    /20240228_124512_session-uuid-5678.json
  /{user_id_2}/
    /20240228_130012_session-uuid-abcd.json
```

# change log 20250107
## file
change email_generation.py to email_generation_bobtest.py (change tools/__init__.py as well)




```
