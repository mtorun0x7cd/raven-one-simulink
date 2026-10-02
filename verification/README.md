# Verification

The checks in this folder test what the repository states about the thesis and its program. Each prints one line per check, PASS or FAIL, and returns 0 when everything holds, 1 on a finding and 2 when it could not run. The workflows `claims.yml` and `checks.yml` run them on every push.

| Check | What it tests | Needs |
| --- | --- | --- |
| `ClaimCheck/` | Each claim of the table under Reproducing in `README.md`, about the MD5 and RSA code: it compiles `src/cMD5.cs` and `src/cRSA.cs` unchanged and runs them; the MD5 of the .NET class library is the reference | .NET SDK 10 (see `global.json`), any operating system |
| `check_appendix.py` | The three appendix files against the listing printed on pp. 53-62 of the deposited thesis | Python 3, `pdftotext` (poppler-utils) |
| `check_reading_copy.py` | The reading copy against the deposited file | Python 3, poppler-utils, `qpdf` |
| `check_metadata.py` | `CITATION.cff`, `codemeta.json`, the project file, `CHANGELOG.md` and the BibTeX entry in `README.md` against each other | Python 3, PyYAML |

## The claim check

```sh
dotnet run --project verification/ClaimCheck -c Release > claims.txt
diff verification/expected-output.txt claims.txt
```

`expected-output.txt` is the output of a run in which all 18 checks hold. The MD5 and RSA classes are compiled as they stand in `src/`. They carry the directive `using System.Windows.Forms;` without using anything from that namespace, and Windows Forms exists only on Windows, so `ClaimCheck/CrossPlatformShim.cs` declares an empty namespace of that name. Nothing else is added to them.

`figure-32-ciphertext.txt` holds the 344 characters that the Ciphertext field of Figure 32 shows (thesis, p. 42; image object 127 of the deposited PDF). They are transcribed from the list "Ciphertext as ASCII Codes" in the detail panel of the same figure, whose digits leave no doubt, unlike glyphs such as I and l. The transcription is confirmed by its MD5, which equals the cipher digest the figure shows.

## The appendix check

```sh
python3 verification/check_appendix.py                                     # the files as they stand
python3 verification/check_appendix.py --rev epub-3598 --printed-headers   # the record tag
python3 verification/check_appendix.py --selftest                          # one changed token must fail
```

The script cuts the listing at the section marks "I.", "II." and "III." of the appendix and compares each file line by line with all whitespace removed, because the PDF text keeps no indentation. At the record tag the whole header must be as printed; afterwards the header lines above the SPDX tags must be. The code below the header must be as printed in both states.
