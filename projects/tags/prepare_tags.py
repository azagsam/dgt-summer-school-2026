"""Read TSV files, extract source tags, and save prepared.json."""
# %% Imports and file paths
import csv
import json
import re
from pathlib import Path

# Paths are relative to the project root; edit these for your files.
DEV = Path("projects/tags/dev")
INPUT_PATH = DEV / "main.tsv"
EXAMPLES_PATH = DEV / "examples.tsv"
OUTPUT_PATH = DEV / "prepared.json"

# %% Tag extraction and TSV reading
TAG_PATTERN = re.compile(
    r"<!--.*?-->|<!\[CDATA\[.*?\]\]>|<\?.*?\?>|"
    r"(?P<tag></?[A-Za-z_:][\w:.-]*(?=[\s/>])"
    r"(?:[^<>\"']|\"[^\"]*\"|'[^']*')*>)", re.DOTALL,
)


def tag_regex(text):
    """Extract tags in order, preserving attributes and duplicates."""
    return [m.group("tag") for m in TAG_PATTERN.finditer(text) if m.group("tag")]


def read_tsv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter="\t")
        headers = reader.fieldnames or []
        if (not {"Source", "Translation"}.issubset(headers)
                or any(not h.strip() for h in headers)
                or len(headers) != len(set(headers))):
            raise ValueError(f"{path}: need unique headers including Source and Translation")
        rows = list(reader)
    for row in rows:
        if None in row or row["Source"] is None or row["Translation"] is None:
            raise ValueError(f"{path}: a row has the wrong number of columns")
        row.update({key: "" for key, value in row.items() if value is None})
        row["Tags"] = tag_regex(row["Source"])
    return rows


# %% Read and process the files
examples = read_tsv(EXAMPLES_PATH)
rows = read_tsv(INPUT_PATH)
data = {"examples": examples, "rows": rows}

# %% Save the processed data
if OUTPUT_PATH.resolve() in {INPUT_PATH.resolve(), EXAMPLES_PATH.resolve()}:
    raise ValueError("Output must differ from the input files")

with OUTPUT_PATH.open("w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
    file.write("\n")
print(f"Saved {len(rows)} rows to {OUTPUT_PATH}")
