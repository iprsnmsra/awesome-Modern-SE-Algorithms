#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
OUTPUT_FILE = DOCS_DIR / "site-data.json"

CODE_EXTENSIONS = {
    ".py": "Python",
    ".ts": "TypeScript",
    ".cpp": "C++",
    ".java": "Java",
    ".cs": "C#",
}

README_CANDIDATES = ["README.md", "Readme.md", "readme.md"]
EXCLUDED_TOP_LEVEL = {".git", ".github", "docs", "scripts", "node_modules"}


def prettify_name(raw: str) -> str:
    return raw.replace("-", " ").replace("_", " ").strip()


def get_readme_text(directory: Path) -> str:
    for name in README_CANDIDATES:
        readme_file = directory / name
        if readme_file.exists():
            return readme_file.read_text(encoding="utf-8", errors="ignore").strip()
    return "No README explanation yet for this algorithm."


def is_algorithm_dir(directory: Path) -> bool:
    if not directory.is_dir():
        return False
    for item in directory.iterdir():
        if item.is_file() and item.suffix.lower() in CODE_EXTENSIONS:
            return True
    return False


def collect_algorithm_data(top_level_dir: Path) -> list[dict]:
    algorithms: list[dict] = []

    for current_dir in sorted(top_level_dir.rglob("*")):
        if not is_algorithm_dir(current_dir):
            continue

        code_files = []
        for code_file in sorted(current_dir.iterdir()):
            if not code_file.is_file() or code_file.suffix.lower() not in CODE_EXTENSIONS:
                continue

            code_files.append(
                {
                    "name": code_file.name,
                    "language": CODE_EXTENSIONS[code_file.suffix.lower()],
                    "content": code_file.read_text(encoding="utf-8", errors="ignore"),
                }
            )

        if not code_files:
            continue

        relative_path = str(current_dir.relative_to(REPO_ROOT)).replace("\\", "/")
        algorithms.append(
            {
                "id": relative_path.replace("/", "-"),
                "title": prettify_name(current_dir.name),
                "path": relative_path,
                "explanation": get_readme_text(current_dir),
                "codeFiles": code_files,
            }
        )

    return algorithms


def build_site_data() -> dict:
    categories = []

    for entry in sorted(REPO_ROOT.iterdir()):
        if not entry.is_dir() or entry.name in EXCLUDED_TOP_LEVEL:
            continue

        algorithms = collect_algorithm_data(entry)
        if not algorithms:
            continue

        categories.append(
            {
                "id": entry.name,
                "title": prettify_name(entry.name),
                "algorithmCount": len(algorithms),
                "algorithms": algorithms,
            }
        )

    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "repository": "iprsnmsra/awesome-Modern-SE-Algorithms",
        "categories": categories,
    }


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    data = build_site_data()
    OUTPUT_FILE.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"Generated {OUTPUT_FILE} with {sum(c['algorithmCount'] for c in data['categories'])} algorithms.")


if __name__ == "__main__":
    main()
