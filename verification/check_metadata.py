#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Mert Torun
# SPDX-License-Identifier: MIT
"""Check that the metadata files of this repository agree with each other.

Compared:
  * CITATION.cff and codemeta.json: the name of the software, its version and
    licence, the DOI, title and publication date of the thesis, and the
    author's ORCID iD in both author lists of each file (orcid in
    CITATION.cff, @id in codemeta.json);
  * the version of RavenOneSimuLink.csproj (Version, or InformationalVersion
    at the record tag) and the first version heading of CHANGELOG.md, passing
    over [Unreleased];
  * the BibTeX entry in README.md: it must parse, be a @mastersthesis of type
    "Bachelor's thesis", and carry the DOI, title and year of CITATION.cff;
  * date-released and date-published must be quoted in CITATION.cff, so that a
    plain YAML loader reads them as strings, as the CFF schema demands.

A file that does not exist yet (README.md, CHANGELOG.md) and an ORCID iD that
neither side names (as at the record tag) are reported as not compared.
Needs PyYAML.

Return values: 0 the files agree, 1 a difference, 2 a tool error.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPDX_URL = "https://spdx.org/licenses/"
DOI_URL = "https://doi.org/"


class ToolError(Exception):
    pass


def load_cff():
    try:
        import yaml
    except ImportError:
        raise ToolError("PyYAML is not installed")
    try:
        return yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ToolError("cannot read CITATION.cff: %s" % exc)


def load_codemeta():
    try:
        return json.loads((ROOT / "codemeta.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ToolError("cannot read codemeta.json: %s" % exc)


def project_version():
    try:
        text = (ROOT / "RavenOneSimuLink.csproj").read_text(encoding="utf-8")
    except OSError as exc:
        raise ToolError("cannot read RavenOneSimuLink.csproj: %s" % exc)
    match = re.search(r"<(Version|InformationalVersion)>([^<]+)</\1>", text)
    return match.group(2).strip() if match else None


def first_person(people):
    """The first entry of an author list, or an empty dict."""
    if isinstance(people, list) and people and isinstance(people[0], dict):
        return people[0]
    return {}


def bibtex_entry(readme):
    """(entry type, {field: value}) of the one ```bibtex block in README.md."""
    blocks = re.findall(r"^```bibtex\n(.*?)^```", readme, re.S | re.M)
    if len(blocks) != 1:
        return None, "README.md has %d ```bibtex block(s), not one" % len(blocks)
    text = blocks[0].strip()
    match = re.match(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text)
    if not match:
        return None, "the BibTeX block does not start with @type{key,"
    depth, end = 0, None
    for index, char in enumerate(text):
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                end = index
                break
    if end is None or text[end + 1:].strip():
        return None, "the braces of the BibTeX entry do not balance"
    fields = {}
    body = text[match.end():end]
    for field in re.finditer(r"(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}\s*,?", body):
        fields[field.group(1).lower()] = field.group(2)
    if not fields:
        return None, "the BibTeX entry has no field"
    return match.group(1).lower(), fields


def main():
    findings, notes = [], []
    try:
        cff = load_cff()
        meta = load_codemeta()
        csproj = project_version()
    except ToolError as exc:
        print("ERROR " + str(exc))
        return 2
    cite = cff.get("preferred-citation") or {}
    publication = meta.get("referencePublication") or {}

    def same(name, a, b):
        if a == b:
            print("PASS %s: %r" % (name, a))
        else:
            findings.append(name)
            print("FAIL %s: %r and %r" % (name, a, b))

    same("name", cff.get("title"), meta.get("name"))
    same("version", cff.get("version"), meta.get("version"))
    same("version-project", cff.get("version"), csproj)
    licence = meta.get("license", "")
    same("licence", cff.get("license"), licence[len(SPDX_URL):] if licence.startswith(SPDX_URL) else licence)
    same("doi", DOI_URL + str(cite.get("doi")), publication.get("@id"))
    same("thesis-title", cite.get("title"), publication.get("name"))
    same("date-published", cite.get("date-published"), publication.get("datePublished"))
    orcid = first_person(cff.get("authors")).get("orcid")
    for name, a, b in (
        ("orcid", orcid, first_person(meta.get("author")).get("@id")),
        ("orcid-thesis", first_person(cite.get("authors")).get("orcid"),
         first_person(publication.get("author")).get("@id")),
        ("orcid-citation", orcid, first_person(cite.get("authors")).get("orcid")),
    ):
        if a is None and b is None:
            notes.append("%s: neither side names an ORCID iD; not compared" % name)
        else:
            same(name, a, b)
    for key, value in (("date-released", cff.get("date-released")), ("date-published", cite.get("date-published"))):
        if not isinstance(value, str):
            findings.append(key + "-quoted")
            print("FAIL %s-quoted: a plain YAML loader reads %r as %s; quote it" % (key, value, type(value).__name__))

    changelog = ROOT / "CHANGELOG.md"
    if changelog.is_file():
        heading = re.search(r"^## \[(?!Unreleased\])([^\]]+)\]", changelog.read_text(encoding="utf-8"), re.M)
        same("version-changelog", cff.get("version"), heading.group(1) if heading else None)
    else:
        notes.append("CHANGELOG.md does not exist; its version was not compared")

    readme = ROOT / "README.md"
    if readme.is_file():
        kind, fields = bibtex_entry(readme.read_text(encoding="utf-8"))
        if kind is None:
            findings.append("bibtex")
            print("FAIL bibtex: " + fields)
        else:
            same("bibtex-type", kind, "mastersthesis")
            same("bibtex-thesis-type", fields.get("type"), "Bachelor's thesis")
            same("bibtex-doi", fields.get("doi"), cite.get("doi"))
            same("bibtex-url", fields.get("url"), cite.get("url"))
            same("bibtex-title", fields.get("title"), cite.get("title"))
            same("bibtex-year", fields.get("year"), str(cite.get("year")))
            if not fields.get("school"):
                findings.append("bibtex-school")
                print("FAIL bibtex-school: the entry names no school")
    else:
        notes.append("README.md does not exist; its BibTeX entry was not compared")

    for note in notes:
        print("NOTE " + note)
    print("%s: %d difference(s)" % ("FAIL" if findings else "OK", len(findings)))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
