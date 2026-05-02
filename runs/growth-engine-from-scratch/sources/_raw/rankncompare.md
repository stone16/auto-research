# Repo: rankncompare

## README.md
```markdown
# Rank&Compare

A web application for comparing and ranking products across different categories.

## Project Overview

Rank&Compare is a full-stack web application built with React and Express that allows users to compare products across different categories. The application features a clean, modern UI built with Tailwind CSS and Shadcn UI components.

## Tech Stack

### Frontend
- React
- TypeScript
- Tailwind CSS
- Shadcn UI components (Radix UI)
- Vite (for building and development)
- React Query (for data fetching)
- React Hook Form (for form handling)
- Wouter (for routing)

### Backend
- Node.js
- Express
- JSON data storage
- Zod (for validation)

### DevOps
- Nginx (for production deployment)
- Node.js scripts for build and deployment

## Project Structure

```
rankncompare/
├── client/               # Frontend code
│   ├── dist/             # Built client assets
│   ├── public/           # Static assets
│   ├── src/              # Source code
│       ├── components/   # UI components
│       ├── hooks/        # Custom React hooks
│       ├── lib/          # Utility functions
│       ├── pages/        # Page components
│       ├── App.tsx       # Main application component
│       └── main.tsx      # Entry point
├── data/                 # JSON data for the application
├── server/               # Backend code
│   ├── index.ts          # Main server file
│   ├── category-api.ts   # Category API handlers
│   ├── seo-api.ts        # SEO metadata API handlers
│   ├── seo-routes.ts     # Sitemap and robots.txt routes
│   ├── sitemap-generator.ts # Sitemap and robots.txt generator
│   └── storage.ts        # Data storage operations
├── server-dist/          # Built server code
├── shared/               # Shared code between client and server
│   └── types.ts          # TypeScript types
├── scripts/              # Build and utility scripts
│   ├── build-search-index.js # Search index builder
│   └── generate-seo-files.ts # SEO files generator
├── nginx.conf            # Nginx configuration for deployment
├── package.json          # Project dependencies and scripts
├── start.sh              # Startup script
├── tailwind.config.ts    # Tailwind CSS configuration
├── tsconfig.json         # TypeScript configuration
└── vite.config.ts        # Vite configuration
```

## Google Analytics Integration

The application is integrated with Google Analytics 4 (GA4) to track user interactions and gain insights into user behavior.

### Implementation Details

1. **GA4 Configuration**
   - The Google Analytics tracking ID (`G-RF6K20FCM8`) is configured in two places:
     - In `client/index.html` via the standard Google Analytics script
     - In `client/src/App.tsx` via the `AnalyticsProvider` component

2. **Analytics Architecture**
   - `client/src/lib/analytics.ts`: Core analytics utility functions
   - `client/src/lib/analytics-provider.tsx`: React context provider that initializes GA
   - `client/src/hooks/useAnalytics.ts`: Custom hook for tracking events throughout the application

3. **Tracked Events**
   The application tracks the following events:
   - Page views
   - Navigation events
   - Search queries and search result clicks
   - Category clicks
   - Product view events
   - UI interactions (mobile menu toggle, etc.)

4. **Testing Analytics Locally**
   When testing locally:
   - GA tracking code executes but data may not appear in your GA reports
   - GA typically filters out localhost traffic
   - Use Google Analytics Debugger extension or browser developer tools to verify tracking calls
   - Check Network tab for requests to `www.google-analytics.com`

5. **Customizing Analytics**
   To modify the tracking ID:
   - Update the `GA_MEASUREMENT_ID` constant in `client/src/App.tsx`
   - Update the measurement ID in the script tags in `client/index.html`

### Adding New Tracking Events

To add tracking for new user interactions:

1. Import the `useAnalytics` hook:
   ```tsx
   import { useAnalytics } from '@/hooks/useAnalytics';
   ```

2. Use the appropriate tracking method:
   ```tsx
   const { trackEvent, trackPageView } = useAnalytics();
   
   // Track a custom event
   trackEvent('my_custom_event', {
     event_category: 'User Engagement',
     event_label: 'Custom Interaction'
   });
   ```

## SEO Features

The application includes built-in SEO features to improve search engine indexability and visibility.

### Sitemap and Robots.txt

The site automatically generates and serves a `sitemap.xml` and `robots.txt` file to help search engines discover and index all pages.

1. **Implementation Details**
   - Dynamic sitemap generation based on available categories
   - Static routes (home, about, contact, trending) included in sitemap
   - Category pages prioritized (0.9 priority) for better indexing
   - Standard robots.txt with reference to sitemap location

2. **File Generation**
   - Files are automatically generated during the build process
   - Generated files are stored in `client/dist` directory
   - Server routes provide access at `/sitemap.xml` and `/robots.txt`
   - The generation script is located at `scripts/generate-seo-files.ts`

3. **Build Integration**
   - The `npm run build` command includes sitemap and robots.txt generation
   - Individual generation via `npm run build:seo-files`

4. **Customization**
   - Modify site URL in `server/sitemap-generator.ts`
   - Adjust priority and change frequency in the same file
   - Add additional static routes to the `STATIC_ROUTES` array

This implementation ensures search engines can discover all pages of the application, including dynamically generated category pages, which helps improve visibility in search results.

## SEO Improvements

The following SEO improvements have been implemented to enhance search engine visibility and user experience:

1. **Improved Meta Tags**
   - Standardized meta titles and descriptions with optimal length (under 60/160 characters)
   - Consistent meta tag formatting across all pages
   - Enhanced keyword coverage while maintaining readability

2. **Technical SEO**
   - Fixed viewport meta tag for better accessibility
   - Standardized canonical URLs to prevent duplicate content issues
   - Improved robots meta tag format

3. **Structured Data**
   - Added breadcrumb schema markup for improved navigation in search results
   - Implemented FAQ schema markup for each category
   - Enhanced product schema with detailed rating information

4. **On-Page Elements**
   - Added visible breadcrumb navigation for improved user experience
   - Added dynamically generated FAQs for each category
   - Consistently formatted title tags for better branding

5. **Site Structure**
   - Improved internal linking between categories
   - Enhanced sitemap.xml and robots.txt generation

These improvements follow SEO best practices to increase visibility in search results while providing a better user experience.

## Prerequisites

- Node.js 16+ (LTS recommended)
- npm or yarn

## Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/rankncompare.git
   cd rankncompare
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory with the following variables:
   ```
   NODE_ENV=development
   SESSION_SECRET=your_session_secret
   ```

4. **Build the search index**
   ```bash
   npm run build:search-index
   ```
   This step is necessary if you're using the search functionality.

5. **Start the development server**
   ```bash
   npm run dev
   ```
   This will start both the client and server in development mode.

   Alternatively, you can run client and server separately:
   ```bash
   npm run client-dev  # Start client (vite dev server)
   npm run api-dev     # Start API server
   ```

6. **Open the application**
   The application will be available at http://localhost:3000

## Building for Production

1. **Build the search index (if using search functionality)**
   ```bash
   npm run build:search-index
   ```

2. **Build the client and server**
   ```bash
   npm run build
   ```
   This will:
   - Build the search index
   - Build the client assets to `client/dist`
   - Generate sitemap.xml and robots.txt
   - Bundle the server code to `server-dist`

3. **Generate SEO files separately (if needed)**
   ```bash
   npm run build:seo-files
   ```
   This will generate sitemap.xml and robots.txt based on the current data.

4. **Start the production server**
   ```bash
   npm run start
   ```
   This will run the application in production mode.

## Deployment to a Remote Server with Nginx

### Prerequisites
- A server with Ubuntu/Debian
- Node.js 16+ installed
- Nginx installed
- Domain name pointed to your server

### Setup Steps

1. **Clone the repository on your server**
   ```bash
   git clone https://github.com/yourusername/rankncompare.git
   cd rankncompare
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env` file with production settings:
   ```
   NODE_ENV=production
   SESSION_SECRET=your_production_secret
   ```

4. **Build the search index**
   ```bash
   npm run build:search-index
   ```
   This step is necessary for search functionality to work properly.

5. **Build the application**
   ```bash
   npm run build
   ```

6. **Configure Nginx**
   Copy the provided nginx.conf to your server:
   ```bash
   sudo cp nginx.conf /etc/nginx/sites-available/rankncompare
   ```

   Create a symbolic link:
   ```bash
   sudo ln -s /etc/nginx/sites-available/rankncompare /etc/nginx/sites-enabled/
   ```

   Edit the Nginx configuration to match your domain and file paths:
   ```bash
   sudo nano /etc/nginx/sites-available/rankncompare
   ```

   Test and restart Nginx:
   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

7. **Set up a process manager (PM2 recommended)**
   ```bash
   sudo npm install -g pm2
   pm2 start server-dist/index.js --name rankncompare
   pm2 save
   pm2 startup
   ```

8. **Enable SSL with Let's Encrypt (optional but recommended)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d rankncompare.com -d www.rankncompare.com
   ```

9. **Monitor the application**
   ```bash
   pm2 logs rankncompare
   ```

## Data Management

The application uses JSON files stored in the `data` directory to manage product and category information.

### Data Manager Script

The project includes a comprehensive data management script (`scripts/data_manager.py`) that helps maintain data consistency and manage content. This Python utility ensures that categories are properly ordered, products are correctly positioned, and trending data stays in sync.

#### Features

- **Data Validation**: Verify that categories are alphabetically ordered, products have valid category IDs and positions, and trending data matches source items
- **Data Fixing**: Automatically fix inconsistencies in category ordering, product positions, and trending data
- **Content Management**: Add new categories, products, and trending items through an interactive interface
- **Data Integrity**: Ensure products have proper ratings, positions, and IDs that align with their ranking within categories

#### Usage

```bash
# Verify data consistency
python scripts/data_manager.py --verify

# Fix data inconsistencies
python scripts/data_manager.py --fix

# Add a new category
python scripts/data_manager.py --add-category

# Add a new product
python scripts/data_manager.py --add-product

# Add a product or category to trending
python scripts/data_manager.py --add-trending

# Interactive mode (menu-driven interface)
python scripts/data_manager.py
```

The script maintains relationships between the three main JSON data files:
- `data/categories.json`: Categories with properties like name, slug, icon, and color
- `data/products.json`: Products with ratings, positions, features, pros, and cons
- `data/trending.json`: Trending products and categories with scores and metadata

When fixing data, the script ensures:
1. Categories are sorted alphabetically by name with sequential IDs
2. Product IDs align with their position within the dataset (sorted by category and rating)
3. References between files are properly updated when IDs change
4. Trending data stays synchronized with the source products and categories

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 

```
