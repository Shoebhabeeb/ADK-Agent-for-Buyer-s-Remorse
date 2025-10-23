# Customer Solutions Data Science Resolutions Agent
[![](https://img.shields.io/badge/Python-3.10|3.11|3.12-blue)](https://www.python.org)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pyright](https://img.shields.io/badge/Pyright-enabled-brightgreen)](https://github.com/microsoft/pyright)


## How to contribute

1. Create a new branch
    ```
    git checkout -b <branch-name> # replace
    ```

2. Install Poetry
- [See the Poetry documentation](https://python-poetry.org) for more details and alternate methods. Examples include:
    ```
    # using pipx.
    pipx install poetry
    ```

3. Ensure virtual enivornment is intalled in your project directory
    ```
    poetry config virtualenvs.in-project true
    ```

4. Update project metadata in:
    - `pyproject.toml`:
        - Change the project name, version, and author information to match your package.
    - `README.md`:
        - Replace placeholder names, badges, and repository links with those for your project.

4. Aftering updating `.toml` run `poetry lock` to update `poetry.lock` file:
    ```
    poetry lock
    ```

5. Install package and dependencies needed for development:
    ```
    poetry install
    ```

6. Enable pre-commit hooks in your local environment so they run automatically before every commit:
    ```
    poetry run pre-commit install
    ```

## Using Poetry
For the full Poetry documentation, visit the [full docs](https://python-poetry.org)

### Managing Dependencies
- Adding Dependencies
    - To add a new runtime dependency to your project, use:
        ```
        poetry add <package_name>
        ```
    - Example:
        ```
        poetry add requests
        ```
        This updates your `pyproject.toml` under [project.dependencies] and synchronizes your virtual environment automatically.

    - For dev-only dependencies, you can specify --dev:
        ```
        poetry add pytest --group dev
        ```
        This updates [tool.poetry.group.dev.dependencies] in your pyproject.toml.

    - Poetry provides a way to organize your dependencies by groups. So you can
    create a new dependency group:
        ```
        poetry add pytest --group <new-dependency-group>
        ```
        Read more about this [here](https://python-poetry.org/docs/managing-dependencies/)

- Removing Dependencies
    - Similarly, to remove a dependency:
        ```
        poetry remove requests
        ```
        Poetry removes the package from your pyproject.toml and uninstalls it from your virtual environment.

### Updating Package Version
- Before merging a branch into main to release a new version of your package you will need to update the version number in the pyproject.toml. If you do not update the verrsion number before merging to the main branch the release-and-tag.yml workflow will fail.
    ```
    poetry version <bump-rule>
    ```
    Provide a valid bump rule: patch, minor, major, prepatch, preminor, premajor, prerelease.

## CI-CD Workflows

This project uses GitHub Actions for continuous integration and deployment.

### On Push to Non-Main Branches
File: `.github/workflows/ci.yml`

- **Linting & Formatting:** Runs `pre-commit` checks using `ruff`.
- **Testing:** Runs `pytest` across Python 3.10, 3.11, and 3.12.
- **Coverage Upload:** Sends test coverage reports to Codecov.


### On Merging into Main
File: `.github/workflows/release-and-tag.yml`. You will need to open and approve a pull request to main to trigger this workflow.

- **Tagging & Releasing:** Automatically tags a new version based on `pyproject.toml`.
- **Builds the Package:** Uses Poetry to create distribution files.
- **Creates a GitHub Release:** Uploads the built package to GitHub releases.


## How to run ADK Agent
1. Populate an `.env` file
```bash
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_HERE
GOOGLE_CLOUD_LOCATION="us-central1"
RAG_CORPUS="projects/hd-contactctr-dev/locations/us-central1/ragCorpora/5764607523034234880"
GOOGLE_CLOUD_LLM_NAME = 'gemini-2.5-flash'
```

2. Go to `resolutions_agent` directory
```
cd resolutions_agent
```

3. Run
```
poetry run adk web
```

## How to update the RAG engine
In the `construct_kb` you can update the `.json` file and then run
`poetry run python main.py`