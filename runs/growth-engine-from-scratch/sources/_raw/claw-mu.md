# Repo: claw-mu

## CLAUDE.md
```markdown
## Workflow Orchestration

### 1. Plan Node Default

- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately - don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy

- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One tack per subagent for focused execution

### 3. Self-Improvement Loop

- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done

- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)

- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing

- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests - then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

## Task Management

1. **Plan First**: Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.

## Build Commands

### Frontend/Backend (Turbo Monorepo)

```bash
pnpm install          # Install dependencies
pnpm build            # Build all apps (api, admin, chat)
pnpm dev              # Development mode
```

### Worker Docker Image (4-Layer Architecture)

| Layer | Image | Content | Rebuild When |
|-------|-------|---------|--------------|
| base | `claw-base-latest` | Ubuntu + Node 22 + Bun | Toolchain update |
| deps | `claw-deps-latest` | openclaw node_modules (1.9GB) | Dependencies change |
| openclaw | `claw-openclaw-latest` | dist/ + assets (~50MB) | Code change |
| worker | `claw-worker-latest` | worker-api | API change |

**Quick Commands:**

```bash
# Most common: openclaw code changed
./docker/build-worker.sh code

# worker-api only
./docker/build-worker.sh api

# Dependencies changed (package.json)
./docker/build-worker.sh deps

# Full rebuild
./docker/build-worker.sh base
```

**Manual Build (openclaw code change):**

```bash
cd openclaw && pnpm build
docker build -f docker/Dockerfile.openclaw -t getuai/getu_ads:claw-openclaw-latest .
docker build -f docker/Dockerfile.worker -t getuai/getu_ads:claw-worker-latest .
```

### OpenClaw CLI

```bash
cd openclaw
pnpm install          # Install dependencies
pnpm build            # Build (generates dist/)
pnpm dev              # Development mode
```

### Chrome Extension

```bash
# Development: Load unpacked from apps/chat/public/extension/claw-extension/
# Chrome: chrome://extensions -> Load unpacked

# Production zip:
cd apps/chat/public/extension/claw-extension
zip -r ../claw-extension.zip .
```

### Staging Deployment

```bash
# On staging server (20.228.94.67)
cd ~/projects/claw-mu
docker compose up -d --build    # Rebuild and start
docker compose logs -f          # View logs
docker compose restart          # Restart all
```

```
