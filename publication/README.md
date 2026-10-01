# Version of record

This folder holds the Bachelor's thesis "Password- / Keyless authentication" by Mert Torun (TH Köln; submitted and examined in 2021, published in 2026) as it was deposited, and a reading copy of it.

| File | Work | Record | Bytes | SHA-256 | Licence | Relation to the sources |
| --- | --- | --- | --- | --- | --- | --- |
| `Torun_Password_Keyless_Authentication.pdf` | Bachelor's thesis | ePublications TH Köln, document 3598, <https://doi.org/10.57683/EPUB-3598> | 7,035,230 | `467ef888c8e499db7985edfd43b86148c564345b2479410f6e1a39ee2b4039ee` | CC BY 4.0; material of third parties excepted, see [`NOTICE`](../NOTICE) | The version of record: byte-identical with the file the catalogue record serves |
| `Torun_Password_Keyless_Authentication_reading-copy.pdf` | Bachelor's thesis | not part of the record | 3,376,312 | `49f56da990b4a9d993c392e2c27df5439623df9d0e66edb76f7f4865c7461100` | as the version of record | Made from the version of record with downsampled images; not the version of record; do not cite it |

The deposited file differs from the thesis as submitted in 2021 in that the signature images on pages 70 and 71 and the author's matriculation number were removed; the restriction notice on page 2 and the blocking notice on page 71 remain, and the restriction they state ended on 2024-06-30.

## Verifying the files

### Without an account

1. In a clone of this repository, check both files against [`SHA256SUMS`](SHA256SUMS):

   ```sh
   cd publication
   sha256sum -c SHA256SUMS          # on macOS: shasum -a 256 -c SHA256SUMS
   ```

2. Hash the file the catalogue record serves and compare the result with the first line of `SHA256SUMS`:

   ```sh
   curl -sSfL -o deposited.pdf https://epb.bibl.th-koeln.de/files/3598/Torun_Password_Keyless_Authentication.pdf
   sha256sum deposited.pdf
   ```

3. The release `epub-3598` carries both files as assets. The public REST API gives the SHA-256 of each asset, which must equal `SHA256SUMS`:

   ```sh
   curl -sSf https://api.github.com/repos/mtorun0x7cd/raven-one-simulink/releases/tags/epub-3598 \
     | jq -r '.assets[] | "\(.digest)  \(.name)"'
   ```

### With plain git

The record tag `epub-3598` carries the author's SSH signature. The public key is published at <https://api.github.com/users/mtorun0x7cd/ssh_signing_keys>; its fingerprint is `SHA256:h0XIy0K+hRkQ921LjtoKu/jSPvvlP0r4BiAMuyEPIrI`.

```sh
key=$(curl -sSf https://api.github.com/users/mtorun0x7cd/ssh_signing_keys | jq -r '.[0].key')
echo "$key" | ssh-keygen -lf -                    # shows the fingerprint above
echo "info@mtorun0x7cd.com $key" > allowed_signers
git -c gpg.ssh.allowedSignersFile=allowed_signers tag -v epub-3598
```

### With a GitHub account

```sh
gh release verify epub-3598 --repo mtorun0x7cd/raven-one-simulink
```

The deposited PDF is untagged, that is, it has no structure for assistive technology, and it cannot change.

## How the reading copy was made

The reading copy is the deposited file passed through Ghostscript 10.08.0 with the `/printer` settings, which downsample its images to 300 dpi, and with one change to its metadata: the document subject, and the description in its XMP metadata, read "Reading copy of https://doi.org/10.57683/EPUB-3598; images downsampled; not the version of record; do not cite". Title, author and keywords are those of the deposited file. The reading copy is not PDF/A.

```sh
cat > docinfo.ps <<'EOF'
[ /Title (Password- / Keyless authentication)
  /Author (Mert Torun)
  /Subject (Reading copy of https://doi.org/10.57683/EPUB-3598; images downsampled; not the version of record; do not cite)
  /Keywords (Secure; Convenient; Passwordless; Distributed; Authentication; Passwordless Authentication; FIDO Alliance; FIDO2; FIDO UAF; U2F; CTAP; Two-Factor Authentication; Biometric Authentication; Public-Key Cryptography; RSA; MD5; Diffie-Hellman Key Exchange; Digital Signatures; Identity Management)
  /DOCINFO pdfmark
EOF
gs -q -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -dPDFSETTINGS=/printer \
   -o Torun_Password_Keyless_Authentication_reading-copy.pdf \
   Torun_Password_Keyless_Authentication.pdf docinfo.ps
```

Ghostscript writes the date of the run and a new document identifier into the file, so a second run gives a file with the same pages and text but other bytes. [`verification/check_reading_copy.py`](../verification/check_reading_copy.py) checks the reading copy against the deposited file: the same pages, text, outline, links, title, author and keywords, the subject above, and every page rendered within a small tolerance.
