# Python Development Guidelines

## 1. Python Project Structure
- Manage dependencies using `uv` CLI and `pyproject.toml`.
- Configure `pyproject.toml` with:
  - Entry points for `python -m`.
  - Scripts, homepage, and development dependencies.
  - Resources and data directories inclusion.
- Follow standard PyPI project layout:
  - Include `tests` and library name directories.
  - Avoid nested `src` directory.
- Write a `README.md` with:
  - Project purpose and pain points solved.
  - Installation instructions via `pip`.
  - Usage examples (module, `python -m`, or script).
  - Development guide.
  - Links to homepage, email, `https://deepwiki.com/githubusername/projectname`, and GitHub issues.

## 2. Python Coding Practices
- Adhere to PEP 8 naming conventions.
- Use type hints consistently for code clarity.
- Extract reusable operations into standalone modules.
- Organize code using the Model-View-Presenter (MVP) pattern.
- Leverage advanced Python features:
  - `functools`, `collections`, and `itertools`.
  - Functional programming: iterators, generators, `reduce`, `map`, `filter`, `sort` with key functions.
  - Self-inspection, `random`, context managers, and first-class functions.
- Use threading for network-bound or wait-heavy operations.
- Employ multiprocessing for CPU- or I/O-intensive tasks.
- Include clear comments to outline code structure and major sections.
- Use meaningful, contextual variable names (up to five words).
- Refactor code blocks exceeding 20 lines into separate functions.
- Name functions with action-driven verbs (e.g., `chunk_data`, `preview_file`, `cache_result`).

## 3. Preferred Python Libraries
- Logging: `loguru`.
- Data validation: `pydantic`.
- Progress bars: `tqdm`.
- Database operations: `sqlmodel`, `sqlite3`.
- Large file I/O: `memoryview`, `mmap`.
- Large datasets: `pandas` or `polars`.
- Retry logic: `tenacity`.
- HTTP requests: `httpx` (preferred over `requests`).
- Prefer popular, well-starred GitHub libraries unless they lack capability or reliability.

## 4. Testing and Quality Assurance
- Write unit tests using `pytest` with:
  - Fixtures and parameterization.
  - Debug logging with level enablement.
- Ensure at least 80% test coverage with `coverage.py`.
- Maintain code style with `ruff` or `black`.
- Cache expensive functions with `functools.lru_cache`.
- Implement asynchronous I/O with `asyncio`.

## 5. Documentation and Collaboration
- Generate API documentation using `Sphinx` or `MkDocs`.
- Write docstrings in Google or NumPy style.
- Maintain a changelog for versioned releases.

## 6. Security Practices
- Sanitize user inputs with `bleach` or similar libraries.
- Manage secrets using `python-dotenv` or `keyring`.
- Validate API inputs with `pydantic` schemas.
- Securely hash passwords with `bcrypt` or `argon2`.

## 7. Web Development
- Build full-stack applications with `Django`.
- Implement WebSocket functionality with `aiohttp` or `channels`.
- Use `Jinja2` or similar for templating.

## 8. always use `uv` CLI
- Use `uv` CLI for managing Python projects, including:
  - Running scripts with `uv run`.
  - Installing dependencies with `uv install`.
  - Managing virtual environments with `uv venv`. 

## 9. always consider the unicode support
- Ensure your code handles Unicode characters properly, especially for non-ASCII text.
- Use libraries like `ftfy` or `unidecode` to clean and normalize text.
- Test your application with a variety of languages and character sets.