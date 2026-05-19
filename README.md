# Setup Development Environment

Before contributing, make sure your environment is ready.

## Install UV

We use UV for dependency management, running tests, and pre-commit hooks.

- [Installing UV](https://docs.astral.sh/uv/getting-started/installation/)

## Clone the Repository

```bash
git clone git@github.com:clause/CS1-Variable-Name-Analysis.git
```

## Install project dependencies

```bash
cd CS1-Variable-Name-Analysis
uv sync --all-extras --all-packages
uv run pre-commit run --all-files
```

# Code Formatting & Style Requirements

To keep the codebase consistent and maintainable, please follow these formatting rules:

## Python Style

We use ruff (via UV) to enforce code style and linting rules: See pyproject.toml for the configuration. A pre-commit hook runs ruff automatically and will prevent commits of poor quality code. You can have ruff automatically fix issues by running the following from the project root.

```bash
uv run ruff fix .
```

However, if you're using VS Code, you should install the project's recommended extensions. If you do so, the provided configuration in .vscode/settings.json will reformat on save.
