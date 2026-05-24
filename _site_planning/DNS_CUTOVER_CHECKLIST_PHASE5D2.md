# DNS cutover checklist — Phase 5D.2

_Local planning only; not rendered into `_site/`. Last updated:
2026-05-24 (end of Phase 5D.1)._

**Do not execute this checklist until Matt has explicitly approved
Phase 5D.2.** This document is the plan; the execution is a separate
deliberate step.

## Pre-cutover state (verified at end of Phase 5D.1)

### GitHub Pages

- Repo: `matthewahester/matthewhester-site`
- Build source: GitHub Actions workflow (`build_type=workflow`)
- Custom domain set: `cname=matthewhester.com`
- HTTPS enforcement: **disabled** (`https_enforced=false`) — GitHub
  auto-disabled it because Let's Encrypt can't issue a cert until DNS
  validates. Will re-enable after DNS cutover.
- `html_url=http://matthewhester.com/` (Pages now expects to be served
  from the custom domain; the github.io staging URL 301-redirects to
  the custom domain).
- Latest deploy: workflow run `26365721933`, commit `30add62`.
- Artifact contains CNAME = `matthewhester.com` at root.

### Current DNS (Google Cloud DNS, via Google Domains / Squarespace)

| Type | Name | Value | Notes |
|---|---|---|---|
| A | `matthewhester.com` (apex) | `198.185.159.145` | Old Google Sites IP |
| AAAA | `matthewhester.com` (apex) | (none) | No IPv6 currently |
| CNAME | `www.matthewhester.com` | (none) | No www record |
| MX | `matthewhester.com` | (none) | No custom email — nothing to preserve |
| TXT | `matthewhester.com` | (none) | No SPF / verification tokens — nothing to preserve |
| NS | `matthewhester.com` | `ns-cloud-d{1,2,3,4}.googledomains.com` | Google Cloud DNS nameservers |

**Nothing to preserve.** The only meaningful record is the single A
record at the apex; replacing it switches everything from Google Sites
to GitHub Pages.

### Verified via DNS bypass that GitHub Pages serves correctly

Using `curl --resolve matthewhester.com:80:185.199.108.153`:

- `/` → 200, title `<title>Matt Hester</title>`
- `/math-software/` → 200, title `<title>Intro to Mathematical Software</title>`
- `/intro-stats/` → 200, title `<title>Intro to Statistics</title>`
- `/math-software/syllabus.html` → 200
- `/CNAME` → 200, body `matthewhester.com`

The artifact is ready; only DNS is missing.

## Cutover plan

### Records to ADD (apex A records — required)

Replace the existing A record at the apex with the four GitHub Pages
canonical IPs. The TTL on the current zone is 300s (5 min), so
propagation will be fast.

```
Type  Name (apex)            Value             TTL
A     matthewhester.com      185.199.108.153   300
A     matthewhester.com      185.199.109.153   300
A     matthewhester.com      185.199.110.153   300
A     matthewhester.com      185.199.111.153   300
```

Some DNS panels accept a single A "record" with four values; others
require four separate records with the same name. Either form is
fine; the resolver returns all four either way.

### Optional records to ADD (IPv6 support)

GitHub Pages supports IPv6 at these addresses. Not required, but a
small modern-DNS improvement:

```
Type  Name (apex)            Value
AAAA  matthewhester.com      2606:50c0:8000::153
AAAA  matthewhester.com      2606:50c0:8001::153
AAAA  matthewhester.com      2606:50c0:8002::153
AAAA  matthewhester.com      2606:50c0:8003::153
```

### Optional records to ADD (www subdomain)

If you want `https://www.matthewhester.com/` to work alongside the
apex:

```
Type   Name                   Value
CNAME  www.matthewhester.com  matthewahester.github.io
```

`matthewahester.github.io` (the user's Pages user-domain, with the
trailing dot omitted by most UIs) is the canonical CNAME target
GitHub recommends for the `www` subdomain.

Skip this if you'd rather keep the public identity strictly at the
apex.

### Records to REMOVE

```
Type  Name (apex)            Old value
A     matthewhester.com      198.185.159.145   (old Google Sites)
```

This is the only legacy record to drop. Some DNS UIs let you edit a
record in place; others require delete-then-create. Both produce the
same final state.

### Records to LEAVE ALONE

- NS records — keep the four `ns-cloud-d*.googledomains.com`
  nameservers as-is. Switching nameservers is a separate, larger
  decision; the cutover only needs A-record changes inside the
  existing Google Cloud DNS zone.

## Execution sequence (Phase 5D.2)

Do these in this exact order. Time the cutover for a quiet window
since matthewhester.com is briefly in an inconsistent state while
DNS propagates (worst case ~5 min with the current 300s TTL).

1. **Pre-flight (read-only)**
   - Re-run the Phase 5D.1 smoke test via the DNS-bypass curl
     pattern to confirm the artifact at `185.199.108.153` is still
     the latest deploy.
   - `gh api repos/matthewahester/matthewhester-site/pages` —
     confirm `cname=matthewhester.com`.
   - Browser-screenshot the current Google Sites homepage at
     `matthewhester.com` for the audit trail (so we know what was
     replaced).

2. **DNS change at the registrar/DNS provider**
   - Log into Google Cloud DNS (or Squarespace's DNS panel for
     this domain, depending on where the user manages it now).
   - Open the `matthewhester.com` zone.
   - Replace the apex A record `198.185.159.145` with the four
     `185.199.108-111.153` records (and optional AAAA + www CNAME).
   - Save.

3. **Wait for propagation**
   - With TTL = 300, most resolvers see the new value within
     ~5 minutes. Verify with:
     ```
     nslookup matthewhester.com 8.8.8.8
     nslookup matthewhester.com 1.1.1.1
     ```
     Both should return the four GitHub IPs.

4. **GitHub verifies the domain**
   - GitHub Pages re-checks the domain automatically; this is
     usually within a few minutes of seeing the correct A records.
   - Watch in **Settings → Pages**: the custom-domain section will
     show "DNS check successful" once verified.
   - At that point GitHub provisions a Let's Encrypt cert (a few
     more minutes).

5. **Enable HTTPS**
   - Once the cert is issued, GitHub will show "Enforce HTTPS" as a
     checkable option in **Settings → Pages**. Re-enable it (or
     via API: `gh api --method PUT repos/matthewahester/matthewhester-site/pages -F https_enforced=true`).

6. **Live smoke test**
   - From a fresh browser session and from `curl` with no DNS
     bypass, walk the same URL list as Phase 5D.1:
     ```
     https://matthewhester.com/
     https://matthewhester.com/about.html
     https://matthewhester.com/teaching.html
     https://matthewhester.com/research.html
     https://matthewhester.com/resources.html
     https://matthewhester.com/math-software/
     https://matthewhester.com/math-software/syllabus.html
     https://matthewhester.com/math-software/notes/index.html
     https://matthewhester.com/math-software/labs/lab01-install-stack.html
     https://matthewhester.com/intro-stats/
     https://matthewhester.com/intro-stats/syllabus.html
     https://matthewhester.com/intro-stats/notes/week01-data-evidence.html
     https://matthewhester.com/CNAME
     ```
   - Every status should be 200. Cert should be valid for
     `matthewhester.com`.

## Rollback plan

If anything goes wrong in step 2–6:

- The **only** change made at the registrar is the apex A records.
  Revert them to `198.185.159.145` and matthewhester.com is back on
  Google Sites within one TTL (~5 min).
- Nothing on the GitHub side needs to be undone for rollback; the
  Pages site keeps running, just won't be reached at the custom
  domain. The github.io URL stays redirecting to the custom domain
  while `cname` is set — if you want full staging access during a
  rollback, also clear cname:
  ```
  gh api --method PUT repos/matthewahester/matthewhester-site/pages -f cname=
  ```
  Setting it back later is a single API call.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| TTL longer than expected, slow propagation | Low (TTL=300) | Minor; up to 5–10 min visible inconsistency | Plan the cut for a quiet window |
| Resolver caches old IP for hours | Low | Minor; resolver-by-resolver | Wait for global propagation before declaring done |
| Let's Encrypt cert delayed | Low–medium | Site briefly serves HTTP only | "Enforce HTTPS" remains unchecked until cert lands; site still works at HTTP |
| Old Google Site has bookmarks pointing to subpaths that don't exist on the new site | Medium | 404s for stale bookmarks | Acceptable for a personal site; old Google Sites is being intentionally retired |
| Email at @matthewhester.com | n/a | No MX records exist; no email impact | Confirmed via DNS inventory |
| Squarespace/Google Domains transfer state | Unknown | Could affect where DNS is edited | Check both panels if Google Cloud DNS access has been removed |

## Approval gate

Phase 5D.2 starts when Matt explicitly says "do the DNS cutover" (or
equivalent). Until then, this document is the plan, not the action.
