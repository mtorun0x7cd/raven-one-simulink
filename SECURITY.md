# Security Policy

## Status

Raven One SimuLink is an archived academic artifact, retained for reference. It
is not actively maintained, and no security updates are issued.

## Not for production use

This software is a teaching aid that deliberately trades security for
transparency. It must not be used to protect real data.

## Known Limitations

The cryptography is intentionally insecure, for pedagogical clarity:

- **MD5** is cryptographically broken; practical collisions have been known
  since 2004. It is implemented here only to illustrate the Merkle–Damgård
  construction.
- The **MD5** padding computation mis-sizes the message buffer for inputs
  whose byte length is 56–62 modulo 64: the length field then overwrites the
  0x80 terminator instead of extending the message by a further block, and the
  digest returned for those inputs does not match RFC 1321. No error is
  raised. The defect is preserved as part of the 2021 record and is not
  corrected here.
- The **RSA** implementation uses fixed, trivially small demo primes
  (p = 11, q = 17), performs no padding (no PKCS #1 / OAEP), and operates on
  integer messages. It is correct only for a decimal integer message m with
  0 ≤ m < n = 187; a larger value decrypts to m mod 187 rather than to the
  original message, with no error raised, and non-numeric input raises an
  unhandled `FormatException`. It demonstrates the mathematics of RSA; it
  provides no confidentiality.

For real-world cryptography, use a vetted library and modern primitives
(for example, SHA-256/SHA-3 for hashing and RSA-OAEP or an ECC scheme for
public-key operations).

## Reporting

To report a substantive issue worth recording, contact <info@mtorun0x7cd.com>.
Given the archived status of the project, a fix or response is not guaranteed.
