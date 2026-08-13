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

## Setup

👉 Read through the provided [`SETUP-INSTRUCTIONS.md`](SETUP-INSTRUCTIONS.md) which guides you to create a proper
environment `.venv/` with the **exact locked versions** of every dependency, 
specific to the local constraints and policies. Complete all steps (5) therein to run your first Python 
notebook. In the process, you will download a fair amount of data (PyTorch, models tooling), so start it early and let it run.

### API access

> Summer school participants will preferably **not** call OpenAI's models
> directly but use the locally installed models. 
> This is controlled by providing the relevant settings in the above setup 
> (by running `setup.cmd`) or manually in the file `.env`:

- `OPENAI_API_KEY` — your GPT@EC API key.
- `OPENAI_BASE_URL` — the GPT@EC API endpoint. 

> If information for the local models is not provided, the notebooks will 
fall back to default values, and you will need to obtain an API key from 
the organisers.

```
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5.1
OPENAI_BASE_URL=https://api.openai.com/v1
```


### Notes

- **Cost.** Running the notebooks makes OpenAI API calls (embeddings + chat
  completions on `gpt-5.1` / `text-embedding-3-small`), which cost a small
  amount of credit — typically a few cents per full run.
- **Python version.** The project targets Python 3.12 (`requires-python =
  ">=3.12,<3.13"`).
