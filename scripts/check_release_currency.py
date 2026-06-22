#!/usr/bin/env python3
"""Creatio release-currency watch.

Detects when Creatio ships a version newer than our recorded baseline so the
hub corpus doesn't silently go stale. Parses the STATIC Academy sitemap(s) for
release-notes / changelog slugs (e.g. `8-3-5-twin-release-notes`), extracts the
version triples, and compares the max found against BASELINE.

No firecrawl / JS needed — the sitemap is static XML, so this runs headless in a
cron with only the Python stdlib. Exit codes:
  0  = up to date (max published == baseline)
  3  = a NEWER version is published  -> run targeted_refresh.py + re-embed
  4  = could not fetch the sitemap (network/structure issue; investigate)

Baseline verified 2026-06-22: latest GA = 8.3.4 "Twin" (no 8.3.5/8.4). Next
Creatio "10x" release event is 2026-07-15 — bump BASELINE when a new line ships.

Usage:
  python3 check_release_currency.py            # check + print
  python3 check_release_currency.py --quiet    # only print on a new version
"""
from __future__ import annotations
import re
import sys
import argparse
import urllib.request

BASELINE = (8, 3, 4)  # update when a newer line is confirmed + corpus refreshed
UA = {"User-Agent": "creatio-hub-release-watch/1.0 (+https://academy.creatio.com)"}
SITEMAPS = [
    "https://academy.creatio.com/docs/8.x/sitemap.xml",
    "https://academy.creatio.com/docs/8.x/dev/sitemap.xml",
]
# Match .../release-notes/8-3-5-twin-release-notes and .../changelog/8-3-5-twin-changelog
SLUG_RE = re.compile(r"/(?:release-notes|releases/changelog)/(\d+)-(\d+)-(\d+)-", re.I)
LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>", re.I)


def fetch(url: str, timeout: int = 20) -> str | None:
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  fetch failed: {url} -> {e}", file=sys.stderr)
        return None


def collect_locs(xml: str) -> list[str]:
    return LOC_RE.findall(xml or "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true", help="print only when a newer version is found")
    args = ap.parse_args()

    seen_xml = []
    locs: list[str] = []
    for sm in SITEMAPS:
        xml = fetch(sm)
        if not xml:
            continue
        seen_xml.append(sm)
        sub = collect_locs(xml)
        # sitemap-index? recurse one level into child sitemaps that look relevant
        if any(s.endswith(".xml") for s in sub):
            for child in sub:
                if child.endswith(".xml") and ("doc" in child or "sitemap" in child):
                    cx = fetch(child)
                    if cx:
                        locs.extend(collect_locs(cx))
        else:
            locs.extend(sub)

    if not locs:
        print("ERROR: no sitemap URLs retrieved — Academy sitemap unreachable or restructured.", file=sys.stderr)
        print("Fallback: manually check https://academy.creatio.com/docs/8.x/resources/category/release-notes", file=sys.stderr)
        return 4

    versions = set()
    for u in locs:
        m = SLUG_RE.search(u)
        if m:
            versions.add(tuple(int(x) for x in m.groups()))
    if not versions:
        print("ERROR: sitemap fetched but no release-notes/changelog version slugs matched.", file=sys.stderr)
        return 4

    newest = max(versions)
    newer = sorted(v for v in versions if v > BASELINE)
    fmt = lambda v: ".".join(map(str, v))

    if newer:
        print(f"🔴 NEW CREATIO RELEASE(S) DETECTED: {', '.join(fmt(v) for v in newer)}")
        print(f"   Baseline was {fmt(BASELINE)}; newest published is {fmt(newest)}.")
        print("   ACTION: crawl the new release notes + changelog and re-embed:")
        print("     set -a; source docs-corpus/.env; set +a")
        print(f"     docs-corpus/scripts/crawlers/targeted_refresh.py <release-notes + changelog URLs for {fmt(newest)}>")
        print("     ai-knowledge-hub/surgical_reembed.py <abs_paths.txt>")
        print(f"   Then bump BASELINE to {fmt(newest)} in this script + the version stamps in CLAUDE.md.")
        return 3

    if not args.quiet:
        known = ", ".join(fmt(v) for v in sorted(versions)[-6:])
        print(f"✅ Up to date. Baseline {fmt(BASELINE)} == newest published {fmt(newest)}.")
        print(f"   (checked {len(seen_xml)} sitemap(s); recent release-note versions seen: {known})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
