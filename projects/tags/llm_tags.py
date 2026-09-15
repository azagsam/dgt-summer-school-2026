"""Read prepared.json, call the LLM, evaluate corrections, and save a TSV."""
# %% Imports and settings
import csv
import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError

# Settings loaded from .env (or existing environment variables).
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.1")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
print(f"Model    : {MODEL}")
print(f"Base URL : {BASE_URL}")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found - add it to your .env file.")

# Paths are relative to the project root; edit these for your files.
DEV = Path("projects/tags/dev")
INPUT_PATH = DEV / "prepared.json"
safe_model = "".join(c if c.isalnum() or c in "-_" else "_" for c in MODEL)
OUTPUT_PATH = DEV / f"results_{safe_model}.tsv"

# %% Prompt and evaluation helpers
SYSTEM_PROMPT = """Correct XML-like tags in the Translation using the Source.
Preserve the translated text. Preserve every source tag occurrence, including
attributes, IDs, order, and nesting, around the corresponding translated content.
Remove extra tags and repair missing, duplicated, malformed, or misplaced tags.
If the Source has no tags, remove all tags from the Translation.
Return JSON with string keys Corrected (the full corrected translation) and
Comment (an empty string unless the result needs review).
"""


TAG_PATTERN = re.compile(
    r"<!--.*?-->|<!\[CDATA\[.*?\]\]>|<\?.*?\?>|"
    r"(?P<tag></?[A-Za-z_:][\w:.-]*(?=[\s/>])"
    r"(?:[^<>\"']|\"[^\"]*\"|'[^']*')*>)", re.DOTALL,
)


def tag_regex(text):
    """Extract tags in order, preserving attributes and duplicates."""
    return [m.group("tag") for m in TAG_PATTERN.finditer(text) if m.group("tag")]


class TagOutput(BaseModel):
    Corrected: str
    Comment: str


def evaluate_row(row, client, model, examples):
    # Keep the reference answer out of the task sent to the model.
    task = {key: row[key] for key in ("Source", "Translation")}
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Examples:\n" + json.dumps(examples, ensure_ascii=False)
             + "\nTask:\n" + json.dumps(task, ensure_ascii=False)},
        ],
        response_format={"type": "json_object"},
    ).choices[0].message.content
    result = dict(row, Model=model, Raw=response, Model_Corrected="",
                  Model_Comment="", Error="", Model_Tags=[],
                  Tags_Match=False, Reference_Match="")
    try:
        answer = TagOutput.model_validate_json(response or "")
    except ValidationError as error:
        result["Error"] = str(error)
    else:
        tags = tag_regex(answer.Corrected)
        result.update(Model_Corrected=answer.Corrected, Model_Comment=answer.Comment,
                      Model_Tags=tags, Tags_Match=tags == row["Tags"])
        if row.get("Corrected"):
            result["Reference_Match"] = answer.Corrected == row["Corrected"]
    return result


# %% Read the prepared data
with INPUT_PATH.open(encoding="utf-8") as file:
    data = json.load(file)
examples = data["examples"]
rows = data["rows"]  # Use data["rows"][:3] to try a small batch.

# %% Connect to the model

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# %% Call the model and evaluate each row
results = []
for row in rows:
    result = evaluate_row(row, client, MODEL, examples)
    results.append(result)
    print(f"Processed {len(results)}/{len(rows)}")

# %% Review the scores
print(f"Tag sequence matches: {sum(r['Tags_Match'] for r in results)}/{len(results)}")
references = [r for r in results if r.get("Corrected")]
print(f"Exact reference matches: {sum(r['Reference_Match'] is True for r in references)}/{len(references)}")
print(f"Invalid responses: {sum(bool(r['Error']) for r in results)}")

# %% Save the results
if OUTPUT_PATH.resolve() == INPUT_PATH.resolve():
    raise ValueError("Output must differ from the input file")
if results:
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(results[0]), delimiter="\t")
        writer.writeheader()
        for result in results:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, list) else v
                             for k, v in result.items()})
    print(f"Saved {OUTPUT_PATH}")
else:
    print("No results to save.")
