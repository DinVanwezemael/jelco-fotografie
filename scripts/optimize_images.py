#!/usr/bin/env python3
"""Resize and re-compress oversized images in the working tree before Jekyll builds.

Photos reach this repo through two authoring pipelines (see CLAUDE.md): folder-based
projects under assets/projects/, and CMS uploads under assets/cms-projects/ that arrive
straight from a phone via the GitHub API. The CMS path has no opportunity to run a local
tool, so image weight can only be enforced at build time — that is why this runs in the
Actions workflow rather than as something an author remembers to invoke.

It rewrites files IN PLACE in the working tree. That is safe in CI because the checkout is
ephemeral: the full-resolution originals stay untouched in git, and only the published
_site output carries the web-sized copies. Run it locally only against a scratch copy.
"""

import argparse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
TARGET_DIRS = ("assets/projects", "assets/cms-projects", "assets/images")
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

MAX_LONG_EDGE = 2000
JPEG_QUALITY = 82
WEBP_QUALITY = 82

# Files at or below this size that also fit within MAX_LONG_EDGE are left alone, so we
# never re-encode something already fine and lose a generation of quality to no purpose.
SIZE_THRESHOLD = 400 * 1024

# A rewrite that saves less than this fraction isn't worth the quality loss, so we discard
# it and keep the original bytes. This is what makes repeated runs idempotent.
MIN_SAVING_RATIO = 0.05


def human(size: int) -> str:
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"

    return f"{size / 1024:.0f} KB"


def iter_images():
    for target in TARGET_DIRS:
        directory = ROOT / target

        if not directory.exists():
            continue

        for path in sorted(directory.rglob("*")):
            if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
                yield path


def save_variant(image: Image.Image, path: Path, destination: Path) -> None:
    """Write `image` to `destination` in `path`'s existing format, dropping EXIF."""
    suffix = path.suffix.lower()

    if suffix in (".jpg", ".jpeg"):
        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")

        image.save(destination, "JPEG", quality=JPEG_QUALITY, progressive=True, optimize=True)

    elif suffix == ".png":
        image.save(destination, "PNG", optimize=True)

    else:
        image.save(destination, "WEBP", quality=WEBP_QUALITY, method=6)


def optimize(path: Path, dry_run: bool = False):
    """Rewrite `path` if worthwhile.

    Returns the bytes saved, or None if the file was left untouched. A corrupt or
    unreadable file is warned about and skipped rather than raised — a bad CMS upload
    shouldn't block publishing the entire site.
    """
    original_size = path.stat().st_size
    relative = path.relative_to(ROOT).as_posix()
    temp_path = path.with_suffix(path.suffix + ".tmp")

    try:
        with Image.open(path) as image:
            image.load()

            # Re-encoding an animated file would silently flatten it to one frame.
            if getattr(image, "n_frames", 1) > 1:
                print(f"WARNING: {relative} is animated — skipping, not flattening it.")
                return None

            long_edge = max(image.size)
            needs_resize = long_edge > MAX_LONG_EDGE

            if not needs_resize and original_size <= SIZE_THRESHOLD:
                return None

            if needs_resize:
                scale = MAX_LONG_EDGE / long_edge
                new_size = (
                    max(1, round(image.width * scale)),
                    max(1, round(image.height * scale)),
                )
                image = image.resize(new_size, Image.Resampling.LANCZOS)

            save_variant(image, path, temp_path)

    except (OSError, ValueError) as error:
        temp_path.unlink(missing_ok=True)
        print(f"WARNING: could not optimize {relative} ({error}) — leaving it as is.")

        return None

    new_size_bytes = temp_path.stat().st_size

    # Keep the original unless the rewrite is a real improvement. A resize always counts,
    # since it also changes the pixel dimensions we're targeting.
    if not needs_resize and new_size_bytes > original_size * (1 - MIN_SAVING_RATIO):
        temp_path.unlink()

        return None

    if dry_run:
        temp_path.unlink()
    else:
        temp_path.replace(path)

    prefix = "Would optimize" if dry_run else "Optimized"
    print(f"{prefix} {relative}: {human(original_size)} -> {human(new_size_bytes)}")

    return original_size - new_size_bytes


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resize and re-compress oversized images in the working tree."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report what would change without modifying any file",
    )
    args = parser.parse_args()

    total_saved = 0
    changed = 0

    for path in iter_images():
        saved = optimize(path, dry_run=args.dry_run)

        if saved is None:
            continue

        total_saved += saved
        changed += 1

    if changed:
        verb = "Would optimize" if args.dry_run else "Optimized"
        print(f"{verb} {changed} image(s), saving {human(total_saved)}.")
    else:
        print("No images needed optimizing.")


if __name__ == "__main__":
    main()
