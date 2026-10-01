#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Mert Torun
# SPDX-License-Identifier: MIT
"""Check the three appendix files against the listing printed in the thesis.

The deposited thesis prints its source code in chapter 7, Appendix I to III:
cMD5.cs on pp. 53-56, cRSA.cs on pp. 56-58 and Raven One.cs on pp. 58-62.
This script extracts those pages with pdftotext, cuts the listing at the
printed section marks "I.", "II." and "III.", and compares each listing with
the file under src/.

Normalisation, and why. pdftotext does not keep the indentation of the
listing, and a printed page cannot show trailing blanks. Each line is
therefore compared with all whitespace removed, and empty lines are dropped
on both sides. Everything else counts: every token, every character of every
comment, and the order of the lines.

What is compared:
  * the code below the header comment ("the body"), always;
  * the header comment, in one of two ways. With --printed-headers the whole
    header must be as printed, which is the state at the record tag
    epub-3598. Without it, the header lines above the SPDX tags must be the
    first lines of the printed header, which is the state after the code was
    relicensed under the MIT License.

    check_appendix.py                     the files in the working tree
    check_appendix.py --rev epub-3598 --printed-headers
                                          the files as committed at a revision
    check_appendix.py --selftest          change one token in each file and
                                          prove that the check fails

Return values: 0 every file holds, 1 a difference, 2 a tool error (a missing
PDF, a missing section mark, pdftotext not installed).
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "publication" / "Torun_Password_Keyless_Authentication.pdf"
FIRST_PAGE, LAST_PAGE = 53, 62

# (file, section mark as printed, pages of the listing)
LISTINGS = [
    ("cMD5.cs", "I.", "pp. 53-56"),
    ("cRSA.cs", "II.", "pp. 56-58"),
    ("Raven One.cs", "III.", "pp. 58-62"),
]
BODY_START = "using System;"
SPDX_TAG = "SPDX-"


class ToolError(Exception):
    pass


def squeeze(lines):
    """The lines with all whitespace removed, empty ones dropped."""
    out = []
    for line in lines:
        packed = "".join(line.split())
        if packed:
            out.append(packed)
    return out


def printed_listings(pdf):
    try:
        text = subprocess.run(
            ["pdftotext", "-layout", "-f", str(FIRST_PAGE), "-l", str(LAST_PAGE), str(pdf), "-"],
            check=True, capture_output=True, text=True, encoding="utf-8").stdout
    except FileNotFoundError:
        raise ToolError("pdftotext is not installed (poppler-utils)")
    except subprocess.CalledProcessError as exc:
        raise ToolError("pdftotext failed on %s: %s" % (pdf, exc.stderr.strip()))
    lines = text.replace("\f", "\n").splitlines()
    marks = {}
    for index, line in enumerate(lines):
        for name, mark, _ in LISTINGS:
            if re.fullmatch(r"\s*%s\s+%s\s*" % (re.escape(mark), re.escape(name)), line):
                if name in marks:
                    raise ToolError("the section mark for %s appears twice" % name)
                marks[name] = index
    missing = [name for name, _, _ in LISTINGS if name not in marks]
    if missing:
        raise ToolError("no section mark found for %s on pp. %d-%d" % (", ".join(missing), FIRST_PAGE, LAST_PAGE))
    order = [marks[name] for name, _, _ in LISTINGS]
    if order != sorted(order):
        raise ToolError("the section marks are not in the order I, II, III")
    listings = {}
    for position, (name, _, _) in enumerate(LISTINGS):
        start = marks[name] + 1
        end = order[position + 1] if position + 1 < len(order) else len(lines)
        listings[name] = lines[start:end]
    return listings


def split_file(text):
    """(header lines, body lines) of a source file."""
    text = text.lstrip("\ufeff")
    at = text.find(BODY_START)
    if at < 0:
        raise ToolError("no line starting the code (%r)" % BODY_START)
    return text[:at].splitlines(), text[at:].splitlines()


def split_printed(lines):
    joined = "\n".join(lines)
    at = joined.find(BODY_START)
    if at < 0:
        raise ToolError("the printed listing has no line %r" % BODY_START)
    return joined[:at].splitlines(), joined[at:].splitlines()


def first_difference(expected, actual):
    for index, (a, b) in enumerate(zip(expected, actual)):
        if a != b:
            return index, a, b
    if len(expected) != len(actual):
        index = min(len(expected), len(actual))
        return (index, expected[index] if index < len(expected) else "(end)",
                actual[index] if index < len(actual) else "(end)")
    return None


def compare(name, pages, printed, text, printed_headers):
    """Findings for one file, as a list of strings; empty when it holds."""
    findings = []
    printed_header, printed_body = split_printed(printed)
    header, body = split_file(text)
    want, have = squeeze(printed_body), squeeze(body)
    diff = first_difference(want, have)
    if diff:
        findings.append("%s: the code differs from the listing (%s) at code line %d: printed %r, file %r"
                        % (name, pages, diff[0] + 1, diff[1], diff[2]))
    want_header = squeeze(printed_header)
    have_header = squeeze(header)
    if printed_headers:
        diff = first_difference(want_header, have_header)
        if diff:
            findings.append("%s: the header is not as printed, at header line %d: printed %r, file %r"
                            % (name, diff[0] + 1, diff[1], diff[2]))
    else:
        above = []
        for line in have_header:
            if SPDX_TAG in line:
                break
            above.append(line)
        else:
            findings.append("%s: the header carries no SPDX tag" % name)
        if above and above != want_header[:len(above)]:
            diff = first_difference(want_header[:len(above)], above)
            findings.append("%s: the header lines above the SPDX tags are not the printed ones, at line %d: "
                            "printed %r, file %r" % (name, diff[0] + 1, diff[1], diff[2]))
        if not above:
            findings.append("%s: no printed header line stands above the SPDX tags" % name)
    return findings, len(want), len(want_header)


def read_sources(rev):
    sources = {}
    for name, _, _ in LISTINGS:
        if rev:
            try:
                blob = subprocess.run(["git", "-C", str(ROOT), "show", "%s:src/%s" % (rev, name)],
                                      check=True, capture_output=True).stdout
            except subprocess.CalledProcessError as exc:
                raise ToolError("git show %s:src/%s failed: %s" % (rev, name, exc.stderr.decode().strip()))
            sources[name] = blob.decode("utf-8")
        else:
            path = ROOT / "src" / name
            try:
                sources[name] = path.read_text(encoding="utf-8")
            except OSError as exc:
                raise ToolError("cannot read %s: %s" % (path, exc))
    return sources


def run(rev, printed_headers, emit):
    if not PDF.is_file():
        raise ToolError("the deposited PDF is missing: %s" % PDF)
    listings = printed_listings(PDF)
    sources = read_sources(rev)
    failed = 0
    for name, _, pages in LISTINGS:
        findings, body_lines, header_lines = compare(name, pages, listings[name], sources[name], printed_headers)
        if findings:
            failed += 1
            for finding in findings:
                emit("FAIL " + finding)
        else:
            emit("PASS %s: %d code lines as printed (%s)%s" % (
                name, body_lines, pages,
                ", header as printed (%d lines)" % header_lines if printed_headers
                else ", printed header lines kept above the SPDX tags"))
    return failed


def selftest(emit):
    """Change one token per file and prove the comparison fails; prove the unchanged files pass.

    The mode follows the files: a header without SPDX tags is checked as printed
    (the state at epub-3598), one with SPDX tags as relicensed. Each file gets
    one change in its code and one in its header line "Author: Mert Torun",
    which stands above the SPDX tags in both states."""
    listings = printed_listings(PDF)
    sources = read_sources(None)
    mutations = {
        "cMD5.cs": ("0xd76aa478", "0xd76aa479"),
        "cRSA.cs": ("m_p = 11;", "m_p = 13;"),
        "Raven One.cs": ("Both digest values are equal", "Both digest values are same"),
    }
    header_mutation = ("Author: Mert Torun", "Author: Mert Toron")
    bad = 0
    for name, _, pages in LISTINGS:
        header, _ = split_file(sources[name])
        printed_headers = not any(SPDX_TAG in line for line in header)
        clean, _, _ = compare(name, pages, listings[name], sources[name], printed_headers)
        if clean:
            emit("FAIL self-test: %s does not hold unchanged: %s" % (name, clean[0]))
            bad += 1
            continue
        for old, new in (mutations[name], header_mutation):
            if sources[name].count(old) != 1:
                raise ToolError("the self-test token %r is not unique in %s" % (old, name))
            changed, _, _ = compare(name, pages, listings[name], sources[name].replace(old, new), printed_headers)
            if not changed:
                emit("FAIL self-test: %s still holds after %r became %r" % (name, old, new))
                bad += 1
            else:
                emit("PASS self-test: %s fails after %r became %r" % (name, old, new))
    return bad


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--rev", help="read src/ as committed at this git revision")
    parser.add_argument("--printed-headers", action="store_true",
                        help="demand the whole header as printed (the state at epub-3598)")
    parser.add_argument("--selftest", action="store_true", help="prove that one changed token is found")
    args = parser.parse_args(argv[1:])
    try:
        if args.selftest:
            bad = selftest(print)
        else:
            bad = run(args.rev, args.printed_headers, print)
    except ToolError as exc:
        print("ERROR " + str(exc))
        return 2
    print("%s: %d of %d file(s) failed" % ("FAIL" if bad else "OK", bad, len(LISTINGS)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
