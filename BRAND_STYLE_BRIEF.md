# Brand & style brief — matthewhester.com

_Phase 4A. Local planning only; not rendered into `_site/`._
_Last updated: 2026-05-23._

The Phase 3 site already established a coherent visual identity: stone,
crystal, and climbing, treated like a geology field notebook. This brief
formalizes that identity, derives a palette and type system around it,
and defines how the new image assets (portrait, boulder motifs) should be
treated.

Source of truth for color tokens is the `:root` block in `styles.css`.
This document explains the _why_; the CSS is the _what_.

## 1. Visual identity

**"Mathematical software + statistics + open teaching + rock / route /
problem-solving imagery."**

- Professional academic, not outdoor influencer.
- Closer to a monograph or working notebook than a marketing site.
- The boulder motif is a signature, not a theme: small, repeated, never
  the loudest element on a page.
- Spiritually similar to the way some R books (Wickham, Healy, etc.) use
  a single distinctive species or object as a visual signature.

Metaphor inventory (use sparingly, never all at once):

- Mathematical structure (lattices, faces, joints)
- Friction and contact (grip, weight transfer, hold quality)
- Routes and problem-solving (sequences, beta, falling and trying again)
- Landscape and exposure (ridgelines, drone perspective, weather)
- Technical movement (small, precise, repeatable)
- Exploration (going to look, finding nothing, going again)

These are reference vocabulary for image selection and short copy. They
are _not_ analogies to overuse in body text.

## 2. Color palette

The palette is already encoded in `styles.css` as named tokens. Hex
values are approximate and should be tuned in CSS rather than
re-anchored here.

| Token              | Hex      | Role                                    |
| ------------------ | -------- | --------------------------------------- |
| `--stone-50`       | `#f6f5f3`| Quartz dust — page background           |
| `--stone-100`      | `#ecebe7`| Limestone — card / hero backgrounds     |
| `--stone-200`      | `#d8d6d0`| Weathered granite — soft borders        |
| `--stone-400`      | `#8a8780`| Basalt — muted text, captions           |
| `--stone-700`      | `#3a3935`| Slate — body text                       |
| `--stone-900`      | `#1c1b19`| Obsidian — headings, navbar             |
| `--crystal-blue`   | `#5b7a8c`| Oxidized copper / glacial ice — quiet accent |
| `--iron-accent`    | `#8a4a2b`| Weathered bolt / rust — primary accent  |
| `--moss-quiet`     | `#6b7a5a`| Lichen — callouts only                  |

**Rules of thumb:**

- Use one accent at a time. `--iron-accent` is the primary link / hover
  color. `--crystal-blue` is the navbar hairline and hero edge.
  `--moss-quiet` is for callout/blockquote left rules only.
- Resist adding additional accents. The restraint is the design.
- Possible future addition: a `--clay` or `--rust` warmer variant for
  illustration accents — only if needed for a specific image treatment.
  Do not introduce speculatively.

## 3. Typography

Already wired in `_quarto.yml`:

- **Body:** Inter (system-ui fallback). Clean, neutral, modern sans;
  reads well at the slightly larger base size (`1.05em`).
- **Headings:** Same Inter, weight 600, slightly tighter letter-spacing.
- **Code:** JetBrains Mono (Consolas / Menlo fallback). Distinctive
  enough to read as "this is code" without being a costume.

**Do not:**

- Introduce a decorative display font (serif slab, hand-drawn, etc.).
- Load multiple weights for visual variety; the existing single weight
  works because the layout is restrained.
- Add Google Fonts via `<link>`; if we ever load a webfont we'll vendor
  it. For now, Inter is left to system rendering where available, with
  graceful sans-serif fallback otherwise.

If a future cover/landing redesign genuinely wants a serif/slab heading,
candidates worth testing: Source Serif, Spectral, or Inter Display. Test
before committing.

## 4. Image treatment

Three image roles. Each has its own treatment.

### Portrait — homepage hero
- Stylized illustration of Matt Hester. Source:
  `D:/My Drive Personal/Personal/Hester_profile_art.png` (re-staged
  in `assets/images/raw/` and gitignored there).
- Lives in `assets/images/brand/` after processing as
  `portrait-matt-hester-800.{webp,jpg}` (800px wide, native portrait
  aspect preserved).
- Sits in the right half of the split hero, below the title block;
  not full-bleed.
- Alt text in use: "Stylized illustrated portrait of Matt Hester."

### Boulder motifs — section / course cards
- Stylized versions of selected images from
  `D:/My Drive Personal/Climbing/Favorite Photos/`.
- Lives in `assets/images/course-motifs/` (course-specific) or
  `assets/images/processed/` (general motifs).
- ~400–600px wide, 16:9 or 3:2 landscape crop, plus a square 600px
  thumbnail for card display.
- Possible future treatments: duotone using `--stone-700` + `--stone-50`,
  vector trace, or single-color illustration. The Phase 4A baseline is
  EXIF-stripped optimized JPEG/WebP, no duotone yet.
- Alt text: short, descriptive, location-agnostic — e.g. "Textured
  sandstone face with quartz vein," not "Alum Creek roof problem."

### Avoid
- Huge full-screen heroes with overlaid text. Lustig's site uses one,
  the user explicitly does not want it. Stick to the split hero.
- Photo galleries / lightboxes / carousels.
- Images that incidentally identify other climbers or landowners.

## 5. Layout principles

- **Strong landing hero, not enormous.** Split layout: name + role +
  one-paragraph statement + 2–3 buttons on the left; portrait on the
  right. Collapses to single-column on mobile with portrait above text.
- **Clear category cards** below the hero: Teaching · Research ·
  Resources. Each is a real link to a page that exists.
- **Featured course sites** as a separate visually-distinct block, not
  mixed with category cards. This signals "these are external public
  course sites" rather than "these are sections of this site."
- **Limited nav.** 7 items is the absolute ceiling; 5–6 preferred. Current
  navbar: Home · About · Teaching · Research · Resources · CV · Contact.
- **Mobile-first.** Test at 360px (small phone), 768px (tablet), and
  1280px (typical desktop). The split hero must collapse cleanly.
- **No dead components.** If a section has no real content yet, mark
  the page as a polished placeholder; don't fake density with filler.

## 6. Accessibility

- **Alt text on every image.** No `alt=""` unless the image is purely
  decorative and conveys no information beyond what's in adjacent text.
- **Contrast.** Body text (`--stone-700` on `--stone-50`) passes WCAG
  AA; accent (`--iron-accent`) on stone-50 also passes. Re-check if any
  color is changed.
- **Responsive images.** Use Quarto's image handling or simple `<img>`
  with explicit width; do not embed raw 4000px photos.
- **Keyboard navigation.** The default Quarto navbar is keyboard-friendly;
  do not add custom JS that breaks tab order.
- **No text baked into images.** Names, titles, links must be HTML/CSS,
  not pixels. Exception: a small wordmark/logo SVG with the name set
  in display type is fine, with `alt="Matt Hester"`.
