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

### Two project-authoring pipelines (both write into `_projects/`)

Projects can be added two independent ways, which coexist safely side by side:

1. **Technical (folder-based):** a project lives as a folder under `assets/projects/<project-name>/` containing images and an optional `ProjectInfo.md`. `scripts/generate_projects.py` reads those folders and writes corresponding `.md` files into `_projects/`.
2. **Non-technical (CMS):** the Sveltia CMS admin panel at `/admin/` (see below) writes directly into `_projects/*.md` with real YAML front matter, and uploads photos to `assets/cms-projects/<slug>/` — a folder namespace kept deliberately separate from `assets/projects/` so the script's folder-scanner never sees or collides with CMS-managed content.

Jekyll renders the `_projects/` collection into `/projecten/:name/` URLs regardless of which pipeline created a given file.

**Safety mechanism:** every file `generate_projects.py` writes carries a `source_folder` front-matter key. The script only ever creates, updates, or deletes files that carry that marker — any file without it (i.e. CMS-authored) is never touched under any circumstances, including when cleaning up stale files after a source folder is removed. If a slug collision is ever detected against a non-marked file, the script skips it and prints a warning instead of overwriting.

**Never manually `rm -rf _projects/` or bulk-delete the directory outside the script.** A plain filesystem delete bypasses the marker safety check entirely and can permanently destroy CMS-authored (git-tracked) projects if you then `git add -A` and commit. Editing/removing an individual *script-generated* file by hand is harmless (it'll just be regenerated/recreated next run) — the risk is specifically in indiscriminate bulk deletion of the whole folder.

**Naming rule:** avoid giving a technical-pipeline project and a CMS-authored project the same title/slug. The marker system stops the script from ever overwriting a CMS file, but nothing stops the CMS from overwriting a script-generated file if the slugs collide (it commits directly via the GitHub API with no knowledge of our marker convention) — whichever pipeline writes second simply wins. This is a documented, accepted edge case rather than something enforced in code, since blocking on it would require a review/approval gate, which conflicts with "publish immediately."

Both pipelines produce the same front-matter schema (`title`, `categorie`, `locatie`, `datum`, `samenvatting`, `uitgelicht`, `images`). There is **no stored `cover` field** — it's derived in Liquid as `page.images | first` wherever needed, so both pipelines only need to get the image order right, never a separate field.

### Adding a project

Fastest way: copy `assets/projects/_TEMPLATE/` (a real folder with a filled-out `ProjectInfo.md` and usage notes in an HTML comment at the bottom), rename the copy, drop in photos, and edit the fields. `_TEMPLATE` itself has no images so `generate_projects.py` skips it, and it's in `_config.yml`'s `exclude` list so it never ends up in the built site.

Manual steps (what the template automates):

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

### CMS admin panel

`/admin/` (`admin/index.html` + `admin/config.yml`) is a [Sveltia CMS](https://github.com/sveltia/sveltia-cms) instance — a hosted, form-based editor so a non-technical person can create/edit/delete projects and upload photos from any device's browser, no git or file editing required. Publishing commits directly to `main` via the GitHub API (no draft/PR step), which triggers the normal `pages.yml` deploy automatically.

It requires a one-time manual setup, since GitHub OAuth needs a confidential client-secret exchange that can't happen purely client-side:

1. Deploy the [`sveltia/sveltia-cms-auth`](https://github.com/sveltia/sveltia-cms-auth) OAuth proxy to a free Cloudflare Worker (`wrangler deploy`).
2. Create a GitHub OAuth App at `github.com/settings/applications/new`, with the Authorization callback URL set to `<worker-url>/callback`.
3. Set `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` (encrypted) / `ALLOWED_DOMAINS` as the Worker's environment variables in the Cloudflare dashboard — never commit these.
4. Update `backend.base_url` in `admin/config.yml` to the real Worker URL (currently a `REPLACE-ME` placeholder).

`admin/` and `assets/cms-projects/` are plain static files/folders — no entries needed in `_config.yml`'s `exclude` list, since they're meant to be included in the built site.

### Layout hierarchy

- `default.html` — base HTML shell (head, sticky header, footer, mobile nav toggle JS)
- `home.html` → `default.html` — homepage
- `project.html` → `default.html` — project detail with hero, metadata sidebar, auto gallery
- `page.html` → `default.html` — generic content pages
- `projects.html` → `default.html` — project listing page

### Styling

All CSS lives in a single file: `assets/css/style.scss`. No build tool — Jekyll compiles the SCSS directly.

Design system: light "paper" theme (`--bg: #f2ede4`) with a dark olive brand accent (`--accent: #21241c`, sampled from `assets/images/logo.jpg`'s background — also reused as the base `--text` color, so the palette is intentionally near-monochrome cream/olive). Buttons, cards, and tag chips are rounded; hairline dividers throughout. Fonts are Work Sans (headings/nav/buttons at weight 800, body text at regular/medium) and JetBrains Mono (`.data-strip` class — used for category/location/date metadata styled like burned-in capture data). Elements overlaid on photos (project hero title, card title/tag) use the fixed `--on-image` light color instead of `--text`, since they always sit on a dark photo scrim regardless of page theme — don't invent fake camera EXIF or print-edition numbers here; only real front-matter fields (`categorie`/`locatie`/`datum`) are shown. The header logo (`.logo-mark`) renders `assets/images/logo.jpg` next to the text wordmark. Responsive breakpoints at 980 px (nav collapses to hamburger) and 680 px (grids go single-column).

### CI/CD

GitHub Actions (`.github/workflows/pages.yml`) on push to `main`:
1. Runs `python3 scripts/generate_projects.py`
2. Runs `bundle exec jekyll build`
3. Deploys to GitHub Pages
