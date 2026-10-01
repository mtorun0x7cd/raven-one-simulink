#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Mert Torun
# SPDX-License-Identifier: MIT
"""Check that the reading copy is faithful to the deposited thesis.

The reading copy under publication/ is the deposited PDF with its images
downsampled, so that it stays under 5 MB. It must say the same thing as the
deposit, and it must say what it is itself, because a downloaded copy travels
without this repository. This script compares the two files:

  * the same number of pages;
  * the same text, with all whitespace removed, in two orders: as the
    pages draw it (pdftotext -raw) and as it stands on the page (pdftotext
    -layout). The re-encoding moves glyphs by fractions of a point, which can
    add or drop a space between two characters, so a space-only difference is
    counted and reported, not failed. The default order of pdftotext is not
    used: it guesses columns, and the guess differs between the two files for
    two lines that stand at the same place on both;
  * the same number of outline entries and of link annotations, and the same
    page labels (qpdf --json);
  * the same Title, Author and Keywords (pdfinfo);
  * the one deliberate difference: Subject, and dc:description in the XMP
    metadata, read SUBJECT below;
  * each page rendered at 20 dpi in grey, with a mean absolute difference of
    at most TOLERANCE grey levels (of 255).

    check_reading_copy.py                         the two files under publication/
    check_reading_copy.py DEPOSIT READING-COPY    two other files

Return values: 0 faithful, 1 a difference, 2 a tool error (a missing file,
pdfinfo, pdftotext, pdftoppm or qpdf not installed).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEPOSIT = ROOT / "publication" / "Torun_Password_Keyless_Authentication.pdf"
READING_COPY = ROOT / "publication" / "Torun_Password_Keyless_Authentication_reading-copy.pdf"
SUBJECT = ("Reading copy of https://doi.org/10.57683/EPUB-3598; images downsampled; "
           "not the version of record; do not cite")
SAME_FIELDS = ("Title", "Author", "Keywords")
TOLERANCE = 1.0
DPI = 20


class ToolError(Exception):
    pass


def tool(args, binary=False):
    try:
        result = subprocess.run(args, check=True, capture_output=True)
    except FileNotFoundError:
        raise ToolError("%s is not installed" % args[0])
    except subprocess.CalledProcessError as exc:
        raise ToolError("%s failed: %s" % (" ".join(args[:2]), exc.stderr.decode(errors="replace").strip()))
    return result.stdout if binary else result.stdout.decode("utf-8", errors="replace")


def info(pdf):
    fields = {}
    for line in tool(["pdfinfo", "-enc", "UTF-8", str(pdf)]).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def xmp_description(pdf):
    meta = tool(["pdfinfo", "-meta", str(pdf)])
    match = re.search(r"<dc:description>.*?<rdf:li[^>]*>(.*?)</rdf:li>", meta, re.S)
    return match.group(1).strip() if match else None


def text(pdf, mode):
    return tool(["pdftotext", mode, "-enc", "UTF-8", str(pdf), "-"])


def structure(pdf):
    data = json.loads(tool(["qpdf", "--json", "--json-key=outlines", "--json-key=pagelabels",
                            "--json-key=qpdf", str(pdf)]))

    def count(entries):
        return sum(1 + count(entry.get("kids", [])) for entry in entries)

    objects = data["qpdf"][1]
    links = sum(1 for value in objects.values()
                if isinstance(value, dict) and isinstance(value.get("value"), dict)
                and value["value"].get("/Subtype") == "/Link")
    return count(data.get("outlines", [])), links, data.get("pagelabels", [])


def pgm(data):
    """(width, height, pixels) of one binary greyscale PGM image."""
    fields, i = [], 0
    while len(fields) < 4:
        while data[i:i + 1].isspace():
            i += 1
        j = i
        while not data[j:j + 1].isspace():
            j += 1
        fields.append(data[i:j])
        i = j
    if fields[0] != b"P5":
        raise ToolError("pdftoppm did not write a binary PGM image")
    width, height = int(fields[1]), int(fields[2])
    return width, height, data[i + 1:i + 1 + width * height]


def render(pdf, page):
    """One page in grey at DPI, read from the standard output of pdftoppm; no file is written."""
    return pgm(tool(["pdftoppm", "-f", str(page), "-l", str(page), "-singlefile", "-r", str(DPI), "-gray",
                     str(pdf)], binary=True))


def compare(deposit, copy, emit):
    failed = 0

    def report(name, holds, detail):
        nonlocal failed
        failed += 0 if holds else 1
        emit("%s %s: %s" % ("PASS" if holds else "FAIL", name, detail))

    for path in (deposit, copy):
        if not path.is_file():
            raise ToolError("missing file: %s" % path)
    a, b = info(deposit), info(copy)
    report("pages", a.get("Pages") == b.get("Pages"), "%s and %s pages" % (a.get("Pages"), b.get("Pages")))
    for field in SAME_FIELDS:
        report("info-" + field.lower(), a.get(field) == b.get(field) and a.get(field),
               "%s %r" % (field, b.get(field)) if a.get(field) == b.get(field)
               else "%s differs: deposit %r, reading copy %r" % (field, a.get(field), b.get(field)))
    report("info-subject", b.get("Subject") == SUBJECT, "Subject %r" % b.get("Subject"))
    description = xmp_description(copy)
    report("xmp-description", description == SUBJECT, "dc:description %r" % description)
    if b.get("Encrypted", "no").startswith("yes"):
        report("not-encrypted", False, "the reading copy is encrypted")
    size = copy.stat().st_size
    report("size", size < 5 * 1000 * 1000, "%d bytes, under 5 MB" % size if size < 5000000 else "%d bytes" % size)

    for mode in ("-raw", "-layout"):
        text_a, text_b = text(deposit, mode), text(copy, mode)
        squeezed_a, squeezed_b = "".join(text_a.split()), "".join(text_b.split())
        words_a, words_b = text_a.split(), text_b.split()
        name = "text" + mode
        if squeezed_a == squeezed_b:
            report(name, True, "%d characters without whitespace, equal; %s" % (
                len(squeezed_a), "the spacing is equal too" if words_a == words_b
                else "the spacing differs, first at word %d" % next(
                    (i for i, (x, y) in enumerate(zip(words_a, words_b)) if x != y), min(len(words_a), len(words_b)))))
        else:
            at = next((i for i, (x, y) in enumerate(zip(squeezed_a, squeezed_b)) if x != y),
                      min(len(squeezed_a), len(squeezed_b)))
            report(name, False, "differs at character %d: deposit %r, reading copy %r"
                   % (at, squeezed_a[at:at + 30], squeezed_b[at:at + 30]))

    outline_a, links_a, labels_a = structure(deposit)
    outline_b, links_b, labels_b = structure(copy)
    report("outline", outline_a == outline_b, "%d and %d outline entries" % (outline_a, outline_b))
    report("links", links_a == links_b, "%d and %d link annotations" % (links_a, links_b))
    report("page-labels", labels_a == labels_b, "%d and %d page label ranges" % (len(labels_a), len(labels_b)))

    pages = int(a.get("Pages", "0") or 0)
    if pages == 0 or a.get("Pages") != b.get("Pages"):
        report("renders", False, "not compared, because the page counts differ or are unknown")
    else:
        worst, worst_page = 0.0, 0
        for number in range(1, pages + 1):
            wa, ha, pa = render(deposit, number)
            wb, hb, pb = render(copy, number)
            if (wa, ha) != (wb, hb):
                worst, worst_page = float("inf"), number
                break
            difference = sum(abs(p - q) for p, q in zip(pa, pb)) / len(pa)
            if difference > worst:
                worst, worst_page = difference, number
        report("renders", worst <= TOLERANCE,
               "%d pages at %d dpi; the largest mean difference is %.3f grey levels, on page %d (at most %.1f)"
               % (pages, DPI, worst, worst_page, TOLERANCE))
    return failed


def main(argv):
    if len(argv) not in (1, 3):
        print("usage: check_reading_copy.py [DEPOSIT READING-COPY]", file=sys.stderr)
        return 2
    deposit, copy = (Path(argv[1]), Path(argv[2])) if len(argv) == 3 else (DEPOSIT, READING_COPY)
    try:
        failed = compare(deposit, copy, print)
    except ToolError as exc:
        print("ERROR " + str(exc))
        return 2
    print("%s: %d check(s) failed" % ("FAIL" if failed else "OK", failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
