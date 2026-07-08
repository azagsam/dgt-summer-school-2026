# DGT Summer School 2026

Code material for **DGT Summer School 2026** (NLP: prompting, retrieval-augmented
generation, and agents).

## Contents

All notebooks call the **OpenAI API** — no local GPU or model download is required.

## Prerequisites

- **[uv](https://docs.astral.sh/uv/)** — the Python package/environment manager.
  - macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **Python 3.12** — uv installs it automatically if it is missing (see below).
- An **OpenAI API key** — https://platform.openai.com/api-keys

## Setup

### 1. Get the code

```bash
git clone <this-repo-url>
cd dgt-summer-school-2026
```

### 2. Add your OpenAI API key

Create a file named `.env` in the project root with a single line:

```
OPENAI_API_KEY=sk-...your key here...
```

`.env` is git-ignored, so your key is never committed. The notebooks load it
automatically via `python-dotenv`.

### 3. Create the environment

```bash
uv sync
```

This reads `pyproject.toml` + `uv.lock` and creates a `.venv/` with the **exact
locked versions** of every dependency — identical on Windows, macOS, and Linux.

> If Python 3.12 is not installed, run `uv python install 3.12` first (or let
> `uv sync` fetch it when prompted).

## Running the notebooks

**Option A — JupyterLab (from the terminal):**

```bash
uv run jupyter lab
```

Then open a notebook in the browser tab that appears.

**Option B — VS Code / another IDE:**

Open the folder, open a notebook, and select the interpreter at
`.venv` (Windows: `.venv\Scripts\python.exe`, macOS/Linux: `.venv/bin/python`)
as the notebook kernel.

### Registering a named Jupyter kernel (optional)

If you want the environment to appear as a clearly-named kernel in the
Jupyter / VS Code kernel picker (instead of a generic `.venv`), register it once:

```bash
uv run python -m ipykernel install --user --name dgt-ss-2026 --display-name "DGT Summer School 2026 (uv)"
```

It will then show up as **"DGT Summer School 2026 (uv)"** when you choose a kernel.

Manage the registered kernels:

```bash
# list all installed kernels
uv run jupyter kernelspec list

# remove this one when you no longer need it
uv run jupyter kernelspec uninstall dgt-ss-2026
```

> The kernel points at this project's `.venv`. If you delete and recreate the
> `.venv` (e.g. another `uv sync`), the kernel keeps working as long as the
> project path is unchanged; if you move the project, re-run the install command.

> The `!pip install ...` cells at the top of each notebook are **not needed** —
> `uv sync` already installed everything. You can skip (or delete) them.

## Notes

- **Reproducibility.** `uv.lock` pins every package (direct and transitive) to
  exact versions. Re-run `uv sync` anywhere to recreate the same environment.
  To intentionally update packages later: `uv lock --upgrade && uv sync`.
- **Cost.** Running the notebooks makes OpenAI API calls (embeddings + chat
  completions on `gpt-4o-mini` / `text-embedding-3-small`), which cost a small
  amount of credit — typically a few cents per full run.
- **Python version.** The project targets Python 3.12 (`requires-python =
  ">=3.12,<3.13"`).
