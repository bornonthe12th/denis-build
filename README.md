# denis.zone

Personal website for Denis Martins: https://denis.zone/

A static site with no build step. Each page is a single HTML file with its own inline CSS and JavaScript.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Homepage: hero terminal, selected work (Word Duel demo, timer game), notes list, personal section, contact |
| `experience.html` | Career timeline |
| `about.html` | The non-technical side, with photos |
| `notes/*.html` | Articles, one file per note |
| `assets/photos/` | Photos used on the About page |
| `assets/og-*.svg` / `.png` | Link preview images (the PNGs are generated, see below) |
| `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png` | Site icons |
| `sitemap.xml`, `robots.txt` | For search engines |

## Preview locally

Pages use root-absolute paths (`/assets/...`, `/about.html`), so serve the folder rather than opening files directly:

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000/.

## Deploy

Cloudflare serves the repo root as static assets, configured in `wrangler.jsonc`. There is no build command. The site is published from `main`.

## Link preview images

Each `assets/og-<name>.svg` is the source for a 1200×630 preview image. On push to `main`, the `Build social preview PNGs` workflow renders every SVG to a matching PNG and commits it. Edit the SVG, not the PNG. Pull after pushing, because the workflow adds a commit.

A new page needs its own SVG, plus `og:image` and `twitter:*` meta tags pointing at `https://denis.zone/assets/og-<name>.png`.

## Conventions

- **Shared header and footer.** Every page has the same `.site-header` and `.site-footer` markup, and the same `.site-*` rules in its CSS (in the base section and the 767px block). There is no shared stylesheet, so a change to either means editing all seven pages. The current page's nav link gets `aria-current="page"`.
- **One rule per selector per breakpoint.** Each page's CSS has base rules first, then one `@media` block per breakpoint (widest first), then `prefers-reduced-motion`. Add to the existing block rather than appending new override layers at the end.
- **Containers.** `.wrap` is 1190px wide with 48px side padding, and 20px on screens up to 767px. It sets side padding only, so sections that share the class can set their own top and bottom padding.
- **Breakpoints.** The main layout switch is at 767px/768px. The homepage also has smaller tweaks at 980, 900, 800, 600, 550, 410 and 380px.
- **Colours.** Dark background `#171a19`, text `#edece4`, green accent `#b0c69a`, orange accent `#dda980`, lines `#363e38`.

## Adding a note

1. Copy an existing file in `notes/` and replace the content and meta tags.
2. Add `assets/og-<slug>.svg` for its preview image.
3. Add it to the notes list in `index.html` and to `sitemap.xml`.
