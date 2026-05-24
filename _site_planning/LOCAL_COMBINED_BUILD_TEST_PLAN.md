# Local combined-build test plan — Phase 5A

_How to assemble and serve the combined artifact locally, using only
the three existing repos on disk. Lets us validate the architecture
before any CI work or DNS change._

Local planning only; not rendered into `_site/`. Last updated:
2026-05-23.

## What this validates

- Each site renders cleanly on its own.
- The contents of each course site's `_site/` copy correctly into a
  subdirectory of the hub's `_site/`.
- Relative links inside each course site continue to work when the
  site is served from a subdirectory.
- The hub's links to `/math-software/` and `/intro-stats/` resolve.
- The hub's CNAME survives the assembly.
- Per-site `site_libs/` and `search.json` don't collide.

## What this does NOT validate

- GitHub Actions checkout / token behavior (those are CI concerns).
- DNS / HTTPS / Pages-side configuration.
- Search across sites (each site's search is scoped to itself).

## Assumptions

- All three repos are at the documented paths and currently render
  cleanly with `quarto render` from their own roots.
- PowerShell on Windows is the shell. Equivalent `bash` commands are
  given as a fallback in comments.
- Python is available for the optional local server (`python -V`
  works).

## Step 1 — Render each site

From PowerShell. Each `Push-Location` / `Pop-Location` pair changes
directory only for the duration of the render.

```powershell
Push-Location "D:/Github/matthewhester-site"
quarto render
Pop-Location

Push-Location "D:/Github/math-software"
quarto render
Pop-Location

Push-Location "D:/Github/intro-stats"
quarto render
Pop-Location
```

Each should print `Output created: _site\index.html` and exit with
code 0. PowerShell may emit `NativeCommandError` around the progress
output — that is cosmetic Quarto stderr noise; trust the exit code.

## Step 2 — Assemble the combined artifact

The hub's `_site/` is the base. Add `math-software/` and
`intro-stats/` subdirectories, populated from the corresponding
course `_site/` contents.

```powershell
$Hub      = "D:/Github/matthewhester-site/_site"
$MathOut  = "$Hub/math-software"
$StatsOut = "$Hub/intro-stats"

# Clean out any prior staging copies (safe — these are subdirs of
# the hub's gitignored _site/, never source).
if (Test-Path $MathOut)  { Remove-Item $MathOut  -Recurse -Force }
if (Test-Path $StatsOut) { Remove-Item $StatsOut -Recurse -Force }

# Copy CONTENTS of each course _site/ into its subdirectory under
# the hub _site/. -Recurse copies the tree; using the trailing
# `\*` on the source means "contents of, not the dir itself", which
# is the PowerShell analogue of `cp -r src/. dst/`.
New-Item -ItemType Directory -Path $MathOut  | Out-Null
New-Item -ItemType Directory -Path $StatsOut | Out-Null

Copy-Item "D:/Github/math-software/_site/*" -Destination $MathOut  -Recurse -Force
Copy-Item "D:/Github/intro-stats/_site/*"   -Destination $StatsOut -Recurse -Force

# Hub CNAME must be at the artifact root. Drop any nested CNAMEs
# (course sites don't produce any today, but be defensive).
Copy-Item "D:/Github/matthewhester-site/CNAME" -Destination "$Hub/CNAME" -Force
Get-ChildItem -Path $Hub -Recurse -Filter "CNAME" |
  Where-Object { $_.FullName -ne (Resolve-Path "$Hub/CNAME").Path } |
  Remove-Item -Force
```

### Bash / WSL fallback

```bash
HUB=/d/Github/matthewhester-site/_site
rm -rf "$HUB/math-software" "$HUB/intro-stats"
mkdir -p "$HUB/math-software" "$HUB/intro-stats"
cp -r /d/Github/math-software/_site/. "$HUB/math-software/"
cp -r /d/Github/intro-stats/_site/.   "$HUB/intro-stats/"
cp /d/Github/matthewhester-site/CNAME "$HUB/CNAME"
find "$HUB" -mindepth 2 -name CNAME -delete
```

## Step 3 — Sanity-check the assembled tree

```powershell
$Hub = "D:/Github/matthewhester-site/_site"

Write-Host "=== top-level files ===" -ForegroundColor Cyan
Get-ChildItem $Hub -File | Select-Object Name

Write-Host "=== subdirectories ===" -ForegroundColor Cyan
Get-ChildItem $Hub -Directory | Select-Object Name

Write-Host "=== math-software index exists ===" -ForegroundColor Cyan
Test-Path "$Hub/math-software/index.html"

Write-Host "=== intro-stats index exists ===" -ForegroundColor Cyan
Test-Path "$Hub/intro-stats/index.html"

Write-Host "=== CNAME content ===" -ForegroundColor Cyan
Get-Content "$Hub/CNAME"

Write-Host "=== no nested CNAMEs ===" -ForegroundColor Cyan
Get-ChildItem -Path $Hub -Recurse -Filter "CNAME" | Select-Object FullName

Write-Host "=== course site_libs and search.json are self-contained ===" -ForegroundColor Cyan
Test-Path "$Hub/math-software/site_libs"
Test-Path "$Hub/math-software/search.json"
Test-Path "$Hub/intro-stats/site_libs"
Test-Path "$Hub/intro-stats/search.json"
```

Expected:

- `index.html`, `CNAME`, `robots.txt`, `sitemap.xml`, `search.json`,
  `styles.css` at top level.
- `math-software/`, `intro-stats/`, `site_libs/`, `assets/` (and
  other rendered subdirs) as subdirectories.
- `$Hub/math-software/index.html` and `$Hub/intro-stats/index.html`
  both exist.
- CNAME at top level only; the nested-CNAME check returns just the
  top-level path.
- Each course subdir has its own `site_libs/` and `search.json`.

## Step 4 — Serve locally

A simple static server is enough; Pages serves the artifact as
plain files. From PowerShell:

```powershell
cd "D:/Github/matthewhester-site/_site"
python -m http.server 8080
```

Then in a browser visit:

- <http://localhost:8080/>
- <http://localhost:8080/math-software/>
- <http://localhost:8080/intro-stats/>

Click around each site. Confirm:

- Navbar, sidebar, and footer all render with styling.
- Internal links inside the course site stay within the course site
  (e.g. clicking "Syllabus" on `/math-software/` goes to
  `/math-software/syllabus.html`, not `/syllabus.html`).
- The hub's homepage cards' `/math-software/` and `/intro-stats/`
  links land on the right course site.
- The search box (top-right on Quarto pages) returns results
  scoped to whatever site you're currently on.
- Images, CSS, and any client-side JS load (check the browser
  console for 404s).

Stop the server with `Ctrl-C`.

## Step 5 — Clean up

The hub's `_site/` is gitignored, so the staged combined artifact
isn't an artifact-pollution risk. If you'd like a clean slate
between iterations:

```powershell
Remove-Item "D:/Github/matthewhester-site/_site"      -Recurse -Force
Remove-Item "D:/Github/math-software/_site"           -Recurse -Force
Remove-Item "D:/Github/intro-stats/_site"             -Recurse -Force
```

Re-run from Step 1.

## What success looks like

If all of the above passes, the combined-deploy architecture is
ready to wire into CI. The remaining unknowns are GitHub-side:
checkout token behavior, Pages config, and DNS. Those are addressed
in `DEPLOYMENT_ARCHITECTURE_PHASE5A.md` §4 ("Safe publication
sequence").
