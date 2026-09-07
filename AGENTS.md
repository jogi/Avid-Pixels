# AGENTS.md

This file provides guidance for coding agents working in this repository.

## Project Overview

Avid Pixels is a photography portfolio built with Hugo. It showcases travel photography organized into albums with a minimalist design. The site name displayed in navigation is configured as Vashishtha Jogi.

## Build Commands

- `npm run build` - Extract missing EXIF metadata, then build the Hugo site into `public/`.
- `npm run build:preview` - Extract missing EXIF metadata, then build with drafts and future-dated content.
- `npm run server` - Start the Hugo development server with live reload; this does not run EXIF extraction.
- `hugo` - Build directly without running the metadata script. Useful for validating template and style changes without rewriting album content.

Use Hugo Extended for SASS compilation and install the Node dependencies with `npm ci`. Hugo compiles `assets/sass/app.scss` and runs PostCSS with autoprefixer through `layouts/partials/site/styles.html` and `postcss.config.js`.

The EXIF script requires `.venv/bin/python3` with Pillow and PyYAML. It can rewrite album frontmatter when metadata is missing, so inspect content changes after running it. Currently `npm run build` invokes extraction twice: once through npm's `prebuild` lifecycle and once explicitly in the build script. Albums with both `exif` and `exif_all` already populated are skipped.

There is no test script configured in `package.json`. For template/style changes, build with Hugo and inspect the affected homepage and album layouts at desktop and mobile widths.

## Architecture

### Content Structure

- Albums live in `content/albums/` as Markdown files with YAML frontmatter.
- Album fields include `title`, `date`, `thumbnail`, and an `images` array. An album-level `description` is optional.
- Images specify `path_original`, `path_medium`, `width`, and `height`; `title` and `description` may be omitted or empty.
- Optional image `exif` and `exif_all` fields provide the summary and full metadata shown in the camera-settings modal.
- Image paths are site-root paths such as `/albums/alaska/medium/alaska-1.jpg`, backed by files under `static/`.
- General pages include `content/about.md` and `content/gear.md`.

### Hugo Templates

- `layouts/_default/baseof.html` - Base navigation, main wrapper, and footer.
- `layouts/index.html` - Homepage album grid, filtering regular pages directly by `Type == "albums"`.
- `layouts/albums/list.html` - Album section grid.
- `layouts/albums/single.html` - Album heading, photograph sequence, original-image links, and EXIF modals.
- `layouts/_default/single.html` - General content pages.
- `layouts/partials/site/` contains reusable components:
  - `album-thumbnail.html` - Shared responsive cover markup for both album grids.
  - `nav.html` - Fixed navigation markup.
  - `scripts.html` - Scroll detection and EXIF modal interactions.
  - `social-icons.html` - Social links rendered from menu configuration.
  - `styles.html` - CSS compilation and stylesheet links.

### Styling and Interaction

- `assets/css/normalize.css` and `assets/css/skeleton.css` provide base styles and container rules. The album grid itself uses CSS Grid in `assets/sass/app.scss`.
- `app.scss` defines the system font stack, colors, navigation, album layouts, EXIF styles, and automatic dark-mode overrides.
- Navigation and album/photo headings use weight 500; grid captions use weight 400. Their font sizes remain distinct by role. Camera-detail labels use sentence case and untracked lettering.
- `.album-grid` has two columns on desktop and one at widths of 960px or below.
- Album photographs break out of their container at 130% width on desktop, 115% at 960px or below, and 100% at 640px or below. Additional responsive rules exist at 480px.
- Navigation is transparent at the top. Scrolling beyond 50px adds `.scrolled`, changing padding and adding a background and shadow. The background is light or dark according to the color scheme.
- EXIF controls appear on photograph hover on desktop and remain visible at narrower widths or on devices that cannot hover. Modals close through the close button, backdrop click, or Escape.

### Configuration

- `config/_default/config.yaml` - Site settings, parameters, markup, and output configuration.
- `config/_default/menus.yaml` - Social and About links with inline SVG icons.
- `params.mainSections` is set to `albums`, but the homepage template uses its own explicit type filter rather than reading this parameter.

### Static Assets and Covers

- Photos live in `static/albums/{album}/original/` and `static/albums/{album}/medium/`.
- Each album's `thumbnail` points to its cover, conventionally `/albums/{album}/album_thumb.jpg`.
- Responsive covers use an 864px-wide `album_thumb.jpg` plus `album_thumb-1440.jpg` and `album_thumb-2160.jpg` in the same directory. Both larger files must exist for the shared partial to emit `srcset`; otherwise it uses the configured thumbnail alone.
- The partial's `sizes` attribute matches the current grid widths and gutters. Update it if the grid layout changes.
- Eleven albums currently have responsive covers. Yosemite retains its existing cover because the matching source is only 866 × 576 pixels.
- Generate cover variants from a sufficiently large source photograph, preserving the cover composition and aspect ratio. Hugo and the EXIF script do not generate these variants automatically.
- Other image assets live in `static/assets/img/`.

## Adding New Albums

1. Place photographs in `static/albums/{album-name}/original/` and `static/albums/{album-name}/medium/`.
2. Create `content/albums/{album-name}.md` with title, date, thumbnail path, and the image paths and dimensions. Add titles/descriptions where appropriate.
3. Create `album_thumb.jpg`; when a sufficiently large source is available, also export the matching 1440px and 2160px covers described above.
4. Run `.venv/bin/python3 _misc/extract_exif.py` to populate missing camera metadata, and inspect the resulting frontmatter changes.
5. Build and verify the album grid, photograph proportions, original-image links, and camera details.

`_misc/_file_lister.py` is a legacy Python 2 helper with hardcoded paths predating the current `static/` structure. It is not ready to run under the project's Python 3 environment without updating it.
