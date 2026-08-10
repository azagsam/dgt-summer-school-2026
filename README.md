# DGT Summer School 2026

Code material for **DGT Summer School 2026** (NLP: prompting, retrieval-augmented
generation, and agents).

## Contents

The repository is organised as follows:

| Path                        | Contents                                         |
|-----------------------------|--------------------------------------------------|
| `notebooks/`                | Teaching materials and demos (Jupyter notebooks). |
| `README.md`                 | This file.                                       |
| `SETUP-INSTRUCTIONS.md`     | DGT-specific installation instructions.          |
| `setup.cmd`                 | DGT-specific script to install the environment.  |
| `pyproject.toml`, `uv.lock` | Reproducible Python environment for uv users.    |

## Prerequisites

Read through the provided `SETUP-INSTRUCTIONS.md` which guides you to create a proper
environment `.venv/` with the **exact locked versions** of every dependency. 
It downloads a fair amount (PyTorch, models tooling), so start it early and let it run.

### API access

> **Summer school participants:** you will preferably **not** call OpenAI's models
> directly but use the locally installed models. You should have defined this via 
> the above setup (by running `setup.cmd`) or manually in the file `.env` 
> with these three settings:

- `OPENAI_API_KEY` — input your GPT@EC API key.
- `OPENAI_BASE_URL` — the GPT@EC API endpoint. 

If information for the local models is not provided, the notebooks will 
fall back to default values, and you will need to obtain an API key from 
the organisers:

```
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5.1
OPENAI_BASE_URL=https://api.openai.com/v1
```

`.env` is git-ignored, so your key is never committed. The notebooks load these
values automatically via `python-dotenv`.

See `notebooks/Minimal_openai_and_embeddings.ipynb` for the smallest example of
calling the chat API and computing local `sentence-transformers` embeddings.

## Running the notebooks

### Open a notebook and select the kernel

**Jupyter Lab (browser):** launch it from the project root — it opens in your
browser automatically:

```bash
jupyter lab
```

Then open a notebook from `notebooks/` and pick the
**"DGT Summer School 2026 (uv)"** kernel via **Kernel → Change Kernel…** (or the
kernel name in the top-right). Stop the server with `Ctrl+C` in the terminal.

**Jupyter Lab (VS Code):** double-click a notebook in `/notebooks`, 
and select the **"DGT Summer School 2026 (uv)"** kernel (or, equivalently, 
the interpreter at `.venv` — Windows: `.venv\Scripts\python.exe`,
macOS/Linux: `.venv/bin/python`).


## Running Python outside the notebooks (optional)

To run notebooks as regular python scripts, you can always convert them
to the correct `.py` format (where all the 'regular', non-code text is 
commented out to let Python know to ignore it). 

To convert, right-click a `.ipynb` notebook and select 
- VS Code: 'Import Notebook to Script', then name and save the newly created file.
- PyCharm: 'Convert to Python file' (automatically creates and saves file).

You normally don't need to "activate" anything — the notebooks run through the
kernel you selected above. To run Python from a terminal, prefix any command with
`python`:

```bash
python some_script.py  # run a script
```

Prefer to activate the venv manually? Run:

```bash
# on Windows (PowerShell)
.venv\Scripts\Activate.ps1

```

Then plain `python` uses the environment until you run `deactivate`.

## Notes

- **Cost.** Running the notebooks makes OpenAI API calls (embeddings + chat
  completions on `gpt-5.1` / `text-embedding-3-small`), which cost a small
  amount of credit — typically a few cents per full run.
- **Python version.** The project targets Python 3.12 (`requires-python =
  ">=3.12,<3.13"`).
