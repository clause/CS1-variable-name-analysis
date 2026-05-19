# Setup Development Environment

Before contributing, make sure your environment is ready.

## Install UV

We use UV for dependency management, running tests, and pre-commit hooks.

- [Installing UV](https://docs.astral.sh/uv/getting-started/installation/)

## Clone the Repository

```bash
git clone git@github.com:clause/CS1-variable-name-analysis.git
```

## Install project dependencies

```bash
cd CS1-Variable-Name-Analysis
uv sync --all-extras --all-packages
uv run pre-commit run --all-files
```

# Run 

The project provides two entry points. The first analyzes a given data file and generates a .csv containing violation information. The second plots the empirical cumulative density functions from the analysis data.

```bash
uv run analysis <file>.json
uv run plot_ecdf <file>.csv
open <file>_ecdf.pdf
```

The initial .json file should contain an array of objects that look like:

```python
class Project(BaseModel, frozen=True):
    user_id: int
    data: Data
    model_config = {"extra": "allow"}

    class Data(BaseModel, frozen=True):
        source: str | None = Field(default=None, alias="/main.py")
        model_config = {"extra": "allow"}

```

# Code Formatting & Style Requirements

To keep the codebase consistent and maintainable, please follow these formatting rules:

## Python Style

We use ruff (via UV) to enforce code style and linting rules: See pyproject.toml for the configuration. A pre-commit hook runs ruff automatically and will prevent commits of poor quality code. You can have ruff automatically fix issues by running the following from the project root.

```bash
uv run ruff fix .
```

However, if you're using VS Code, you should install the project's recommended extensions. If you do so, the provided configuration in .vscode/settings.json will reformat on save.
