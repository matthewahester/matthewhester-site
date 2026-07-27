#!/usr/bin/env python3
"""Validate courses.yml, the authoritative course registry.

Run automatically as a Quarto pre-render step (see `project.pre-render` in
_quarto.yml), so a registry violation fails the render before anything can be
published. Run it directly too:

    python tools/validate_courses.py

This gate FAILS CLOSED. Exit codes: 0 only when the registry parsed and every
invariant held; 1 for a violated invariant, a malformed registry, a missing
registry, or a missing parser. There is deliberately no "skip because PyYAML
is unavailable" path: a validator that passes when it could not run is worse
than no validator, because it reports a gate that is not there. PyYAML is
installed explicitly in the Pages workflow for exactly this reason.

The rules below enforce what TEACHING_PORTFOLIO_ARCHITECTURE.md sections 4
and 6 already say in prose: kind and status are independent and both must be
truthful; only a course-site record may carry a public path; unknown values
are omitted rather than invented.
"""

import os
import re
import sys

REGISTRY = "courses.yml"

LEVELS = {"Undergraduate", "Graduate"}
KINDS = {"site", "course", "direction"}
STATUSES = {
    "Current offering",
    "Maintained public reference",
    "In development",
    "No public materials yet",
    "Curriculum direction",
    "Archived resource",
}

# A record's kind constrains which public-material statuses can be true of it.
# A site has materials; a course does not yet; a direction is not a course.
KIND_STATUS = {
    "site": {"Current offering", "Maintained public reference", "Archived resource"},
    "course": {"In development", "No public materials yet"},
    "direction": {"Curriculum direction"},
}

REQUIRED = ("order", "title", "level", "kind", "status", "group", "summary", "categories")
OPTIONAL = ("code", "path", "image", "reviewed")
KNOWN = set(REQUIRED) | set(OPTIONAL)

PATH_RE = re.compile(r"^/[a-z0-9]+(?:-[a-z0-9]+)*/$")
IMAGE_RE = re.compile(r"^assets/images/[A-Za-z0-9._/-]+\.(?:webp|png|jpg|jpeg)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fail(problems, idx, title, msg):
    problems.append("  [%02d] %s\n        %s" % (idx, title or "<untitled>", msg))


def validate(records, root):
    problems = []
    seen_titles, seen_paths, seen_orders = {}, {}, {}

    if not isinstance(records, list) or not records:
        return ["  courses.yml must be a non-empty YAML list of course records."]

    for idx, rec in enumerate(records, 1):
        title = rec.get("title") if isinstance(rec, dict) else None
        if not isinstance(rec, dict):
            fail(problems, idx, None, "record is not a mapping")
            continue

        # -- required / unknown fields ------------------------------------
        for key in REQUIRED:
            if key not in rec or rec[key] in (None, "", []):
                fail(problems, idx, title, "missing required field '%s'" % key)
        for key in rec:
            if key not in KNOWN:
                fail(problems, idx, title, "unknown field '%s' (typo, or update this validator)" % key)

        level, kind, status = rec.get("level"), rec.get("kind"), rec.get("status")
        group, path, image = rec.get("group"), rec.get("path"), rec.get("image")

        # -- enums ---------------------------------------------------------
        if level is not None and level not in LEVELS:
            fail(problems, idx, title, "level %r is not one of %s" % (level, sorted(LEVELS)))
        if kind is not None and kind not in KINDS:
            fail(problems, idx, title, "kind %r is not one of %s" % (kind, sorted(KINDS)))
        if status is not None and status not in STATUSES:
            fail(problems, idx, title, "status %r is not one of %s" % (status, sorted(STATUSES)))

        # -- kind / status compatibility -----------------------------------
        if kind in KIND_STATUS and status in STATUSES:
            if status not in KIND_STATUS[kind]:
                fail(problems, idx, title,
                     "kind '%s' cannot have status '%s' (allowed: %s)"
                     % (kind, status, sorted(KIND_STATUS[kind])))

        # -- path rules ----------------------------------------------------
        if kind == "site":
            if not path:
                fail(problems, idx, title, "kind 'site' requires a public 'path'")
            elif not PATH_RE.match(path):
                fail(problems, idx, title,
                     "path %r must look like '/course-slug/' (leading and trailing slash)" % path)
        elif path:
            fail(problems, idx, title,
                 "kind '%s' must not expose a public course path (%r): a record that "
                 "links out reads as a published course site" % (kind, path))

        # -- categories must mirror the typed fields exactly ----------------
        cats = rec.get("categories")
        expected = [level, status, group]
        if cats is not None:
            if not isinstance(cats, list):
                fail(problems, idx, title, "categories must be a list")
            elif cats != expected:
                fail(problems, idx, title,
                     "categories %r must equal [level, status, group] = %r" % (cats, expected))

        # -- optional formats ----------------------------------------------
        if image is not None:
            if not IMAGE_RE.match(str(image)):
                fail(problems, idx, title, "image %r must be an assets/images/... webp/png/jpg path" % image)
            elif not os.path.isfile(os.path.join(root, image)):
                fail(problems, idx, title, "image %r does not exist on disk" % image)
        if rec.get("reviewed") is not None and not DATE_RE.match(str(rec["reviewed"])):
            fail(problems, idx, title, "reviewed %r must be an ISO date (YYYY-MM-DD)" % rec["reviewed"])
        if rec.get("code") is not None and not str(rec["code"]).strip():
            fail(problems, idx, title, "code is present but empty: omit it instead")

        # -- curated order ---------------------------------------------------
        # The Library is never alphabetical and has no visitor-facing sort, so
        # `order` is the only thing deciding sequence. It has to be an integer
        # and unique, or the displayed order stops being deterministic.
        order = rec.get("order")
        if order is not None:
            if isinstance(order, bool) or not isinstance(order, int):
                fail(problems, idx, title, "order %r must be an integer" % (order,))
            elif order < 1:
                fail(problems, idx, title, "order %r must be a positive integer" % (order,))
            elif order in seen_orders:
                fail(problems, idx, title, "duplicate order %d (also record %d)" % (order, seen_orders[order]))
            else:
                seen_orders[order] = idx

        # -- uniqueness ------------------------------------------------------
        if title:
            if title in seen_titles:
                fail(problems, idx, title, "duplicate title (also record %d)" % seen_titles[title])
            seen_titles[title] = idx
        if path:
            if path in seen_paths:
                fail(problems, idx, title, "duplicate path %r (also record %d)" % (path, seen_paths[path]))
            seen_paths[path] = idx

    return problems


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    registry = os.path.join(root, REGISTRY)

    try:
        import yaml
    except ImportError:
        sys.stderr.write(
            "ERROR: PyYAML is required to validate %s and is not installed.\n"
            "       The registry gate fails closed rather than passing unchecked.\n"
            "       Fix: python -m pip install PyYAML\n" % REGISTRY)
        return 1

    if not os.path.isfile(registry):
        sys.stderr.write("ERROR: %s not found (expected at %s).\n" % (REGISTRY, registry))
        return 1

    try:
        with open(registry, encoding="utf-8") as fh:
            records = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        sys.stderr.write("ERROR: %s is not valid YAML.\n\n%s\n" % (REGISTRY, exc))
        return 1
    except OSError as exc:
        sys.stderr.write("ERROR: could not read %s: %s\n" % (REGISTRY, exc))
        return 1

    problems = validate(records, root)
    if problems:
        sys.stderr.write("\n%s: %d problem(s) found.\n\n" % (REGISTRY, len(problems)))
        sys.stderr.write("\n".join(problems) + "\n\n")
        sys.stderr.write("Render aborted. See TEACHING_PORTFOLIO_ARCHITECTURE.md sections 4 and 6.\n")
        return 1

    n = len(records)
    sites = sum(1 for r in records if r.get("kind") == "site")
    print("%s: %d records OK (%d course sites, %d without a public site)." % (REGISTRY, n, sites, n - sites))
    return 0


if __name__ == "__main__":
    sys.exit(main())
