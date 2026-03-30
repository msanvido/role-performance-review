#!/usr/bin/env python3
"""
Packages a skill folder into a distributable .skill file (zip format).

Usage:
    python scripts/package_skill.py [skill-folder] [output-dir]

Defaults:
    skill-folder  — current directory (i.e. the repo root)
    output-dir    — current directory

Example (run from repo root):
    python scripts/package_skill.py
    python scripts/package_skill.py . dist/
"""

import fnmatch
import re
import sys
import zipfile
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ PyYAML is required: pip install pyyaml")
    sys.exit(1)

EXCLUDE_DIRS = {"__pycache__", "node_modules", ".git", ".github", "scripts", "evals"}
EXCLUDE_FILES = {".DS_Store"}
EXCLUDE_GLOBS = {"*.pyc"}


def should_exclude(rel_path: Path) -> bool:
    parts = rel_path.parts
    if any(part in EXCLUDE_DIRS for part in parts):
        return True
    if rel_path.name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(rel_path.name, pat) for pat in EXCLUDE_GLOBS)


def validate(skill_path: Path):
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found in SKILL.md"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        return False, f"Invalid YAML: {e}"

    if not isinstance(fm, dict):
        return False, "Frontmatter must be a YAML dict"

    allowed = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
    unexpected = set(fm.keys()) - allowed
    if unexpected:
        return False, f"Unexpected frontmatter keys: {', '.join(sorted(unexpected))}"

    for required in ("name", "description"):
        if required not in fm:
            return False, f"Missing '{required}' in frontmatter"

    name = fm["name"].strip()
    if not re.match(r"^[a-z0-9-]+$", name):
        return False, f"Name '{name}' must be kebab-case"
    if len(name) > 64:
        return False, f"Name too long ({len(name)} chars, max 64)"

    desc = fm["description"].strip()
    if len(desc) > 1024:
        return False, f"Description too long ({len(desc)} chars, max 1024)"
    if "<" in desc or ">" in desc:
        return False, "Description cannot contain angle brackets"

    return True, fm["name"]


def package(skill_path: Path, output_dir: Path):
    print(f"📦 Packaging: {skill_path}")

    valid, result = validate(skill_path)
    if not valid:
        print(f"❌ Validation failed: {result}")
        sys.exit(1)

    skill_name = result
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"{skill_name}.skill"

    with zipfile.ZipFile(out_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(skill_path.rglob("*")):
            if not file_path.is_file():
                continue
            rel = file_path.relative_to(skill_path.parent)
            if should_exclude(rel):
                continue
            zf.write(file_path, rel)
            print(f"  + {rel}")

    print(f"\n✅ Created: {out_file}")
    return out_file


if __name__ == "__main__":
    skill_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    output_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path.cwd()
    package(skill_path, output_dir)
