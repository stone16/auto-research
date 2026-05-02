# Repo: Pi

## README.md
```markdown
This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

```

## CLAUDE.md
```markdown
@AGENTS.md

```

## AGENTS.md
```markdown
<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

# Writing — 惜字如金

Every word must earn its place.

- No filler taglines, no marketing fluff, no sentences that restate the section title.
- Skip "uses these everywhere it works"-style copy. Cut the half of a sentence that adds nothing.
- A subtitle that doesn't tell the user *what to do* or *what just happened* doesn't ship.
- Only express the core product value. If you can't, say nothing.

Applies to UI copy, comments, commit messages, and chat replies alike.

# Setup / settings page

This is a foundation page, not a feed.

- Focus: connections + the firm's core info. No activity items, no "first N articles published"-style milestones, no shipped-work history. Activity belongs on the agent pages.
- Pi-managed vs user-editable must be visible at a glance. Pi-managed = set during onboarding, locked in the dashboard, "message your partner to change". User-editable = anything the user should be able to update without us.
- User data fields default to **read-only**. An explicit `Edit` button unlocks them; `Save` commits, `Cancel` reverts. Never leave editable inputs always-hot — it invites accidental edits.

# Always read CLAUDE.md first

Every task: read `CLAUDE.md` and any files it imports (e.g. this `AGENTS.md`) before writing or editing code. The harness auto-loads them, but read them anyway — the principles override defaults.

```

## agents.md
```markdown
<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

# Writing — 惜字如金

Every word must earn its place.

- No filler taglines, no marketing fluff, no sentences that restate the section title.
- Skip "uses these everywhere it works"-style copy. Cut the half of a sentence that adds nothing.
- A subtitle that doesn't tell the user *what to do* or *what just happened* doesn't ship.
- Only express the core product value. If you can't, say nothing.

Applies to UI copy, comments, commit messages, and chat replies alike.

# Setup / settings page

This is a foundation page, not a feed.

- Focus: connections + the firm's core info. No activity items, no "first N articles published"-style milestones, no shipped-work history. Activity belongs on the agent pages.
- Pi-managed vs user-editable must be visible at a glance. Pi-managed = set during onboarding, locked in the dashboard, "message your partner to change". User-editable = anything the user should be able to update without us.
- User data fields default to **read-only**. An explicit `Edit` button unlocks them; `Save` commits, `Cancel` reverts. Never leave editable inputs always-hot — it invites accidental edits.

# Always read CLAUDE.md first

Every task: read `CLAUDE.md` and any files it imports (e.g. this `AGENTS.md`) before writing or editing code. The harness auto-loads them, but read them anyway — the principles override defaults.

```
