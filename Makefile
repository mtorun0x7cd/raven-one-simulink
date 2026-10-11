# SPDX-FileCopyrightText: 2026 Mert Torun
# SPDX-License-Identifier: MIT
#
# Build the program and run the local checks.
#
#   make build          build the program with the .NET SDK that global.json
#                       names; the output goes to artifacts/
#   make claims         build and run the claim check and compare its output
#                       with verification/expected-output.txt
#   make record         check publication/ against SHA256SUMS
#   make appendix       check the appendix files against the printed listing,
#                       and the check itself on one changed token per file
#                       (needs pdftotext)
#   make reading-copy   check the reading copy against the deposited file
#                       (needs poppler-utils and qpdf)
#   make metadata       check that CITATION.cff, codemeta.json, the project
#                       file, CHANGELOG.md, the README's BibTeX entry and the
#                       errata index agree (needs PyYAML)
#   make verify         claims, record, appendix, reading-copy and metadata
#
# The link check is not among the targets: it needs the network, and CI runs
# it. Set PYTHON=<path> or DOTNET=<path> where the default does not fit, as in
# make metadata PYTHON=.venv/bin/python3. All output goes to artifacts/, which
# git ignores; no target deletes anything.

SHELL       := /bin/bash
.SHELLFLAGS := -euo pipefail -c

PYTHON ?= python3
DOTNET ?= dotnet

export PYTHONDONTWRITEBYTECODE := 1

.PHONY: build claims record appendix reading-copy metadata verify

build:
	$(DOTNET) build RavenOneSimuLink.csproj -c Release

# The build is a step of its own, as in claims.yml, so that no message of the
# .NET SDK reaches the output that is compared.
claims:
	mkdir -p artifacts
	$(DOTNET) build verification/ClaimCheck -c Release --nologo
	$(DOTNET) run --project verification/ClaimCheck -c Release --no-build > artifacts/claims.txt
	diff -u verification/expected-output.txt artifacts/claims.txt

record:
	cd publication && if command -v sha256sum >/dev/null; then sha256sum -c SHA256SUMS; \
		else shasum -a 256 -c SHA256SUMS; fi

appendix:
	$(PYTHON) verification/check_appendix.py
	$(PYTHON) verification/check_appendix.py --selftest

reading-copy:
	$(PYTHON) verification/check_reading_copy.py

metadata:
	$(PYTHON) verification/check_metadata.py

verify: claims record appendix reading-copy metadata
