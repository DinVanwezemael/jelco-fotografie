#!/usr/bin/env python3
"""Regenerate _projects/*.md from assets/projects/<project-name>/ folders."""

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "assets" / "projects"
OUTPUT_DIR = ROOT / "_projects"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".svg"}


def slugify(name: str) -> str:
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def parse_project_info(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = ""
    fields = {}
    body_lines = []
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


def build_front_matter(name: str, info: dict, images: list, cover: str) -> str:
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

    lines.append(f'cover: "{cover}"')
    lines.append("images:")
    for image in images:
        lines.append(f'  - "{image}"')

    lines.append("---")
    return "\n".join(lines)


def generate() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    if not SOURCE_DIR.exists():
        return

    for project_dir in sorted(SOURCE_DIR.iterdir()):
        if not project_dir.is_dir():
            continue

        images = sorted(
            f.name for f in project_dir.iterdir()
            if f.suffix.lower() in IMAGE_EXTS
        )
        if not images:
            continue

        cover = images[0]
        rel_dir = f"/assets/projects/{project_dir.name}"
        image_paths = [f"{rel_dir}/{img}" for img in images]
        cover_path = f"{rel_dir}/{cover}"

        info_path = project_dir / "ProjectInfo.md"
        info = parse_project_info(info_path) if info_path.exists() else {
            "title": "", "fields": {}, "body": ""
        }

        slug = slugify(project_dir.name)
        front_matter = build_front_matter(project_dir.name, info, image_paths, cover_path)
        content = f"{front_matter}\n\n{info['body']}\n"

        (OUTPUT_DIR / f"{slug}.md").write_text(content, encoding="utf-8")
        print(f"Generated _projects/{slug}.md")


if __name__ == "__main__":
    generate()
