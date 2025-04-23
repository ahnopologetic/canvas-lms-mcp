# Development Guide for Canvas LMS MCP Server

This guide provides detailed instructions for developing and contributing to the Canvas LMS MCP server.

## Development Environment Setup

### Prerequisites

- Python 3.13+
- `uv` package manager

### Setting Up Your Development Environment

1. Install uv:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/canvas-lms-mcp.git
   cd canvas-lms-mcp
   ```

3. Create a virtual environment and install development dependencies:
   ```bash
   uv venv
   uv pip install -e ".[dev]"
   ```

## Development Workflow

### Running the Server Locally

```bash
uv run src/canvas_lms_mcp/main.py
```

### Making Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and run the linter to ensure code quality:
   ```bash
   uv run ruff check .
   uv run ruff format .
   ```

3. Run tests to verify your changes:
   ```bash
   uv run pytest
   ```

### Using uv for Development Tasks

#### Managing Dependencies

Add a new dependency:
```bash
uv add package-name
```

Add a development dependency:
```bash
uv add --dev package-name
```

Update dependencies:
```bash
uv pip sync
```

#### Running Tools

Run tools without installing them:
```bash
uvx black .
uvx mypy .
```

#### Project Management

Initialize or update lock file:
```bash
uv lock
```

Build the project:
```bash
uv build
```

## Testing

### Running Tests

Run all tests:
```bash
uv run pytest
```

Run tests with coverage:
```bash
uv run pytest --cov=canvas_lms_mcp
```

### Testing with Different Python Versions

You can test with different Python versions using uv's python management:

```bash
uv python install 3.13
uv python install 3.11

# Run tests with Python 3.13
uv python -m pytest --python 3.13

# Run tests with Python 3.11
uv python -m pytest --python 3.11
```

## Documentation

Update documentation when you make significant changes:

1. Update docstrings in the code
2. Update the README.md if needed
3. Add examples for new features

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Commit changes:
   ```bash
   git add .
   git commit -m "Bump version to x.y.z"
   ```
4. Tag the release:
   ```bash
   git tag -a vx.y.z -m "Version x.y.z"
   ```
   
   > **Important**: Ensure the version tag (without the 'v' prefix) matches exactly with the version in pyproject.toml
   
5. Push changes and tags:
   ```bash
   git push origin main
   git push origin vx.y.z
   ```

6. The GitHub Actions workflow will automatically:
   - Verify that the tag version matches the version in pyproject.toml
   - Build the package
   - Publish it to PyPI

## Setting up PyPI Publishing

To enable automatic PyPI publishing:

1. Create an API token on PyPI:
   - Log into your PyPI account
   - Go to Account Settings > API tokens
   - Create a new API token with scope "Upload to project"

2. Add the token to your GitHub repository:
   - Go to your GitHub repository
   - Navigate to Settings > Secrets > Actions
   - Add a new secret named `PYPI_API_TOKEN` with your PyPI token as the value

## Continuous Integration

The project uses CI to run tests and linting on each pull request. Make sure your code passes all CI checks before requesting a review. 