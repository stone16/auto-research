# Repo: openinterx-api-demo

## README.md
```markdown
# OpenInterX API Demo

This is a demo application that demonstrates how to interact with the OpenInterX API endpoints. The application provides a user interface for uploading videos and chatting with the OpenInterX AI agent about the uploaded videos.

## Features

- Authentication with OpenInterX API
- Video upload functionality
- Video chat with AI agent
- Token refresh mechanism

## Tech Stack

- React with TypeScript
- Material-UI (MUI) for UI components
- Vite as the build tool
- Axios for API requests

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd openinterx-demo
```

2. Install dependencies
```bash
npm install
```

3. Start the development server
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:5173`

## Usage

### Authentication

To use the OpenInterX API, you need to authenticate with your credentials:

1. Obtain a Client ID and Authorization Code from OpenInterX
2. Enter these credentials in the login form
3. Once authenticated, you can access the video upload and chat features

### Uploading Videos

1. Navigate to the "Upload Video" tab
2. Enter a callback URL (this URL will receive status updates about your video)
3. Select a video file to upload
4. Click the "Upload Video" button
5. Once the upload is complete, you'll receive a video ID that you can use for chatting

### Chatting with Videos

1. Navigate to the "Video Chat" tab
2. Enter the video ID(s) of the videos you want to chat about
3. Type your message in the input field
4. Click the send button or press Enter
5. The AI will respond based on the content of the videos

## API Endpoints

The application interacts with the following OpenInterX API endpoints:

- `auth/api/token/getAccessToken`: Get an access token using a code and client ID
- `auth/api/token/refreshAccessToken`: Refresh an access token using a refresh token
- `/api/serve/video/upload`: Upload a video to the OpenInterX platform
- `/api/serve/video/chat`: Chat with the AI about uploaded videos

## License

This project is licensed under the MIT License - see the LICENSE file for details.

```
