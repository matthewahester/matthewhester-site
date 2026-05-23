# Raw images — gitignored

This folder is **gitignored** via the repo `.gitignore`. Drop full-size,
unprocessed source images here for staging; they are never committed.

Workflow:

1. Copy a raw image into this folder.
2. Run `python tools/process_images.py <file> --target {brand|card|motif|banner}`
   to produce EXIF-stripped WebP + JPEG outputs in
   `../processed/` (or `../brand/`, `../course-motifs/` if you move them).
3. Delete the file from this folder once processed.

Originals also live in:

- `D:/My Drive Personal/Climbing/Favorite Photos/` — climbing imagery
- `D:/My Drive Personal/Personal/` — portrait (`hester_profile_art*`)

See `../../../IMAGE_ASSET_PLAN.md` for the full policy (EXIF, alt text,
filename rules, privacy).
