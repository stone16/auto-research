# Repo: getuai-2.0

## README.md
```markdown
<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/drive/1r8qvoChH2STCNMPBQkBPOes_lWmE1ewi

## Project Structure

```
.
├── frontend/          # React + Vite frontend application
│   ├── components/    # React UI components
│   ├── services/      # API service layer (Gemini AI)
│   ├── App.tsx        # Main application component
│   ├── index.tsx      # React DOM entry point
│   ├── index.html     # HTML template
│   ├── types.ts       # TypeScript type definitions
│   ├── vite.config.ts # Vite build configuration
│   ├── tsconfig.json  # TypeScript configuration
│   └── package.json   # Dependencies and scripts
├── .gitignore
└── README.md
```

## Run Locally

**Prerequisites:** Node.js

1. Navigate to the frontend directory:
   `cd frontend`
2. Install dependencies:
   `npm install`
3. Set the `GEMINI_API_KEY` in [frontend/.env.local](frontend/.env.local) to your Gemini API key
4. Run the app:
   `npm run dev`

```
