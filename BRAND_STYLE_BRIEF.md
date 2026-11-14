# Brand & style brief — matthewhester.com

_Local planning only; not rendered into `_site/`._
_First written 2026-05-23 (Phase 4A). Revised 2026-11-13, when the look was
made sharp and simple: section 0 is new, and sections 2, 4, 5 and 6 changed._

The Phase 3 site already established a coherent visual identity: stone,
crystal, and climbing, treated like a geology field notebook. This brief
formalizes that identity, derives a palette and type system around it,
and defines how the image assets (portrait, course artwork) should be
treated.

Source of truth for color tokens is the `:root` block in `styles.css`.
This document explains the _why_; the CSS is the _what_.

## 0. The look, in five rules

Matt, 2026-11-13: "i like sharp and simple". The first version of the site
was softer: a stone-tinted page, 8 px rounded cards with shadows, pill
tags, and colored card edges. The revision keeps the identity and takes
those away.

1. **One accent.** Iron marks links, hovers, and the current page, and
   nothing else.
2. **One paper tone.** The page is white. Blocks are separated by rules
   and space, not by boxes, fills, shadows, or rounded corners.
3. **One column.** Every hub page sits in the same 800 px column with its
   title on the same left edge, and the navbar and footer share that
   edge. No page has a sidebar or an "On this page" list.
4. **Square and flat.** Tags and inline code have a 2 px radius. Every
   other edge is square, and nothing lifts on hover.
5. **Links look like links.** In running text they are underlined.

The portrait and the course artwork carry the color. The page around them
stays plain. When in doubt, remove before adding.

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

The palette is encoded in `styles.css` as named tokens. Hex values should
be tuned in CSS rather than re-anchored here.

| Token              | Hex      | Role                                    |
| ------------------ | -------- | --------------------------------------- |
| `--paper`          | `#ffffff`| The page, and everything set on it      |
| `--stone-50`       | `#f6f5f3`| Quartz dust — navbar text, quiet plates |
| `--stone-100`      | `#ecebe7`| Limestone — panels: code, tags, quotes  |
| `--stone-200`      | `#d8d6d0`| Weathered granite — hairlines, borders  |
| `--stone-400`      | `#8a8780`| Basalt — rules and marks only, never text |
| `--stone-500`      | `#6b6862`| Shale — muted text, captions            |
| `--stone-700`      | `#3a3935`| Slate — body text                       |
| `--stone-900`      | `#1c1b19`| Obsidian — headings, navbar, firm rules |
| `--iron-accent`    | `#8a4a2b`| Weathered bolt / rust — the one accent  |

**Rules of thumb:**

- Iron is the only accent. It is the link and hover color, and it marks
  the current page in a course site's sidebar and contents list. The hub
  navbar marks the current page in the bar's own light tone instead,
  because iron on the navbar's black is too faint (see section 6).
- `--crystal-blue` and `--moss-quiet` were removed on 2026-11-13. Quote
  and code edges, focus rings, and the navbar hairline that used them are
  grey, black, or light.
- Resist adding additional accents. The restraint is the design.
- Possible future addition: a `--clay` or `--rust` warmer variant for
  illustration accents — only if needed for a specific image treatment.
  Do not introduce speculatively.
- The course sites carry the same tokens in their own stylesheets, plus
  one shared block (headed SHARP AND SIMPLE) that applies these rules
  there: callouts in grey, with an iron edge kept for important, warning,
  and caution. Change that block in every course site or in none.

## 3. Typography

Already wired in `_quarto.yml`:

- **Body:** Inter (system-ui fallback). Clean, neutral, modern sans;
  reads well at the slightly larger base size (`1.05em`).
- **Headings:** Same Inter, weight 600, slightly tighter letter-spacing.
  A linked heading or caption keeps that weight; the theme's own link
  weight is 400.
- **Code:** JetBrains Mono (Consolas / Menlo fallback). Distinctive
  enough to read as "this is code" without being a costume.

**Do not:**

- Introduce a decorative display font (serif slab, hand-drawn, etc.).
- Load multiple weights for visual variety; the existing single weight
  works because the layout is restrained.
- Add Google Fonts via `<link>`; if we ever load a webfont we'll vendor
  it. For now, Inter is left to system rendering where available, with
  graceful sans-serif fallback otherwise. A visitor without Inter or
  JetBrains Mono installed sees the fallbacks (Segoe UI and Consolas on
  Windows).

If a future cover/landing redesign genuinely wants a serif/slab heading,
candidates worth testing: Source Serif, Spectral, or Inter Display. Test
before committing.

## 4. Image treatment

Four image roles. Each has its own treatment.

### Portrait — homepage
- Stylized illustration of Matt Hester. The source is staged in
  `assets/images/raw/` and gitignored there.
- Lives in `assets/images/brand/` as
  `portrait-matt-hester-800.{webp,jpg}` (800px wide, native portrait
  aspect preserved), written by `tools/make_portrait.py`.
- Sits beside the name at the top of the homepage, 250 px wide on a wide
  screen, set straight on the page with no card; not full-bleed.
- Because there is no card, the paper in the picture has to be the
  page's white. The tool moves the white point so the ground is 255
  throughout. Rerun it if the source art changes.
- Alt text in use: "Stylized illustrated portrait of Matt Hester."

### Course artwork — posters and marks
- Each course has one poster: a 4:3 field with a crystal or object in the
  middle and typeset panels at the sides. It appears whole on the
  course's own landing page, capped at 560 px, and as a card on the
  homepage and the Teaching page.
- The course mark is the poster's central object, cut out on
  transparency. A course site shows it in its navbar and as its favicon.
  The Course Library shows it beside each record, 80 px wide and 56 px on
  a phone.
- Marks shown together are drawn alike. `tools/make_library_marks.py`
  trims each mark to its object, gives every object the same optical
  size on the same centre, and writes exact pixel sizes for 1x, 2x and 3x
  screens. Do the same for any new set of images shown in a row or a
  column: marks that are only shrunk come out uneven and soft.
- The posters and the portrait are the identity pieces. Contain them; do
  not remove them.

### Favicon
- `assets/images/brand/favicon.png`, 96×96: the initials MH, light on the
  navbar's black. `tools/make_favicon.py` draws it from rectangles and
  parallelograms, not from a font, so it is square-edged at 16 px.
- Each course site uses its own course mark as its favicon.

### Boulder motifs — section / course cards
- Not in use as of 2026-11-13: the homepage section links are text-only
  and the course cards carry posters. The treatment below stands if a
  motif is ever chosen for a card.
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
- A frame, card, shadow, or rounded corner around an image.

## 5. Layout principles

- **One column.** 800 px, the same on every hub page, with the navbar and
  footer on its edges. A course site has its own wider frame with a
  sidebar and a contents list, and its navbar and footer sit on that
  frame's edges.
- **Strong landing hero, not enormous.** The name and role in the title
  block, one short statement under them, and the portrait to the right,
  starting level with the name. On a phone it reads name, portrait,
  statement. No buttons in the hero: the navbar and the section links
  below do that job.
- **Three section links** below the hero: Teaching · Research · Governed
  courseware. Text only, each under a rule. Each is a real link to a page
  that exists.
- **Featured course sites** as a separate visually-distinct block, not
  mixed with the section links. This signals "these are external public
  course sites" rather than "these are sections of this site."
- **Limited nav.** 7 items is the absolute ceiling; 5–6 preferred. Current
  navbar: About · Teaching · Courses · Research · CV · Contact. The site
  name at the left is the home link.
- **Less copy above the content.** A page should not explain how to read
  itself. If a control needs a paragraph of instructions, simplify the
  control.
- **Mobile-first.** Test at 360px (small phone), 768px (tablet), and
  1280px (typical desktop). No page should scroll sideways at any of
  them, and the hero must collapse cleanly.
- **No dead components.** If a section has no real content yet, mark
  the page as a polished placeholder; don't fake density with filler.

## 6. Accessibility

- **Alt text on every image.** No `alt=""` unless the image is purely
  decorative and conveys no information beyond what's in adjacent text.
- **Contrast.** Measured against WCAG's 4.5:1 for text. On white: body
  text (`--stone-700`) 11.6:1, muted text (`--stone-500`) 5.5:1, links
  (`--iron-accent`) 6.8:1. `--stone-400` is 3.6:1 on white, so it is for
  rules and marks and never for text. Iron on the navbar's black is
  2.5:1, so the navbar does not use it. Re-check if any color is changed.
- **Links are not marked by color alone.** In running text they are
  underlined.
- **Responsive images.** Use Quarto's image handling or simple `<img>`
  with explicit width; do not embed raw 4000px photos.
- **Keyboard navigation.** The default Quarto navbar is keyboard-friendly;
  do not add custom JS that breaks tab order.
- **No text baked into images.** Names, titles, links must be HTML/CSS,
  not pixels. Exception: a small wordmark/logo SVG with the name set
  in display type is fine, with `alt="Matt Hester"`. The course posters
  carry their titles in the artwork, so each one sits beside the same
  title as text and carries alt text.
