# Security policy

## Scope

This repository holds the Bachelor's thesis "Password- / Keyless authentication" as deposited, and Raven One SimuLink, the program written for it in 2021 to demonstrate RSA and MD5. Neither is developed further, and no version receives security updates. The program is a demonstration implementation, not cryptography for use: do not use it, or code from it, to protect data.

## What to report privately

- A secret, a credential or personal data committed to this repository by mistake.
- A file that is not what this repository says it is, for example a PDF whose SHA-256 differs from `publication/SHA256SUMS`.
- A weakness of the workflows under `.github/` that could let someone change what the repository publishes.

## How to report

Write to [info@mtorun0x7cd.com](mailto:info@mtorun0x7cd.com), naming the file, the problem and how to see it. E-mail is the only route: the repository takes no issues, and private vulnerability reporting is not enabled.

## What is not a vulnerability

The weaknesses of the program are known and documented, and they are part of the work of 2021. They are not fixed, because the code is kept as the thesis prints it:

- MD5 is not collision resistant; the thesis itself shows a collision (p. 31).
- The MD5 code returns wrong digests for messages whose length is 56 to 62 bytes modulo 64, and for messages of 2^29 bytes or more it does not follow RFC 1321.
- The RSA code uses the fixed primes 11 and 17, so n = 187, applies no padding and accepts only decimal integers. An m of 187 or more comes back reduced modulo 187, a negative m gives a negative result, text or an empty field raises a FormatException, and a number beyond the 32-bit range an OverflowException.
- The window encodes its text fields as ASCII, so every character outside ASCII becomes "?".

The README describes each of them under Limitations, and `verification/ClaimCheck` checks their numbers, except the 2^29-byte limit, which follows from the code. An error in the text of the thesis is a correction, not a security report; see the README, section Corrections.

## What to expect

Reports are read. A reply or a fix is not guaranteed, because the repository is not maintained as software.
