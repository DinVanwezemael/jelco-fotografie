#!/usr/bin/env python3
"""Regenerate _projects/*.md from assets/projects/<project-name>/ folders.

This script only ever creates, updates, or deletes files it marked itself
(via the `source_folder` front-matter key). Projects authored through the
CMS (assets/cms-projects/, front matter with no `source_folder` key) are
never touched, so the two authoring pipelines can safely coexist.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "assets" / "projects"
OUTPUT_DIR = ROOT / "_projects"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".svg"}
MARKER_KEY = "source_folder"


def slugify(name: str) -> str:
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def is_script_managed(path: Path) -> bool:
    """True only for files this script generated (carry the source_folder marker)."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    front_matter = text[3:end] if end != -1 else text[3:]
    return re.search(rf'^{MARKER_KEY}:', front_matter, re.MULTILINE) is not None


def parse_project_info(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = ""
    fields = {}
    i = 0

    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        i = 1

    while i < len(lines) and lines[i].strip():
        match = re.match(r"^([^:]+):\s*(.*)$", lines[i])
        if match:
            key = match.group(1).strip().lower()
            fields[key] = match.group(2).strip()
            i += 1
        else:
            break

    while i < len(lines) and not lines[i].strip():
        i += 1

    body_lines = lines[i:]
    body = "\n".join(body_lines).strip()

    return {"title": title, "fields": fields, "body": body}


def yaml_escape(value: str) -> str:
    return value.replace('"', '\\"')


def build_front_matter(name: str, info: dict, images: list, source_folder: str) -> str:
    title = info["title"] or name
    fields = info["fields"]

    lines = ["---", "layout: project", f'title: "{yaml_escape(title)}"']

    for key in ("categorie", "locatie", "datum", "samenvatting"):
        if key in fields:
            lines.append(f'{key}: "{yaml_escape(fields[key])}"')

    if "samenvatting" in fields:
        lines.append(f'description: "{yaml_escape(fields["samenvatting"])}"')

    featured = fields.get("uitgelicht", "").strip().lower() in ("ja", "yes", "true", "1")
    lines.append(f'uitgelicht: {"true" if featured else "false"}')
    lines.append(f'{MARKER_KEY}: "{yaml_escape(source_folder)}"')

    lines.append("images:")
    for image in images:
        lines.append(f'  - "{image}"')

    lines.append("---")
    return "\n".join(lines)


def generate() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    expected_slugs = set()

    if SOURCE_DIR.exists():
        for project_dir in sorted(SOURCE_DIR.iterdir()):
            if not project_dir.is_dir() or project_dir.name.startswith("_"):
                continue

            images = sorted(
                f.name for f in project_dir.iterdir()
                if f.suffix.lower() in IMAGE_EXTS
            )
            if not images:
                continue

            slug = slugify(project_dir.name)
            expected_slugs.add(slug)
            out_path = OUTPUT_DIR / f"{slug}.md"

            if out_path.exists() and not is_script_managed(out_path):
                print(
                    f"WARNING: '{slug}' collides with a non-script file "
                    f"(likely CMS-authored) — skipping, not overwriting."
                )
                continue

            rel_dir = f"/assets/projects/{project_dir.name}"
            image_paths = [f"{rel_dir}/{img}" for img in images]

            info_path = project_dir / "ProjectInfo.md"
            info = parse_project_info(info_path) if info_path.exists() else {
                "title": "", "fields": {}, "body": ""
            }

            front_matter = build_front_matter(project_dir.name, info, image_paths, project_dir.name)
            content = f"{front_matter}\n\n{info['body']}\n"

            out_path.write_text(content, encoding="utf-8")
            print(f"Generated _projects/{slug}.md")

    # Clean up stale script-generated files whose source folder was removed.
    # Never touch files without our marker (CMS-authored or hand-authored).
    for existing in OUTPUT_DIR.glob("*.md"):
        if existing.stem in expected_slugs:
            continue
        if is_script_managed(existing):
            existing.unlink()
            print(f"Removed stale _projects/{existing.stem}.md (source folder gone)")


if __name__ == "__main__":
    generate()
