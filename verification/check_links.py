#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Mert Torun
# SPDX-License-Identifier: MIT
"""Check the links of this repository to doi.org, nbn-resolving.org and itself.

Only these hosts are requested: the DOI and URN resolvers, which carry the
citable addresses of the thesis, and this repository's own pages on
github.com. Other hosts are not requested, because publishers and many other
sites answer scripts with 403, and a check that fails for that reason says
nothing about the link.

The URLs are taken from the Markdown files outside fenced code blocks, from
CITATION.cff and from codemeta.json. The workflow runs this check on push and
by hand, never as a required check.

    check_links.py          request every URL in scope
    check_links.py --list   name the URLs in scope and request nothing

Return values: 0 every link answers, 1 a link fails, 2 no URL in scope was
found (a check over nothing is not a pass).
"""

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = re.compile(r"https?://[^\s<>()\"'`\]\[|]+")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
OWN = "/mtorun0x7cd/raven-one-simulink"
AGENT = "raven-one-simulink link check"


def in_scope(url):
    host_path = url.split("://", 1)[1]
    host, _, path = host_path.partition("/")
    path = "/" + path
    if host in ("doi.org", "nbn-resolving.org"):
        return True
    return host == "github.com" and (path == OWN or path.startswith(OWN + "/") or path.startswith(OWN + "#"))


def urls_of(path):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        kept, fenced = [], False
        for line in text.splitlines():
            if FENCE.match(line):
                fenced = not fenced
                continue
            if not fenced:
                kept.append(line)
        text = "\n".join(kept)
    return [match.group(0).rstrip(".,;:") for match in URL.finditer(text)]


def collect():
    files = sorted(p for p in ROOT.rglob("*.md") if "artifacts" not in p.parts and ".git" not in p.parts)
    files += [ROOT / "CITATION.cff", ROOT / "codemeta.json"]
    found = {}
    for path in files:
        if path.is_file():
            for url in urls_of(path):
                if in_scope(url):
                    found.setdefault(url, path.relative_to(ROOT).as_posix())
    return found


def request(url):
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url.split("#", 1)[0], method=method, headers={"User-Agent": AGENT})
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.status, response.geturl()
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in (403, 405, 501):
                continue
            return exc.code, url
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            return str(exc), url
    return "no answer", url


def main(argv):
    found = collect()
    if not found:
        print("ERROR no URL in scope was found; nothing was checked")
        return 2
    if len(argv) > 1 and argv[1] == "--list":
        for url, source in sorted(found.items()):
            print("%s  (%s)" % (url, source))
        return 0
    failed = 0
    for url, source in sorted(found.items()):
        status, final = request(url)
        good = isinstance(status, int) and 200 <= status < 400
        failed += not good
        print("%s %s (%s): %s%s" % ("PASS" if good else "FAIL", url, source, status,
                                    "" if final == url.split("#", 1)[0] else ", reached " + final))
    print("%s: %d of %d link(s) failed" % ("FAIL" if failed else "OK", failed, len(found)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
