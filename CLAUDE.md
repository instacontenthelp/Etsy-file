# CLAUDE.md

This file documents the project structure, conventions, and development workflows for AI assistants working in this repository.

## Project Overview

**Repository:** `instacontenthelp/Etsy-file`
**Owner:** The Planners Collective

This project manages Etsy product files and listings for The Planners Collective's Etsy shop. The repository serves as the source of truth for digital product assets, listing data, and any automation tooling around Etsy file management.

## Repository Structure

```
Etsy-file/
├── CLAUDE.md          # This file — AI assistant guidance
├── README.md          # Human-facing project documentation
└── (project files)    # To be established as the project grows
```

This is a new repository. Update this structure section as directories and files are added.

## Development Workflow

### Branch Strategy

- `main` — stable, production-ready state
- `claude/...` — branches created for AI-assisted tasks (e.g. `claude/claude-md-docs-49C2v`)
- Feature branches should follow the pattern: `feature/<short-description>`
- Fix branches: `fix/<short-description>`

### Making Changes

1. Always work on a feature branch, never commit directly to `main`
2. Write clear, descriptive commit messages (imperative mood: "Add listing parser" not "Added listing parser")
3. Push with `git push -u origin <branch-name>`
4. Open a pull request to merge into `main`

### Git Commit Conventions

```
<type>: <short summary>

<optional body explaining WHY, not WHAT>
```

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`

Examples:
- `feat: add CSV export for Etsy listings`
- `fix: handle missing image URLs in product parser`
- `docs: update README with setup instructions`

## Key Conventions for AI Assistants

### General Rules

- Do not commit directly to `main`
- Do not push unless explicitly asked
- Do not create pull requests unless the user explicitly requests one
- Prefer editing existing files over creating new ones
- Do not add speculative features — implement only what is asked
- Do not add comments explaining what code does; only add them when the WHY is non-obvious

### File Operations

- Always read a file before editing it
- When deleting files, confirm with the user first
- Do not create `*.md` documentation files unless explicitly requested (this file is an exception — it was requested)

### Code Style

To be defined as the project tech stack is established. Update this section when languages and frameworks are chosen.

### Environment Variables

Document any required environment variables here as they are introduced. Example format:

```
ETSY_API_KEY=        # Etsy API v3 key
ETSY_SHOP_ID=        # Numeric Etsy shop ID
```

Do not commit `.env` files or files containing real credentials.

## Testing

To be defined. Update this section when a testing framework is set up.

## CI/CD

To be defined. Update this section when GitHub Actions or other CI is configured.

## Updating This File

Keep this file current as the project evolves:
- When new directories are added, update the structure section
- When new environment variables are required, document them
- When a testing or build workflow is established, add it here
- When code style linters or formatters are added, document the commands
