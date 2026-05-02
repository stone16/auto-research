# Repo: getuai-api

## README.md
```markdown
# GetU.ai API Layer

This repository contains the REST API layer for GetU.ai platform. It's built with FastAPI and serves as the central data management and session coordination layer for the entire platform.

## Architecture

The GetU.ai platform follows a three-tier architecture where this API service plays a central role:

```
Frontend (getuai-ui) → AI Agent (getuai-ai) → API Layer (getuai-api) → External Services
```

Additionally, the Frontend communicates directly with the API layer for form submissions and storage operations:

```
Frontend (getuai-ui) → API Layer (getuai-api)
```

### Key Responsibilities
- Acts as the source of truth for session management across all layers
- Provides temporary storage for session-based data (images, texts)
- Manages form submissions and data persistence
- Validates sessions for both frontend and AI layer requests
- Handles cleanup of expired sessions and associated data

## Features

- Session Management
  - Creation and validation of UUID v4 session IDs
  - Session expiration handling
  - Cross-layer session coordination
  - Automatic cleanup of expired sessions

- Storage Systems
  - Temporary image storage with session isolation
  - Text storage for form submissions
  - Automatic cleanup of old files
  - Support for various image formats

- Form Processing
  - Company information submission
  - Image upload handling
  - Data validation and sanitization

- REST API Endpoints
  - Session management endpoints
  - Storage operations (images, texts)
  - Form submission endpoints
  - Health check and monitoring

## Session Management

The API implements a comprehensive session management system:

### Session Endpoints

#### Create Session
```http
POST /api/v1/session
Response: {
    "session_id": "uuid-v4"
}
```

#### Validate Session
```http
GET /api/v1/session/validate
Headers: X-Session-Id: uuid-v4
Response: {
    "session_id": "uuid-v4"
}
```

#### Clear Session
```http
DELETE /api/v1/session
Headers: X-Session-Id: uuid-v4
```

### Session Flow
1. Session Creation:
   - Frontend or AI layer requests new session
   - API generates UUID v4 session ID
   - Session ID returned in response

2. Session Validation:
   - All requests must include  header
   - API validates session existence and expiration
   - Returns 404 if session expired/not found

3. Session Cleanup:
   - Automatic cleanup of expired sessions
   - Removal of associated storage data
   - Configurable retention period

## Storage System

### Image Storage

#### Upload Image
```http
POST /api/v1/images/upload
Headers: 
  X-Session-Id: uuid-v4
Form Data:
  file: image_file
  name: image_name
  form_name: string (optional, defaults to "default")
Response: {
    "filename": "stored_image_name.ext"
}
```

#### List Session Images
```http
GET /api/v1/images
Headers: X-Session-Id: uuid-v4
Query Parameters:
  form_name: string (optional)
Response: {
    "images": [
        "image1.jpg",
        "image2.png"
    ]
}
```

#### Get Image
```http
GET /api/v1/images/{filename}
Headers: X-Session-Id: uuid-v4
Response: Image file
```

#### Delete Image
```http
DELETE /api/v1/images/{filename}
Headers: X-Session-Id: uuid-v4
```

#### Cleanup Form Images
```http
DELETE /api/v1/images
Headers: X-Session-Id: uuid-v4
Query Parameters:
  form_name: string (required)
```

### Text Storage

#### Save Company Info
```http
POST /api/v1/texts/save/companyInfo
Headers: 
  X-Session-Id: uuid-v4
Body: {
    "company_name": string,
    "company_description": string,
    "company_logo": string,
    "product_images": [
        {
            "title": string,
            "description": string,
            "filename": string
        }
    ],
    "promotional_images": [
        {
            "title": string,
            "description": string,
            "filename": string
        }
    ]
}
Response: {
    "status": "success"
}
```

#### List Session Texts
```http
GET /api/v1/texts
Headers: X-Session-Id: uuid-v4
Response: {
    "texts": [
        {
            "id": string,
            "content": string,
            "created_at": string
        }
    ]
}
```

#### Delete Session Texts
```http
DELETE /api/v1/texts
Headers: X-Session-Id: uuid-v4
```

All endpoints return appropriate HTTP status codes:
- 200: Success
- 400: Bad Request (invalid parameters)
- 401: Unauthorized (missing session ID)
- 404: Not Found (resource doesn't exist)
- 413: Payload Too Large (file size exceeds limit)
- 500: Internal Server Error

## Configuration

Required environment variables:
```bash
# Server Configuration
PORT=8000
API_V1_STR=/api/v1

# Storage Configuration
TEMP_IMAGE_STORAGE_DIR=storage
MAX_IMAGE_SIZE_MB=5
IMAGE_RETENTION_MINUTES=60

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
uvicorn app.main:app --reload --port 8000 --workers 2
```

## API Documentation

Full API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
```
