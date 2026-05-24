# Current site state — matthewhester.com

_Snapshot for handoff / review. Local planning only; not rendered into
`_site/`. Last updated: 2026-05-24 (Phase 5F, post-launch cleanup)._

## Live status

- **Domain:** `matthewhester.com`
- **HTTP**: ✅ live as of Phase 5D.2
  (`http://matthewhester.com/`, `/math-software/`, `/intro-stats/` all 200)
- **HTTPS**: 🟡 pending — Let's Encrypt cert not yet issued by GitHub
  Pages. Retry with
  `gh api --method PUT repos/matthewahester/matthewhester-site/pages -F https_enforced=true`;
  succeeds when GitHub's domain-validation cycle completes (typically
  15 min – a few hours after DNS propagates).
- **www:** ✅ `www.matthewhester.com` 301-redirects to apex.
- **Old Google Site:** ✅ no longer served at the apex (replaced by
  the new Pages artifact).

## Three deployed repos

| Role | GitHub | Local | Latest commit |
|---|---|---|---|
| Hub | [matthewahester/matthewhester-site](https://github.com/matthewahester/matthewhester-site) | `D:/Github/matthewhester-site/` | `30add62` `ci: prepare Pages workflow for Node 24` |
| math-software | [matthewahester/math-software](https://github.com/matthewahester/math-software) | `D:/Github/math-software/` | `cb228dd` `site: initialize public math software course site` |
| intro-stats | [matthewahester/intro-stats](https://github.com/matthewahester/intro-stats) | `D:/Github/intro-stats/` | `61ba087` `site: add hub backlink` |

All three are public. The hub workflow checks out the course repos at
deploy time; course repos do not have their own workflows.

## DNS state (post-cutover, 2026-05-24)

| Type | Name | Value |
|---|---|---|
| A | `matthewhester.com` (apex) | `185.199.108.153`, `.109.153`, `.110.153`, `.111.153` |
| AAAA | `matthewhester.com` (apex) | `2606:50c0:8000::153`, `:8001::153`, `:8002::153`, `:8003::153` |
| CNAME | `www.matthewhester.com` | `matthewahester.github.io` |
| NS | `matthewhester.com` | `ns-cloud-d{1,2,3,4}.googledomains.com` (Squarespace-managed Google Cloud DNS) |

Old apex A `198.185.159.145` (Google Sites) and old www CNAME
`ghs.googlehosted.com` were replaced. Stale-cache propagation may
linger on some resolvers (worst case ~2 hours from the cutover time)
because the old A record carried a 14400-second TTL.

## GitHub Pages config

```json
{
  "cname": "matthewhester.com",
  "html_url": "http://matthewhester.com/",
  "build_type": "workflow",
  "https_enforced": false,
  "protected_domain_state": null,
  "pending_domain_unverified_at": null
}
```

`https_enforced` flips to `true` once the cert is issued and the
enable call succeeds.

## Combined-deploy workflow

[`.github/workflows/publish.yml`](../.github/workflows/publish.yml) is
**`on: workflow_dispatch` only** — no push trigger. One manual click in
the Actions UI (or `gh workflow run publish.yml --repo matthewahester/matthewhester-site --ref main`)
runs the whole pipeline:

1. Checkout hub
2. Checkout `matthewahester/math-software` → `course-math-software/`
3. Checkout `matthewahester/intro-stats` → `course-intro-stats/`
4. Set up Quarto
5. Render hub
6. Render each course (in its own working directory)
7. Copy course `_site/.` into `_site/{math-software,intro-stats}/`
8. Ensure root CNAME; drop nested CNAMEs
9. Upload artifact → deploy

Action versions (Phase 5D.1 bump): `actions/checkout@v5`,
`actions/upload-pages-artifact@v5`, `actions/deploy-pages@v5`,
`quarto-dev/quarto-actions/setup@v2`. No Node 20 deprecation
warnings on the last run.

## Main pages and navbar (hub)

| Page      | File             | Role                                                                  |
| --------- | ---------------- | --------------------------------------------------------------------- |
| Home      | `index.qmd`      | Title block (single H1 + subtitle) + split-hero + cards               |
| About     | `about.qmd`      | Short professional bio + brief personal note                          |
| Teaching  | `teaching.qmd`   | Three current courses (Applied Stats I as LMS-only)                   |
| Research  | `research.qmd`   | Five interests + four projects + placeholder publications/talks       |
| Resources | `resources.qmd`  | Index of public course-site resources + planned writeups              |
| CV        | `cv.qmd`         | Position + interests + teaching/service + selected work + PDF placeholder |
| Contact   | `contact.qmd`    | University vs general professional channels + Blackboard pointer      |

Not in the navbar but still in the repo:

- `projects.qmd` — Phase 4A redirect stub. **Recommended for deletion
  in Phase 5E cleanup** now that the site is live and no external
  bookmarks point at `/projects.html`.

## Visual identity status

- **Palette:** rock/crystal/climbing tokens in `styles.css`. Unchanged
  since Phase 3.
- **Type:** Inter (body + headings), JetBrains Mono (code).
- **Hero:** Quarto title block above two-column split with intro
  prose + page links on the left and stylized portrait on the right.
  Collapses to single-column ≤720px with portrait above text.
- **Cards:** all text-only as of Phase 4C. Image-bearing variants
  still in `styles.css` for future intentional use.
- **No JS**, no analytics, no third-party widgets.

## Current image policy

- **Raw originals** stage in `assets/images/raw/` (gitignored).
- **Processed images:**
  - `assets/images/brand/`: `portrait-matt-hester-800.{webp,jpg}` (live
    on the hub hero), `og-default-og.{webp,jpg}` (site-wide OG card).
    The earlier `portrait-placeholder.svg` was deleted in Phase 5F
    once the real portrait was confirmed live.
  - `assets/images/course-motifs/`: five 600px motif/course images
    produced in Phase 4B, currently **unreferenced** in any QMD.
- **No location-revealing filenames** in committed assets.
- **EXIF stripped** on all processed outputs (verified in Phase 4B).
- **Helper:** `tools/process_images.py` (Pillow).
- The Phase 4A `assets/brand/` redirect-stub folder was deleted in
  Phase 5F.

## Recent phase summary

- **Phase 4A–C** (2026-05-23): site scaffold → image pipeline →
  editorial cleanup (text-only cards, contact split, BNO branding
  removed from public page).
- **Phase 4D–E** (2026-05-23): review bundle for ChatGPT, pre-commit
  editorial polish.
- **Phase 4F–G** (2026-05-23): commit hygiene, first milestone
  commit + push (hub `6d5aa95`).
- **Phase 5A** (2026-05-23): deployment-architecture inspection,
  drafted combined-deploy workflow.
- **Phase 5B** (2026-05-23): course-site privacy hygiene, hardened
  `math-software/.gitignore`, added course back-links, local
  combined-build smoke test.
- **Phase 5C** (2026-05-24): created public course GitHub repos,
  pushed both, applied combined workflow on the hub, triggered first
  Pages deploys. Pages enabled with `build_type=workflow`.
- **Phase 5D.1** (2026-05-24): action versions bumped to clear Node
  20 deprecation, custom domain `matthewhester.com` set in Pages
  settings, DNS cutover checklist prepared.
- **Phase 5D.2** (2026-05-24): user edited DNS in Squarespace; A,
  AAAA, www CNAME records replaced; HTTP smoke test fully green.
- **Phase 5E** (2026-05-24): cleanup audit, state-doc refresh, more
  HTTPS polling (still pending).
- **Phase 5F** (2026-05-24): deleted `portrait-placeholder.svg` and
  `assets/brand/`, kept `projects.qmd` (user-preferred 404
  insurance), refreshed `OPEN_DECISIONS.md` (marked items 3/5/6/7
  resolved), refreshed `main_site_status.md` (Phase 5 entries),
  refreshed `CLAUDE.md` and `IMAGE_ASSET_PLAN.md` to drop stale
  references. Committed three durable Phase 5A/5D planning docs.
  HTTPS still pending.

## Outstanding items (post-Phase-5F)

| Item | Disposition |
|---|---|
| Enable HTTPS once cert is issued | One API PUT call (`gh api --method PUT … -F https_enforced=true`); gated on GitHub-side validation. Polling will eventually succeed. |
| Run HTTPS smoke test after enforcement | Mirror the HTTP list; expect 200 + `https://` final URLs |
| Switch workflow to push-on-main (optional) | See `OPEN_DECISIONS.md` item 3 — currently `workflow_dispatch:` only |
| Card motif images (optional) | See `OPEN_DECISIONS.md` item 1 — currently all cards text-only |
| Real CV PDF (optional) | See `OPEN_DECISIONS.md` item 2 — currently text-only placeholder |

## Reviewer entry points

- Live site: `http://matthewhester.com/` (HTTPS coming soon)
- Hub repo: <https://github.com/matthewahester/matthewhester-site>
- Course repos: <https://github.com/matthewahester/math-software>,
  <https://github.com/matthewahester/intro-stats>
- Design intent + constraints: `SITE_VISION.md`, `BRAND_STYLE_BRIEF.md`,
  `SITE_LINKING_PLAN.md`, `CLAUDE.md`
- Open decisions: `_site_planning/OPEN_DECISIONS.md` (some items now
  resolved — update pending)
