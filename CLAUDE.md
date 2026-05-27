# CLAUDE.md

This file documents the project structure, conventions, and development workflows for AI assistants working in this repository.

## Project Overview

**Repository:** `instacontenthelp/Etsy-file`
**Owner:** The Planners Collective
**Language:** Python 3

This is a full-featured Etsy shop management tool for The Planners Collective. It covers:

- **Listing management** — create, update, and bulk-edit Etsy product listings via the Etsy API v3
- **Digital file handling** — organize, rename, and upload digital product files (planners, printables, etc.)
- **Content automation** — generate and schedule Etsy listing content (titles, descriptions, tags)
- **Shop dashboard** — unified interface for monitoring and managing the Etsy shop

## Repository Structure

```
Etsy-file/
├── CLAUDE.md              # This file — AI assistant guidance
├── README.md              # Human-facing project documentation
├── requirements.txt       # Python dependencies (production)
├── requirements-dev.txt   # Python dependencies (dev/test)
├── .env.example           # Template for required environment variables
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions CI pipeline
├── src/                   # Main application source code
│   └── etsy_file/         # Top-level package
│       ├── __init__.py
│       ├── api/           # Etsy API v3 client and wrappers
│       ├── listings/      # Listing creation, update, bulk-edit logic
│       ├── files/         # Digital file handling and upload logic
│       ├── content/       # Content generation and automation
│       └── dashboard/     # Shop overview and reporting
└── tests/                 # pytest test suite (mirrors src/ structure)
    ├── conftest.py        # Shared fixtures
    ├── test_api/
    ├── test_listings/
    ├── test_files/
    └── test_content/
```

Update this structure as the project grows.

## Development Workflow

### Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
cp .env.example .env             # fill in real values
```

### Running the App

```bash
python -m etsy_file              # or whatever entry point is defined
```

### Running Tests

```bash
pytest                           # run all tests
pytest tests/test_listings/      # run a specific module
pytest -k "test_upload"          # run tests matching a name pattern
pytest --cov=src --cov-report=term-missing  # with coverage
```

### Branch Strategy

- `main` — stable, production-ready state
- `claude/...` — branches created for AI-assisted tasks
- `feature/<short-description>` — new features
- `fix/<short-description>` — bug fixes

### Making Changes

1. Always work on a feature or fix branch — never commit directly to `main`
2. Write clear, descriptive commit messages (imperative mood)
3. Push with `git push -u origin <branch-name>`
4. Open a pull request to merge into `main`

### Git Commit Conventions

```
<type>: <short summary>

<optional body explaining WHY, not WHAT>
```

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`

Examples:
- `feat: add CSV export for bulk listing updates`
- `fix: handle missing image URLs in product parser`
- `test: add fixtures for Etsy API mock responses`

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
- Do not create `*.md` documentation files unless explicitly requested

### Code Style

- **Python version:** 3.11+
- **Formatter:** `black` (line length 88)
- **Linter:** `ruff` (replaces flake8/isort)
- **Type hints:** required on all public functions and methods
- **Docstrings:** one-line only where the purpose isn't obvious from the name; no multi-paragraph docstrings
- Run before committing:

```bash
black src/ tests/
ruff check src/ tests/
```

### Environment Variables

Required variables (copy `.env.example` to `.env` and fill in):

```
ETSY_API_KEY=        # Etsy API v3 key (from Etsy developer portal)
ETSY_SHOP_ID=        # Numeric Etsy shop ID
ETSY_REDIRECT_URI=   # OAuth redirect URI (for user auth flows)
```

Never commit `.env` or any file containing real credentials. `.env` is in `.gitignore`.

### API Notes

- The project uses **Etsy API v3** (`https://openapi.etsy.com/v3`)
- OAuth 2.0 is required for write operations (listings, uploads)
- Rate limits: 10 req/s per key — add appropriate backoff on 429 responses
- File uploads use the Etsy Digital Downloads API endpoint

## Testing

**Framework:** `pytest`

- Tests live in `tests/` and mirror the `src/` structure
- Use `pytest.fixture` in `conftest.py` for shared setup (API mock clients, sample listing data)
- Mock all external API calls — never hit the real Etsy API in tests
- Use `pytest-mock` (`mocker` fixture) for mocking
- Target: all public functions have at least one test; critical paths have edge-case coverage

```bash
pip install pytest pytest-mock pytest-cov
pytest --cov=src --cov-report=term-missing
```

## CI/CD

**Provider:** GitHub Actions

The CI pipeline (`.github/workflows/ci.yml`) runs on every push and pull request to `main`:

1. Lint — `ruff check src/ tests/`
2. Format check — `black --check src/ tests/`
3. Tests — `pytest --cov=src`

PRs must pass CI before merging. AI assistants should ensure code passes linting and tests locally before pushing.

## Updating This File

Keep this file current as the project evolves:
- When new directories or modules are added, update the structure section
- When new environment variables are required, document them here
- When dependencies change, update the setup commands
- When CI steps change, update the CI/CD section
