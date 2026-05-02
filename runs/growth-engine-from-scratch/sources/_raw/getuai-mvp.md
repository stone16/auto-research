# Repo: getuai-mvp

## README.md
```markdown
# GetUAI MVP

## Environment Setup

This project has been configured to support both local development and production environments, particularly regarding API routing.

### API Configuration

The application uses a configurable API prefix system:

- **Local Development**: Uses direct API paths (e.g., `/chat/session`)
- **Production**: Uses prefixed API paths (e.g., `/api/chat/session`)

### Frontend Configuration

The frontend automatically detects the environment and sets the appropriate API base URL:

```typescript
// In v2-ui/app/chat/components/Chat.tsx
const apiBaseUrl = process.env.NODE_ENV === 'development' ? '' : '/api';
```

This ensures that API requests are routed correctly in both development and production environments.

### Backend Configuration

The backend FastAPI application uses the `API_PREFIX` environment variable to determine the route prefix:

```python
# In v2-ai/api/config.py
API_PREFIX = os.getenv("API_PREFIX", "")  # Empty string for local development, "/api" for production
```

All route decorators use this prefix:

```python
@app.post(f"{API_PREFIX}/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    # ...
```

### Environment Configuration

#### Local Development

For local development, no additional configuration is needed. The default empty prefix will be used.

#### Production Deployment

For production deployment, set the `API_PREFIX` environment variable to `/api`:

```sh
# In your .env file or environment variables
API_PREFIX=/api
```

### Proxy Configuration (Production)

In production, configure your web server (Nginx, etc.) to route requests to the appropriate backend:

```nginx
# Example Nginx configuration
location /api/ {
    proxy_pass http://backend:8000/;  # Note the trailing slash
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

location / {
    proxy_pass http://frontend:3000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## Development Setup

1. Clone the repository
2. Set up the backend:
   ```sh
   cd v2-ai
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Set up the frontend:
   ```sh
   cd v2-ui
   npm install
   ```
4. Start the development servers:
   ```sh
   # Backend
   cd v2-ai
   python main.py

   # Frontend
   cd v2-ui
   npm run dev
   ```

## Troubleshooting

### API Routing Issues

If you're experiencing API routing issues:

1. Check the environment setting - `process.env.NODE_ENV` should be `development` for local development
2. Verify your `API_PREFIX` environment variable is correctly set
3. For production, ensure your proxy server is properly configured to route `/api/*` requests to the backend

### Session Storage

Session IDs are stored in localStorage. If you experience session issues, try clearing localStorage in your browser. 
```
