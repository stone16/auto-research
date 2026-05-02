# Repo: getuai-ui

## README.md
```markdown
# GetU.ai Frontend

This repository contains the frontend application for the GetU.ai platform. It's built with React and TypeScript, providing a modern interface for AI interactions and company information management.

## Architecture

The GetU.ai platform follows a three-tier architecture:

```
Frontend (getuai-ui) → AI Agent (getuai-ai) → API Layer (getuai-api)
```

Additionally, the frontend communicates directly with the API layer for form submissions and storage operations:

```
Frontend (getuai-ui) → API Layer (getuai-api)
```

### Key Responsibilities
- Provides user interface for AI chat interactions
- Manages company information forms and submissions
- Handles session management across services
- Coordinates image uploads and storage
- Manages streaming responses from AI service

## Features

### Session Management
- Automatic session initialization
- Session validation and retry mechanisms
- Session expiration handling
- Cross-layer session coordination

### Chat Interface
- Real-time message streaming
- Message history display
- Error handling and recovery
- Automatic reconnection
- Session persistence

### Company Profile Management
- Company information form
- Image upload handling
  - Company logo
  - Product images
  - Promotional images
- Form validation
- Progress tracking

### UI Components
- Material-UI based design
- Responsive layouts
- Loading states
- Error messages
- Form validation feedback

## Project Structure

```
src/
├── components/        # Reusable UI components
├── hooks/            # Custom React hooks
├── pages/            # Page components
├── services/         # API and service integrations
├── styles/           # Global styles and themes
└── utils/            # Helper functions
```

## Tech Stack

- React 18
- TypeScript
- Material-UI
- Axios
- React Router
- ESLint + Prettier

## Prerequisites

- Node.js 16+
- npm or yarn
- Running instances of:
  - getuai-api (port 8000)
  - getuai-ai (port 8001)

## Installation

1. Install dependencies:
```bash
npm install
# or
yarn install
```

2. Create `.env` file:
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_AI_URL=http://localhost:8001
```

3. Start development server:
```bash
npm start
# or
yarn start
```

## Available Scripts

- `npm start`: Start development server
- `npm build`: Build production version
- `npm test`: Run tests
- `npm lint`: Run linter
- `npm format`: Format code

## Application Routes

### /chat
Chat interface for AI interactions:
- Initializes session if none exists
- Connects to AI service for message streaming
- Displays message history
- Handles errors and reconnection

### /company-info
Company information form:
- Collects company details
- Handles image uploads
- Validates form data
- Submits to API layer
- Redirects to chat on success

## Session Management

The session service (`src/services/session.ts`) handles:
- Session initialization
- Session ID storage
- Adding session headers to requests
- Session validation and retry logic
- Session expiration handling

### Session Flow

1. Initial Access:
   - Session service checks for existing session
   - If none exists, requests new session from API
   - Stores session ID for future requests

2. API Requests:
   - Session ID added to request headers
   - Automatic retry on session expiration
   - New session creation if needed

3. AI Service Requests:
   - Same session ID used for AI requests
   - Handles session validation failures
   - Maintains session consistency

## API Integration

### API Service (`src/services/api.ts`)
- Base URL: http://localhost:8000
- Handles form submissions
- Manages image uploads
- Stores company information

### AI Service (`src/services/ai.ts`)
- Base URL: http://localhost:8001
- Manages chat messages
- Handles streaming responses
- Maintains chat context

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create pull request

## License

MIT License - see LICENSE file for details

```
