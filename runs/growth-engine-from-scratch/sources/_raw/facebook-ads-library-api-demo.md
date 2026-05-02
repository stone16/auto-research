# Repo: facebook-ads-library-api-demo

## README.md
```markdown
# Facebook Ads Library API Demo Application

This application demonstrates how to use the Facebook Ads Library API to search for ads, view their details, and save them locally for further operations.

## Features

- Search for ads using keywords or phrases
- Filter ads by type, status, media type, and platform
- View detailed information about each ad
- Save ads to local storage for later viewing
- Filter and sort saved ads

## Tech Stack

### Frontend
- React with TypeScript
- Material-UI (MUI) for UI components
- Vite as the build tool
- Context API for state management
- LocalForage for local storage

### Backend
- Node.js with Express
- Axios for API requests

## Project Structure

```
facebook-ads-library-demo/
├── frontend/                  # Frontend React application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── detail/        # Ad detail components
│   │   │   ├── layout/        # Layout components
│   │   │   ├── results/       # Search results components
│   │   │   ├── saved/         # Saved ads components
│   │   │   └── search/        # Search form components
│   │   ├── context/           # React context providers
│   │   ├── hooks/             # Custom React hooks
│   │   ├── services/          # API and storage services
│   │   ├── types/             # TypeScript type definitions
│   │   └── utils/             # Utility functions
│   ├── public/                # Static assets
│   └── index.html             # HTML entry point
├── backend/                   # Backend Express server
│   └── server.js              # Server implementation
└── README.md                  # Project documentation
```

## Setup Instructions

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Facebook Developer Account with access to the Ads Library API

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```
PORT=5000
FB_ACCESS_TOKEN=your_facebook_access_token
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/facebook-ads-library-demo.git
cd facebook-ads-library-demo
```

2. Install backend dependencies:
```bash
cd backend
npm install
```

3. Install frontend dependencies:
```bash
cd ../frontend
npm install
```

### Running the Application

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Start the backend server:
```bash
cd ../backend
npm start
```

3. Open your browser and navigate to `http://localhost:5000`

## Facebook Ads Library API Authentication

To use the Facebook Ads Library API, you need to:

1. **Create a Facebook Developer Account**:
   - Go to [Facebook for Developers](https://developers.facebook.com/)
   - Sign up or log in with your Facebook account

2. **Create a Facebook App**:
   - Go to the [Apps Dashboard](https://developers.facebook.com/apps/)
   - Click "Create App"
   - Select "Business" as the app type
   - Fill in the required information and create the app

3. **Add the Marketing API Product**:
   - In your app dashboard, click "Add Product"
   - Select "Marketing API"

4. **Generate an Access Token**:
   - Go to the [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
   - Select your app from the dropdown
   - Select "Get Token" > "Get User Access Token"
   - Select the required permissions:
     - `ads_read`
     - `ads_management`
     - `business_management`
   - Click "Generate Access Token"

5. **Extend the Token Expiration**:
   - Go to the [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
   - Paste your token and click "Debug"
   - Click "Extend Access Token"

6. **Confirm Identity for Political Ads Access**:
   - To access political ads, you need to confirm your identity
   - Go to [Facebook.com/ID](https://www.facebook.com/id)
   - Follow the confirmation process
   - This can take a few days to complete

7. **Add the Access Token to Your Environment Variables**:
   - Add the token to your `.env` file as `FB_ACCESS_TOKEN`

## API Endpoints

### Search Ads
```
POST /api/search
```
Request body:
```json
{
  "search_terms": "example",
  "ad_type": "ALL",
  "ad_active_status": "ACTIVE",
  "ad_reached_countries": ["US"],
  "media_type": "ALL",
  "publisher_platforms": ["FACEBOOK", "INSTAGRAM"]
}
```

### Fetch Next Page
```
GET /api/next?url={next_page_url}
```

### Get Ad Details
```
GET /api/ad/{ad_id}
```

## Local Storage

The application uses IndexedDB (via LocalForage) to store saved ads. The storage is structured as follows:

- **Store Name**: `saved_ads`
- **Key**: Ad ID
- **Value**: Ad object with additional properties:
  - `saved`: Boolean indicating the ad is saved
  - `savedAt`: Timestamp when the ad was saved

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Facebook Ads Library API Documentation](https://www.facebook.com/ads/library/api/)
- [React Documentation](https://reactjs.org/)
- [Material-UI Documentation](https://mui.com/)
- [Vite Documentation](https://vitejs.dev/)

```
