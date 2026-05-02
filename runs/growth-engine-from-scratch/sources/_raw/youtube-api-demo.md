# Repo: youtube-api-demo

## README.md
```markdown
# YouTube API Demo

A simple web application that demonstrates how to use the YouTube Data API v3 to search for videos based on keywords.

## Features

- Search for YouTube videos using keywords
- Adjust the number of search results (5, 10, 25, or 50)
- View video thumbnails, titles, channel names, and descriptions
- Click to watch videos on YouTube

## Technologies Used

- Node.js and Express for the backend
- Vanilla JavaScript, HTML, and CSS for the frontend
- YouTube Data API v3 for fetching video data

## Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```
   npm install
   ```
3. Create a `.env` file in the root directory with your YouTube API key:
   ```
   YOUTUBE_API_KEY=your_api_key_here
   PORT=3000
   ```
4. Start the server:
   ```
   node src/server.js
   ```
5. Open your browser and navigate to `http://localhost:3000`

## How to Get a YouTube API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the YouTube Data API v3
4. Create credentials (API Key)
5. Copy the API key and add it to your `.env` file

## API Endpoint

The application exposes the following API endpoint:

- `GET /api/search?query=SEARCH_TERM&maxResults=NUMBER_OF_RESULTS`
  - `query`: The search term (required)
  - `maxResults`: The number of results to return (optional, default: 10, max: 50)

## License

This project is licensed under the MIT License. 
```
