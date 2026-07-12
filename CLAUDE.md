# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Static Jekyll website for **Jelco Fotografie**, a Belgian photographer specializing in automotive, motorsport, architecture, and interior photography, plus print sales. Hosted on GitHub Pages at `https://jelcofotografie.be`. The site is in Dutch (nl-BE).

Portfolio is organized into five fixed categories, each with its own nav link and listing page at `/projecten/<slug>/`: Automotive, Motorsport, Architectuur, Interieur, Prints. A project's `Categorie` field in `ProjectInfo.md` must exactly match one of these five values (case-sensitive) to appear on its category page — otherwise it's only visible on the general `/projecten/` overview.

## Commands

Requires Ruby ≥ 3.0 (matches CI's Ruby 3.2). macOS system Ruby is often older — install via `brew install ruby@3.2` and prepend `/opt/homebrew/opt/ruby@3.2/bin` to `PATH` if `bundle install` fails with native extension errors.

```bash
# Install dependencies (first time)
bundle install

# Local development server
bundle exec jekyll serve

# Production build
bundle exec jekyll build

# Regenerate _projects/ from assets/projects/ folders
python3 scripts/generate_projects.py
```

## Architecture

### Project generation pipeline

Projects are **not written by hand**. The flow is:

1. Each project lives as a folder under `assets/projects/<project-name>/` containing images and an optional `ProjectInfo.md`.
2. `scripts/generate_projects.py` reads those folders and writes corresponding `.md` files into `_projects/`.
3. Jekyll then renders the `_projects/` collection into `/projecten/:name/` URLs.

**Never manually edit files in `_projects/`** — they are wiped and regenerated every build (locally and in CI).

### Adding a project

1. Create `assets/projects/<Folder Name>/`
2. Drop images (`.jpg`, `.jpeg`, `.png`, `.webp`, `.svg`) into the folder — the first one alphabetically becomes the cover.
3. Optionally add `ProjectInfo.md` with these fields at the top:

```markdown
# Titel van het project
Categorie: Automotive
Locatie: Gent
Datum: 2026-05-16
Samenvatting: Korte omschrijving van het project.
Uitgelicht: Ja

Langere beschrijving als body...
```

`Categorie` must be one of: `Automotive`, `Motorsport`, `Architectuur`, `Interieur`, `Prints`.

`Uitgelicht` (`Ja`/`Yes`/`True`/`1`, case-insensitive) controls whether the project appears in the "Uitgelicht" section on the homepage — this is a manual curation flag, not automatic (the homepage does **not** just show the most recent projects). Omit it, or set it to anything else, to keep a project off the homepage; it's still reachable via its category page and `/projecten/`.

4. Run `python3 scripts/generate_projects.py` to update `_projects/`.

### Layout hierarchy

- `default.html` — base HTML shell (head, sticky header, footer, mobile nav toggle JS)
- `home.html` → `default.html` — homepage
- `project.html` → `default.html` — project detail with hero, metadata sidebar, auto gallery
- `page.html` → `default.html` — generic content pages
- `projects.html` → `default.html` — project listing page

### Styling

All CSS lives in a single file: `assets/css/style.scss`. No build tool — Jekyll compiles the SCSS directly.

Design system: light "paper" theme (`--bg: #f2ede4`) with a dark olive brand accent (`--accent: #21241c`, sampled from `assets/images/logo.jpg`'s background — also reused as the base `--text` color, so the palette is intentionally near-monochrome cream/olive). Sharp corners throughout (no `border-radius`) and hairline dividers. Fonts are Work Sans (headings/nav/buttons at weight 800, body text at regular/medium) and JetBrains Mono (`.data-strip` class — used for category/location/date metadata styled like burned-in capture data). Elements overlaid on photos (project hero title, card title/tag) use the fixed `--on-image` light color instead of `--text`, since they always sit on a dark photo scrim regardless of page theme — don't invent fake camera EXIF or print-edition numbers here; only real front-matter fields (`categorie`/`locatie`/`datum`) are shown. The header logo (`.logo-mark`) renders `assets/images/logo.jpg` next to the text wordmark. Responsive breakpoints at 980 px (nav collapses to hamburger) and 680 px (grids go single-column).

### CI/CD

GitHub Actions (`.github/workflows/pages.yml`) on push to `main`:
1. Runs `python3 scripts/generate_projects.py`
2. Runs `bundle exec jekyll build`
3. Deploys to GitHub Pages
