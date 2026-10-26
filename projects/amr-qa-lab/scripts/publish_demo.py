"""Copy reproducible reports into the static portfolio demo."""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT.parents[1] / "docs" / "projects" / "amr-qa-lab" / "data"
TARGET.mkdir(parents=True, exist_ok=True)
for filename in ("latest.json", "mutations.json"):
    shutil.copyfile(ROOT / "results" / filename, TARGET / filename)
print(f"Copied QA reports to {TARGET}")
