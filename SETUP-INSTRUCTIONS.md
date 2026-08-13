# LTC Summer School 2026 participant setup


## 1 Prerequisites

👉 Before the session, go to the EC store and install:

- approved 64-bit Python 3.12 (the `py -3.12` or `python` command must work);
- Visual Studio Code (a.k.a VS code);
- the Microsoft **Python** extension (`ms-python.python`); and
- the Microsoft **Jupyter** extension (`ms-toolsai.jupyter`).

👉 Make sure you have been granted access to the local GPT@EC and an API key.

##### *(Administrator rights, `uv`, and PowerShell scripts are not required for the course setup itself.)*

## 2 Download and extract course package 

👉 Download the repository: on the [main repository page](..), find **< > Code** (big green button)
and select **Download ZIP**. Extract the complete  package into a writable local 
to create your project directory (e.g., `.../CATE/dgt-summer-school-2026/`). 

   Keep the notebooks, setup files and `pyproject.toml` together in the supplied
   folder structure. Do not transfer `.venv` from another computer.


## Run the setup

👉 Go to the project directory, and double-click **setup.cmd** to run it.

   > Alternatively, from PowerShell or Command Prompt in the project directory✳️,
   run:
   
   ```bash
   setup.cmd
   ```
   
   > or invoke the Python bootstrap directly by running:
   
   ```bash
   py -3.12 setup_environment.py
   ```

#### NOTE ✳️ 
   *To run PowerShell from the project directory, go to the project directory,* 
   *hold down the Shift key and right-click anywhere to open up the explorer menu.*
   *Select **Open PowerShell here***
   
The bootstrap will:
   
      1. read the preconfigured proxy server URL and GPT@EC settings from `.env`;
      2. ask only for your *proxy username*, *proxy password*, and *GPT@EC API key* when
         those values are still blank;
      3. create a local `.venv` using the approved Python 3.12 interpreter;
      4. install the locked, hash-verified dependencies, including CPU-only PyTorch;
      5. run dependency and import checks; and
      6. register the environment as the named Jupyter kernel
         **Python (DGT Summer School 2026)**.

#### NOTE ✳️  
   *If you mistype anything, you can open `.env` with Notepad and manually correct it.*

## Open project in Visual Studio Code

👉 After setup, open VS Code and use **File > Open Folder** to open the extracted
`dgt-summer-school-2026` installation folder (not just an individual notebook). 
The notebooks are already associated with the following named kernel:

```text
Python (DGT Summer School 2026)
```

#### NOTE ✳️ 
   On a clean machine, VS Code should match the notebook metadata to the registered
   kernel. If the notebook still says **Select Kernel**, or if VS Code was already*
   open during setup, restart VS Code. Then use the kernel picker in the upper-right:
   **Select Another Kernel > Jupyter Kernels > Python (DGT Summer School 2026)**.
   
   Do not choose the entry under **Python Environments** if you want the named label;
   that equivalent route may be displayed simply as `.venv (Python 3.12.x)`.


## 2 - Running the notebooks

👉 Run `[notebooks/1_Minimal_openai_and_embeddings.ipynb](notebooks/1_Minimal_openai_and_embeddings.ipynb)` for the smallest example of
calling the chat API and computing local `sentence-transformers` embeddings. To run
the notebook, use options A or B described below.

Notebook 2 and 3 are completely optional.

### A) Running notebooks in the browser 
Launch **Jupyter Lab** from the project root — it opens in your
browser automatically:

   ```bash
   jupyter lab
   ```
   
   Then, open a notebook from `notebooks/` and pick the
   **"DGT Summer School 2026 (uv)"** kernel via **Kernel → Change Kernel…** (or the
   kernel name in the top-right). Stop the server with `Ctrl+C` in the terminal.

### B) Running notebooks directly in VS Code

Double-click a notebook in `/notebooks`, it should open in a new tab
in VS Code. Read through and run the code in the cells. 

   If it asks for a kernel, select the **"DGT Summer School 2026 (uv)"**
   kernel (or, equivalently, the interpreter at`.venv` — 
   Windows: `.venv\Scripts\python.exe`, macOS/Linux: `.venv/bin/python`).




### Additional notes

### About setup.md and .env
Do not change the proxy URL, `OPENAI_BASE_URL`, or `OPENAI_MODEL` supplied in
`.env`. Interactive prompting URL-encodes special characters in proxy
credentials automatically.

The *proxy username*, *proxy password* and *GPT@EC API* key are deliberately displayed
while you type so that you can verify them. Make sure **nobody else can see your** 
**screen**. The resulting URL, credentials and *GPT@EC API key* are also saved in
plaintext (with URL encoding where required) in the project `.env`. **Do not share**
your completed `.env` or commit it to source control. Settings are applied only
to the installation process and to programs which later load the project `.env`;
no machine-wide proxy settings are changed.

If an existing `.venv` is found, the bootstrap offers to preserve and reuse it.
The default is to move it to a timestamped backup and create a genuinely local
environment. This is strongly recommended for an environment copied from
another computer.

#### New notebooks
The installation bootstrap reads `.env`, but a notebook started later is a new
process and must load the file itself. The course notebooks may already contain
this step.

To recreate an existing environment without prompting, run:

```bash
setup.cmd --recreate
```

For a non-interactive installation, fill all three blank credential fields in
`.env` first and run:

```bash
setup.cmd --non-interactive
```


#### Notebooks requiring internet access

At the beginning of each notebook that needs internet access, load the project
settings before making API calls or downloading models:

```python
from dotenv import load_dotenv
load_dotenv()
```

### Running Python scripts outside the notebooks

To run notebooks as regular python scripts, you can always convert them
to the correct `.py` format where all the 'regular', non-code text is 
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


## Policy and proxy limitations

The batch file merely locates the approved Python 3.12 interpreter and invokes
`setup_environment.py`. It does not alter or bypass PowerShell execution policy.
If Group Policy or application control also prohibits batch files or local
Python scripts, stop and request the normal IT approval rather than bypassing
the restriction.

The proxy URL approach works with standard HTTP/HTTPS proxy authentication. If
the corporate proxy requires NTLM, Kerberos, a PAC file, or a locally managed
proxy helper, username and password in the URL may not be sufficient. An HTTP
407 response normally indicates that the authentication method or credentials
need to be checked with IT.
