# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Avid Pixels is a photography portfolio site built with Hugo static site generator. It showcases travel photography organized into albums with a clean, minimalist design.

## Build Commands

- `npm run build` - Build the Hugo site (outputs to `public/`)
- `npm run build:preview` - Build with drafts and future-dated content
- `npm run server` - Start Hugo development server with live reload

Hugo processes SASS files automatically through its asset pipeline with PostCSS and autoprefixer.

## Architecture

### Content Structure

**Albums** are the primary content type in this site:
- Located in `content/albums/`
- Each album is a markdown file with frontmatter containing:
  - `title`, `date`, `thumbnail` (path to album cover)
  - `images` array: each image has `title`, `description`, `path_original`, `path_medium`, `width`, `height`
- Album images are stored in `static/albums/{album-name}/` with two sizes: `original/` and `medium/`

### Hugo Template Hierarchy

- `layouts/_default/baseof.html` - Base template with navigation, wrapper, footer
- `layouts/index.html` - Homepage displays album grid
- `layouts/albums/single.html` - Individual album page template
- `layouts/albums/list.html` - Album listing page
- `layouts/partials/site/` - Reusable components:
  - `nav.html` - Fixed navigation bar with scroll detection
  - `scripts.html` - JavaScript for scroll behavior (adds `.scrolled` class at 50px)
  - `social-icons.html` - Social media links rendered from menu config
  - `styles.html` - CSS asset compilation

### Styling Architecture

- CSS framework: Skeleton.css for responsive grid
- Custom styles: `assets/sass/app.scss` compiled by Hugo
- Key SASS structure:
  - Variables for colors and fonts at top
  - `.main-nav` - Fixed navigation with `.scrolled` state (background, padding, shadow changes)
  - `.album-grid` - 2-column grid for album thumbnails (responsive to 1-column)
  - `.album-photos` - Individual album photo layout with 130% width breakout on desktop
  - Responsive breakpoints: 960px, 640px, 480px

### Configuration

- `config/_default/config.yaml` - Site settings, params, markup config
- `config/_default/menus.yaml` - Social media links with inline SVG icons
- Main sections set to `albums` for homepage content filtering

### Navigation Behavior

The navigation uses JavaScript scroll detection:
- Transparent background at top
- White background with shadow when scrolled past 50px
- Implemented in `layouts/partials/site/scripts.html`

### Static Assets

- Photos stored in `static/albums/{album}/original/` and `static/albums/{album}/medium/`
- Each album requires an `album_thumb.jpg` for grid display
- Other static assets in `static/assets/img/`

## Adding New Albums

1. Create markdown file in `content/albums/{album-name}.md`
2. Add frontmatter with title, date, thumbnail path
3. Add images array with metadata (use `_misc/_file_lister.py` to help generate image metadata)
4. Place photos in `static/albums/{album-name}/original/` and `static/albums/{album-name}/medium/`
5. Create `album_thumb.jpg` in `static/albums/{album-name}/`
