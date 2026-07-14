# DGT Summer School 2026

Code material for **DGT Summer School 2026** (NLP: prompting, retrieval-augmented
generation, and agents).

## Contents

The repository is organised as follows:

| Path | Contents |
|---|---|
| `notebooks/` | Teaching materials and demos (Jupyter notebooks). |
| `pyproject.toml`, `uv.lock` | Reproducible Python environment (see [Setup](#setup)). |
| `README.md` | This file. |

New teaching material and demos go under `notebooks/`.

All notebooks call the **OpenAI API** — no local GPU or model download is required.

## Prerequisites

- **[uv](https://docs.astral.sh/uv/)** — the Python package/environment manager.
  - macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **Python 3.12** — uv installs it automatically if it is missing (see below).
- An **OpenAI API key** — https://platform.openai.com/api-keys

## Setup

### 1. Get the code

**If you have git:**

```bash
git clone <this-repo-url>
cd dgt-summer-school-2026
```

**If you don't have git**, download a ZIP instead: on this page, find **Code** (big green button), **Download ZIP**, then unzip it and open a terminal in that folder.

### 2. Create the environment

```bash
uv sync
```

This reads `pyproject.toml` + `uv.lock` and creates a `.venv/` with the **exact
locked versions** of every dependency — identical on Windows, macOS, and Linux.
It downloads a fair amount (PyTorch, models tooling), so start it early and let it
run while you do the next step.

> If Python 3.12 is not installed, run `uv python install 3.12` first (or let
> `uv sync` fetch it when prompted).

### 3. Configure your API access

> **Summer school participants:** you will **not** call OpenAI's models directly.
> Instead, the organisers provide you with a **custom base URL, model id(s), and
> API key** for the course. Put those provided values in `.env` below — you do
> not need your own OpenAI account.

Create a file named `.env` in the project root with these three settings:

```
OPENAI_API_KEY=sk-...your key here...
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

- `OPENAI_API_KEY` — the key provided by the organisers (or your own from
  https://platform.openai.com/api-keys if you are working outside the course).
- `OPENAI_MODEL` — the chat model id to use (use the model id you were given).
- `OPENAI_BASE_URL` — the API endpoint. Use the custom URL provided for the course;
  the default above points at OpenAI directly for anyone working outside it.

`.env` is git-ignored, so your key is never committed. The notebooks load these
values automatically via `python-dotenv`.

See `notebooks/Minimal_openai_and_embeddings.ipynb` for the smallest example of
calling the chat API and computing local `sentence-transformers` embeddings.

## Running the notebooks

### 1. Register the named Jupyter kernel

Register the environment once so it appears as a clearly-named kernel in the
Jupyter / VS Code kernel picker (instead of a generic `.venv`):

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

### 2. Open a notebook and select the kernel

**Jupyter Lab (browser):** launch it from the project root — it opens in your
browser automatically:

```bash
uv run jupyter lab
```

Then open a notebook from `notebooks/` and pick the
**"DGT Summer School 2026 (uv)"** kernel via **Kernel → Change Kernel…** (or the
kernel name in the top-right). Stop the server with `Ctrl+C` in the terminal.

**PyCharm / VS Code:** open the folder, open a notebook, and select the
**"DGT Summer School 2026 (uv)"** kernel (or, equivalently, the interpreter at
`.venv` — Windows: `.venv\Scripts\python.exe`, macOS/Linux: `.venv/bin/python`).

> The `!pip install ...` cells at the top of each notebook are **not needed** —
> `uv sync` already installed everything. You can skip (or delete) them.

## Running Python outside the notebooks (optional)

You normally don't need to "activate" anything — the notebooks run through the
kernel you selected above. To run Python from a terminal, prefix any command with
`uv run`:

```bash
uv run python                 # start a REPL in the project environment
uv run python some_script.py  # run a script
```

`uv run` uses the project's `.venv` automatically and works **identically on
Windows, macOS, and Linux**.

Prefer to activate the venv manually?

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

Then plain `python` uses the environment until you run `deactivate`.

## Notes

- **Reproducibility.** `uv.lock` pins every package (direct and transitive) to
  exact versions. Re-run `uv sync` anywhere to recreate the same environment.
  To intentionally update packages later: `uv lock --upgrade && uv sync`.
- **Cost.** Running the notebooks makes OpenAI API calls (embeddings + chat
  completions on `gpt-4o-mini` / `text-embedding-3-small`), which cost a small
  amount of credit — typically a few cents per full run.
- **Python version.** The project targets Python 3.12 (`requires-python =
  ">=3.12,<3.13"`).
