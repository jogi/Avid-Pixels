# Avid Pixels

A photography portfolio site built with Hugo, showcasing travel photography organized into albums.

## Development

### Requirements

- Hugo Extended v0.152.2 or later
- Node.js (for PostCSS processing)

### Local Development

```bash
# Install dependencies
npm install

# Start development server
npm run server

# Build for production
npm run build
```

The site will be available at `http://localhost:1313/`

## Structure

- `content/albums/` - Album markdown files with image metadata
- `layouts/` - Hugo templates and partials
- `static/albums/` - Photo files (original and medium sizes)
- `assets/sass/` - SASS stylesheets compiled by Hugo

## Deployment

The site automatically deploys to GitHub Pages via GitHub Actions when changes are pushed to the `main` branch.

Live site: https://jogi.github.io/Avid-Pixels/

## Adding Albums

1. Create a markdown file in `content/albums/` with frontmatter containing title, date, thumbnail, and images array
2. Add photos to `static/albums/{album-name}/` in `original/` and `medium/` directories
3. Include an `album_thumb.jpg` for the grid view

See existing album files for reference.
