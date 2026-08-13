# DGT Summer School 2026

Code material for **DGT Summer School 2026** (NLP: prompting, retrieval-augmented
generation, and agents).

## Contents

The repository is organised as follows:

| Path                       | Contents                                         |
|----------------------------|--------------------------------------------------|
| `notebooks/`               | Teaching materials and demos (Jupyter notebooks). |
| `README.md`                | This file.                                       |
| `pyproject.toml`, `uv.lock`| Reproducible Python environment for uv users.   |

## 0️⃣ Environment setup

👉 Read through the provided `SETUP-INSTRUCTIONS.md` which guide you to create a proper
environment with the **exact locked versions** of every dependency, 
specific to the local constraints and policies. In the process, you will download a fair
amount of data (PyTorch, models tooling), so start it early and let it run.


#### API access

> Summer school participants will preferably use the locally installed GPT models. 
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

## 1️⃣ Add project to Visual Studio Code

👉 After setup, open VS Code and use **File > Open Folder** to open the project folder,
e.g. `../dgt-summer-school-2026/`
The notebooks should already be associated with the following named kernel:

```text
Python (DGT Summer School 2026)
```
>  ✳️  On a clean machine, VS Code should match the notebook metadata to the registered
   kernel. If the notebook still says **Select Kernel**, or if VS Code was already*
   open during setup, restart VS Code. Then use the kernel picker in the upper-right:
   **Select Another Kernel > Jupyter Kernels > Python (DGT Summer School 2026)**.
> Do not choose the entry under **Python Environments** if you want the named label;
   that equivalent route may be displayed simply as `.venv (Python 3.12.x)`.


## 2️⃣ Run a notebook

👉 Run [`notebooks/1_Minimal_openai_and_embeddings.ipynb`](notebooks/1_Minimal_openai_and_embeddings.ipynb) 
for the smallest example of calling the chat API and computing local `sentence-transformers` embeddings. To run
the notebook, use options A or B described below.

Notebooks 2 and 3 are completely optional.

### A) Running notebooks directly in VS Code

Double-click a notebook in `/notebooks`, it should open in a new tab
in VS Code. Read through and run the code in the cells. 

> ✳️ If it asks for a kernel, first restart VS Code. Then use the kernel picker in the upper-right:
   **Select Kernel > Jupyter Kernel … > DGT Summer School 2026 (uv)**
   kernel (or, equivalently, the interpreter at`.venv` — 
   Windows: `.venv\Scripts\python.exe`, macOS/Linux: `.venv/bin/python`).


### B) Running notebooks in a web browser 
Launch **Jupyter Lab** from the terminal✳️ in the project root to  in your
browser automatically:

   ```bash
   jupyter lab
   ```
> ✳️ If you do not see the TERMINAL window, open it from the toolbar by selecting `Terminal > New terminal`.

It will automatically open Jupyter in your browser. There, double-click a notebook from `notebooks/` and pick the
   **"DGT Summer School 2026 (uv)"** kernel via **Kernel → Change Kernel…** (or the
   kernel name in the top-right). Stop the server with `Ctrl+C` in the terminal.

### C) Running Python scripts outside the notebooks

To run notebooks as regular python scripts, you can always convert them
to the `.py` format where all the 'regular', non-code text is 
commented out with # to let Python know to ignore it. 

To convert to `.py`, right-click a `.ipynb` notebook and select:

- VS Code: 'Import Notebook to Script', then name and save the newly created file.
- PyCharm: 'Convert to Python file' (automatically creates and saves file).

You also normally don't need to "activate" anything — the notebooks run through the
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


### Notes

- **Cost.** Running the notebooks makes OpenAI API calls (embeddings + chat
  completions on `gpt-5.1` / `text-embedding-3-small`), which cost a small
  amount of credit — typically a few cents per full run.
- **Python version.** The project targets Python 3.12 (`requires-python =
  ">=3.12,<3.13"`).

