# Course artwork

One poster per course, and the images made from it.

- `<slug>-hero.png` — the course poster, the preserved master (about
  1450 px wide). Not published as is.
- `thumbs/` — web thumbnails of the posters, 480 px and 800 px WebP,
  written by `tools/make_hero_thumbs.py`. The homepage and Teaching cards
  show them.
- `marks/` — the course marks the Course Library shows: the poster's
  central object, sized alike, at 80, 160 and 240 px. Written by
  `tools/make_library_marks.py`. `courses.yml` names the 80 px file and
  `tools/validate_courses.py` checks that the other two exist.
- `icons/` — the 1254 px masters of five course marks, each with a
  dark-ground preview. The other ten masters live in their course repos.

Same processing and privacy rules as `../processed/`. See
`../../../IMAGE_ASSET_PLAN.md`.
