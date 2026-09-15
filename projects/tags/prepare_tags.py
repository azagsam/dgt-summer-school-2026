"""Read TSV files, extract source tags, and save prepared.json."""
import argparse
import csv
import json
import re
from pathlib import Path

DEV = Path(__file__).parent / "dev"
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEV / "main.tsv")
    parser.add_argument("--examples", type=Path, default=DEV / "examples.tsv")
    parser.add_argument("-o", "--output", type=Path, default=DEV / "prepared.json")
    args = parser.parse_args()
    if args.output.resolve() in {args.input.resolve(), args.examples.resolve()}:
        parser.error("Output must differ from the input files")
    data = {"examples": read_tsv(args.examples), "rows": read_tsv(args.input)}
    with args.output.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")
    print(f"Saved {len(data['rows'])} rows to {args.output}")


if __name__ == "__main__":
    main()
