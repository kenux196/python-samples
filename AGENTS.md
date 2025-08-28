# Repository Guidelines

## Project Structure & Module Organization
- `pyproject.toml`: Project metadata and Python (3.11) constraints.
- `uv.lock`: Locked dependencies managed by `uv`.
- `with-chatgpt/`: Standalone Python scripts:
  - `tetris.py` (game sample)
  - `mp4tomp3.py` (media conversion via `pydub`)
  - `straching-routine.py` (utility sample)
- `.vscode/`: Editor settings. `.python-version` pins the interpreter.

## Setup, Run, and Development Commands
- Create venv and install deps: `uv venv && uv sync`
- Run a script (examples):
  - `uv run python with-chatgpt/tetris.py`
  - `uv run python with-chatgpt/mp4tomp3.py --help`
- Add a dependency: `uv add <package>` (updates `pyproject.toml` and `uv.lock`).

## Coding Style & Naming Conventions
- Follow PEP 8; use 4‑space indentation.
- Use `snake_case` for files, functions, and variables; `UpperCamelCase` for classes.
- Prefer small, single‑purpose scripts under `with-chatgpt/` with module‑level docstrings.
- Add type hints where practical and keep imports standard‑library first, then third‑party.

## Testing Guidelines
- No formal test suite yet. If adding tests:
  - Place under `tests/`, mirroring script names (e.g., `tests/test_tetris.py`).
  - Use `pytest` (`uv add pytest`) and run with `uv run pytest -q`.
  - Aim for basic behavior coverage of each script’s main paths.

## Commit & Pull Request Guidelines
- Commits: imperative mood and concise subjects (e.g., `Add tetris game`, `Fix: indent error`).
- Group related changes; reference issues when applicable.
- PRs: include a short description, affected scripts/paths, run instructions, and any screenshots/output for user‑facing changes.

## Security & Configuration Tips
- `pydub` requires FFmpeg for audio/video: install via `brew install ffmpeg` (macOS) or your distro’s package manager.
- Use Python 3.11 as pinned; ensure your editor points to `.venv` (see `.vscode/settings.json`).
- Avoid committing large binaries; prefer links or generation steps in the README.

