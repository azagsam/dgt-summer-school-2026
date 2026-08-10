"""Set up the LTC Summer School 2026 participant environment."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from datetime import datetime
from urllib.parse import quote, urlsplit, urlunsplit
import venv


ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"
REQUIREMENTS_FILE = ROOT / "requirements.lock.txt"
VENV_DIR = ROOT / ".venv"
KEY_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def read_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for line in path.read_text(encoding="utf-8-sig").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not KEY_PATTERN.fullmatch(key):
            continue
        if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                value = value[1:-1]
        elif len(value) >= 2 and value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        values[key] = str(value)
    return values


def write_dotenv_updates(path: Path, updates: dict[str, str]) -> None:
    existing = []
    if path.exists():
        existing = path.read_text(encoding="utf-8-sig").splitlines()

    remaining = dict(updates)
    output: list[str] = []
    for line in existing:
        if "=" in line:
            key = line.split("=", 1)[0].strip()
            if key in updates:
                output.append(f"{key}={json.dumps(str(updates[key]))}")
                remaining.pop(key, None)
                continue
        output.append(line)

    if output and output[-1].strip() and remaining:
        output.append("")
    for key in sorted(remaining):
        output.append(f"{key}={json.dumps(str(remaining[key]))}")

    path.write_text("\n".join(output) + "\n", encoding="utf-8")


def build_proxy_url(server: str, username: str = "", password: str = "") -> str:
    parsed = urlsplit(server)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Proxy server must be a URL beginning with http:// or https://")
    if parsed.path not in {"", "/"} or parsed.query or parsed.fragment:
        raise ValueError("Proxy server URL must not contain a path, query or fragment")

    hostname = parsed.hostname
    if ":" in hostname and not hostname.startswith("["):
        hostname = f"[{hostname}]"
    host = hostname
    if parsed.port is not None:
        host = f"{host}:{parsed.port}"

    if username:
        credentials = quote(username, safe="")
        if password:
            credentials += ":" + quote(password, safe="")
        host = credentials + "@" + host

    return urlunsplit((parsed.scheme, host, "", "", ""))


def prompt_required(prompt: str) -> str:
    """Prompt visibly until a non-empty value is entered."""
    while True:
        value = input(prompt)
        value = value.strip()
        if value:
            return value
        print("A value is required. Please try again.")


def configure_project_settings(non_interactive: bool) -> dict[str, str]:
    settings = read_dotenv(ENV_FILE)
    missing_course_settings = [
        key for key in ("OPENAI_BASE_URL", "OPENAI_MODEL") if not settings.get(key)
    ]
    if missing_course_settings:
        raise ValueError(
            "Missing preconfigured course setting(s) in .env: "
            + ", ".join(missing_course_settings)
        )

    proxy_server = settings.get("PROXY_SERVER", "").strip()
    username = settings.get("PROXY_USERNAME", "").strip()
    password = settings.get("PROXY_PASSWORD", "")
    api_key = settings.get("OPENAI_API_KEY", "").strip()

    if not api_key and non_interactive:
        raise ValueError(
            "Missing required value in .env for non-interactive setup: OPENAI_API_KEY"
        )

    if not non_interactive:
        if not api_key:
            api_key = prompt_required("GPT@EC API key: ")

    updates: dict[str, str] = {"OPENAI_API_KEY": api_key}
    if proxy_server:
        updates["HTTP_PROXY"] = build_proxy_url(proxy_server, username, password)
        updates["HTTPS_PROXY"] = build_proxy_url(proxy_server, username, password)
        if "NO_PROXY" not in settings:
            updates["NO_PROXY"] = "localhost,127.0.0.1"

    updates = {
        key: value for key, value in updates.items() if settings.get(key) != value
    }

    if updates:
        write_dotenv_updates(ENV_FILE, updates)
        print("Project settings saved in .env")

    return read_dotenv(ENV_FILE)


def backup_venv() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    destination = ROOT / f".venv.backup-{timestamp}"
    suffix = 1
    while destination.exists():
        destination = ROOT / f".venv.backup-{timestamp}-{suffix}"
        suffix += 1
    shutil.move(str(VENV_DIR), str(destination))
    print(f"Existing environment moved to: {destination}")
    return destination


def venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def venv_is_usable(python: Path) -> bool:
    if not python.is_file():
        return False
    result = subprocess.run(
        [
            str(python),
            "-c",
            "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 1)",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def prepare_venv(*, recreate: bool, reuse: bool, non_interactive: bool) -> Path:
    python = venv_python()

    if VENV_DIR.exists():
        should_recreate = recreate
        if not recreate and not reuse:
            if non_interactive:
                should_recreate = True
            else:
                answer = input(
                    "An existing .venv was found. Reuse it instead of creating a local one? [y/N] "
                ).strip().lower()
                should_recreate = answer not in {"y", "yes"}
        if should_recreate or not venv_is_usable(python):
            backup_venv()

    if not VENV_DIR.exists():
        print("Creating a local Python 3.12 virtual environment...")
        venv.EnvBuilder(with_pip=True).create(VENV_DIR)

    python = venv_python()
    if not venv_is_usable(python):
        raise RuntimeError("The local Python 3.12 virtual environment could not be created")
    return python


def run_checked(command: list[str], *, env: dict[str, str]) -> None:
    printable = " ".join(command)
    print(f"> {printable}")
    subprocess.run(command, cwd=ROOT, env=env, check=True)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create and verify the DGT Summer School Python environment."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--recreate", action="store_true", help="Back up and recreate an existing .venv"
    )
    mode.add_argument(
        "--reuse", action="store_true", help="Reuse an existing valid Python 3.12 .venv"
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Read settings from .env without prompting",
    )
    parser.add_argument(
        "--skip-smoke-test",
        action="store_true",
        help="Skip the final import test",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    if sys.version_info[:2] != (3, 12) or sys.maxsize <= 2**32:
        print(
            "SETUP FAILED: run this script with the approved 64-bit Python 3.12 interpreter.",
            file=sys.stderr,
        )
        return 1
    if not REQUIREMENTS_FILE.is_file():
        print("SETUP FAILED: requirements.lock.txt is missing.", file=sys.stderr)
        return 1

    try:
        settings = configure_project_settings(args.non_interactive)
        child_env = os.environ.copy()
        child_env.update(settings)
        child_env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"

        python = prepare_venv(
            recreate=args.recreate,
            reuse=args.reuse,
            non_interactive=args.non_interactive,
        )

        print("Installing locked dependencies. This can take several minutes...")
        run_checked(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--require-hashes",
                "--extra-index-url",
                "https://download.pytorch.org/whl/cpu",
                "-r",
                str(REQUIREMENTS_FILE),
            ],
            env=child_env,
        )
        run_checked([str(python), "-m", "pip", "check"], env=child_env)

        if not args.skip_smoke_test:
            print(
                "Running import checks. sentence_transformers may be slow on its first import..."
            )
            smoke_test = (
                "import sys, torch, faiss, langchain, openai, sentence_transformers, ipykernel; "
                "print('Imports OK'); "
                "print('Python:', sys.version.split()[0]); "
                "print('PyTorch:', torch.__version__); "
                "print('CUDA:', torch.cuda.is_available()); "
                "print('ipykernel:', ipykernel.__version__)"
            )
            run_checked([str(python), "-c", smoke_test], env=child_env)

        print("Registering the named Jupyter kernel...")
        run_checked(
            [
                str(python),
                "-m",
                "ipykernel",
                "install",
                "--user",
                "--name",
                "dgt-summer-school-2026",
                "--display-name",
                "Python (DGT Summer School 2026)",
            ],
            env=child_env,
        )

        print("\nSetup completed successfully.")
        print('Notebook kernel: Python (DGT Summer School 2026)')
        print("Open a notebook in VS Code and select this named kernel.")
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"\nSETUP FAILED: {exc}", file=sys.stderr)
        print(
            "HTTP 407 usually means the proxy credentials or authentication method are wrong. "
            "Certificate errors may require PIP_CERT or REQUESTS_CA_BUNDLE in .env.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
