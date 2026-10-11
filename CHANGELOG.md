# Changelog

All notable changes to this repository are listed here. The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). The first entry is the record tag `epub-3598`; from 1.1.0 on, the versions of the code follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

This repository was recreated with a new history on 2026-10-01; the earlier release, v1.0.0 of 2026-08-01, was not the version of record and is withdrawn. Its program archive opened an empty window.

## [Unreleased]

### Added

- `CITATION.cff` and `codemeta.json`: the Software Heritage identifier of the release `epub-3598`, the repository at the version of record, `swh:1:rel:0752922c9f06de5e5314bd2dd3bd99964420f135`.
- `README.md`: the section Citing the code under Citation, with that identifier and the badge of the Software Heritage archive.
- `ERRATA.md`: an index before the first entry, with the number of entries per class and one row per entry; `verification/check_metadata.py` holds it against the entries.
- `Makefile`, with one target per local check and `make verify` for all of them.
- `codemeta.json`: the addresses of the README, the changelog and the build instructions, and the software requirements.

### Changed

- `verification/check_metadata.py` compares the version with the first released section of `CHANGELOG.md` and passes over `[Unreleased]`.
- `README.md`: the identity line names the language of the program and its algorithms; the Contents table names every path at the root; every cited erratum links to its entry; the heading Licence is spelled as in the rest of the repository; Reproducing names `make verify` and what the checks need; two long paragraphs are split, their words unchanged; Corrections says that the repository is archived and read-only, and no longer that an error affecting a result is reported to the library.
- `CITATION.cff` and `codemeta.json`: the keywords are the keywords the thesis prints, followed by the subject terms of the program.
- `CONTRIBUTING.md`: the repository takes no pull requests.
- `.gitattributes`: the checks and the hook are left out of GitHub's language statistics.
- `slides/colloquium-handout-2021-07-05.de.pdf`: its document information gives title, author, subject and language, and opens with the title; pages and text are unchanged, and `NOTICE` declares the edit.

### Fixed

- `README.md`: the labels of the two diagrams keep their ends on GitHub at every zoom. Each label breaks its own lines, and the diagram raises Mermaid's wrapping width to 400 px, so that Mermaid wraps none of them; in Safari, a label that Mermaid wrapped could be measured too narrow at some page zooms and lose its end. The wording is unchanged.

## [1.1.0] - 2026-10-09

### Changed

- The three appendix files are relicensed from GPL-3.0-or-later to the MIT License by their author, the sole rights holder; copies received under the GPL keep that grant. Their code is unchanged.
- The program targets .NET 10 (`net10.0-windows`) instead of .NET 8.

### Added

- `verification/`: a claim check that runs the printed MD5 and RSA code on any operating system, a check of the appendix files against the printed listing, a check of the reading copy against the deposited file, and checks of the metadata and the links.
- Figures 32 to 36 of the thesis under `docs/figures/`, and the colloquium handout of 2021-07-05 under `slides/`.
- `ERRATA.md`, the known errors of the deposited thesis.
- `README.md`, `SECURITY.md`, `CONTRIBUTING.md`, the social card and the workflows.
- The author's ORCID iD in `CITATION.cff` and `codemeta.json`.

### Fixed

Statements in files that the record tag `epub-3598` holds, corrected here; the tag keeps them as they were:

- `NOTICE` and `REUSE.toml`: the marks of TH Köln and of the partner company stand in the headers of pages 1 to 71, and page 72, the back cover, carries only the mark of TH Köln; at the tag, `NOTICE` says that every page carries both, and `REUSE.toml` names only the page headers.
- `REUSE.toml`: `CITATION.cff` quotes the abstract of the thesis, as the README does, and `codemeta.json` does not; the tag says that `codemeta.json` quotes it.
- `publication/README.md`: Ghostscript's `/printer` settings downsample only the images of more than 450 ppi, not every image to 300 dpi; and the digest that the REST API reports for an asset carries the prefix `sha256:`, which the comparison with `SHA256SUMS` now strips.
- `codemeta.json`: the reference publication is typed `schema:Thesis` and its language is given as `schema:inLanguage`, because the CodeMeta 3.0 context defines neither `Thesis` nor `inLanguage`.

## [epub-3598] - 2026-10-01

### Added

- `publication/Torun_Password_Keyless_Authentication.pdf`, the deposited thesis, byte-identical with the file behind <https://doi.org/10.57683/EPUB-3598>: 7,035,230 bytes, SHA-256 `467ef888c8e499db7985edfd43b86148c564345b2479410f6e1a39ee2b4039ee`.
- `publication/Torun_Password_Keyless_Authentication_reading-copy.pdf`, a reading copy with downsampled images; not the version of record.
- `src/cMD5.cs`, `src/cRSA.cs` and `src/Raven One.cs`, Appendix I to III of the thesis, with their headers as printed and under GPL-3.0-or-later, as printed.
- `src/Program.cs` and the build files for .NET 8, written in 2026 under the MIT License so that the printed files compile.
- `CITATION.cff`, `codemeta.json`, `NOTICE`, `REUSE.toml` and the licence texts.

[Unreleased]: https://github.com/mtorun0x7cd/raven-one-simulink/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/mtorun0x7cd/raven-one-simulink/compare/epub-3598...v1.1.0
[epub-3598]: https://github.com/mtorun0x7cd/raven-one-simulink/releases/tag/epub-3598
