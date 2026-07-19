# Contributing to Stadium Coordinator

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/stadium-coordinator`
3. Create a branch: `git checkout -b feat/your-feature-name`
4. Install dependencies: `pip install -r requirements.txt`
5. Make your changes
6. Run tests: `pytest tests/ -v`
7. Commit and push, then open a Pull Request

## Branch Naming

| Type | Format | Example |
|------|--------|---------|
| Feature | `feat/description` | `feat/gemini-integration` |
| Bug Fix | `fix/description` | `fix/crowd-chart-error` |
| Docs | `docs/description` | `docs/api-reference` |
| Tests | `test/description` | `test/data-loader-coverage` |

## Commit Messages (Conventional Commits)

```
feat: add Gemini AI integration
fix: resolve NaN handling in context builder
docs: update installation guide
test: add unit tests for data_loader
refactor: split mission control into subtabs
```

## Pull Request Checklist

- [ ] Tests pass: `pytest tests/ -v`
- [ ] No hardcoded secrets or API keys
- [ ] Type hints added for new functions
- [ ] Docstrings added for new modules/functions
- [ ] README updated if adding a new feature
- [ ] No absolute file paths

## Code Style

- Max line length: 120 characters
- Follow PEP 8
- Use type hints for all function signatures
- Docstrings for all public functions

## Security

Never commit `.env` files, API keys, or credentials.
See [SECURITY.md](SECURITY.md) for our vulnerability reporting process.
