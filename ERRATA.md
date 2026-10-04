# Errata: Password- / Keyless authentication

This file lists the known errors of the Bachelor's thesis "Password- / Keyless authentication" by Mert Torun (TH Köln, submitted and examined in 2021), published in 2026 on ePublications, a publication server of TH Köln, as document 3598 (DOI 10.57683/EPUB-3598, URN urn:nbn:de:hbz:832-epub4-35985). The deposited file in this repository is byte-identical with the file the library serves (SHA-256 467ef888c8e499db7985edfd43b86148c564345b2479410f6e1a39ee2b4039ee). It stays unchanged; corrections are recorded here only.

The section "Errata" lists errors of the author's text. The section "Properties of the record and the deposited file" lists what is wrong or missing in the catalogue record and in the file as a container. The section "Updates" lists web addresses printed in the work that no longer work or have moved. Every quotation is taken verbatim from the deposited file. A quotation may begin or end within a sentence; where it leaves out words inside it, or cuts off a web address or a reference entry, the omission is marked "…". Subscripts appear on the base line, as the file's text layer gives them (KD for K with subscript D). The file prints no page numbers. Its table of contents and its lists count pages exactly as the PDF does, so each location below gives one number, which is both the page by the table of contents and the PDF page.

To report an error, write to info@mtorun0x7cd.com and give the page and the passage.

## Errata

### E-001

- **Location:** p. 12 (PDF page 12), section 2.1 Knowledge-based, first paragraph after Figure 9.
- **Quoted text:** "Originating from Ali Baba and the Forty Thieves fairy tale (ref. [15]) based on real occurrences, the first recorded password in history is falsely known as open sesame."
- **Correction:** Delete "based on real occurrences" and "the first recorded password in history", or give sources for them. The reference [15] stands after the name of the tale; the work gives no source for the tale being based on real events or for its password being the first one on record.
- **Class:** claim not supported by the work's evidence
- **Evidence:** The work's p. 12 and its reference [15] (p. 69), the Wikipedia article on the tale.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-002

- **Location:** p. 15 (PDF page 15), section 2.3 Biometric-based, first paragraph.
- **Quoted text:** "Biometric authentication is sometimes also called realistic authentication (ref. [6], [7]) in computer science literature."
- **Correction:** Reference [7] does not support this sentence; the word "realistic" does not occur in it. Whether [6] uses the term has not been checked.
- **Class:** attribution
- **Evidence:** Reference [7] in its open-access version from the publisher (DOI 10.1007/s12652-019-01654-y, 21 pages): no occurrence of "realistic". Reference [6] (DOI 10.4018/978-1-5225-8100-0.ch008) is not openly available and was not read.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed for [7]; [6] not checked

### E-003

- **Location:** p. 16 (PDF page 16), section 2.3 Biometric-based, paragraph after Figure 13.
- **Quoted text:** "the necessary data should be in a specific form that permits subsequent processing and extraction of relevant future sets."
- **Correction:** Read "feature sets" for "future sets".
- **Class:** typographical
- **Evidence:** The work's p. 16: the sentence concerns the processing of the data acquired from a biometric trait.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-004

- **Location:** p. 18 (PDF page 18), chapter 3 Cryptography, paragraph "Cryptographic hash functions".
- **Quoted text:** "This security risk can be easily reduced by only storing the hash digest of each password, rendering any compromised password file useless for potential attackers."
- **Correction:** Storing only hash values reduces the risk, but it does not make a stolen password file useless: an attacker can hash candidate passwords and compare the results with the stored values offline, which is the dictionary attack on hash values that the work itself takes up on p. 19 (see E-006). To resist such attacks, [3] requires stored passwords to be salted and hashed with a key derivation function that makes each guess expensive.
- **Class:** factual, not affecting results
- **Evidence:** The work's p. 19: "a dictionary attack on our hash values". The work's reference [3] (NIST SP 800-63B), section 5.1.1.2: verifiers "SHALL store memorized secrets in a form that is resistant to offline attacks", and the key derivation function is to make each guess "by an attacker who has obtained a password hash file expensive".
- **Found:** 2026-09-28
- **Reported:** not reported
- **Status:** confirmed

### E-005

- **Location:** p. 19 (PDF page 19), chapter 3 Cryptography, paragraph "One-way functions".
- **Quoted text:** "Direct superior to this, the P versus NP problem is assuredly a complex topic of modern computer science. Which undoubtedly has to be resolved beforehand to scientifically prove or disprove one-way functions."
- **Correction:** P versus NP need not be resolved beforehand. A proof that one-way functions exist would itself prove P ≠ NP; conversely, P ≠ NP alone is not known to imply that one-way functions exist.
- **Class:** factual, not affecting results
- **Evidence:** If P = NP, every function computable in polynomial time could be inverted in polynomial time, because a proposed preimage is checked by computing the function once (the inversion problem lies in NP). One-way functions can therefore exist only if P ≠ NP; whether P ≠ NP suffices is an open question.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-006

- **Location:** p. 19 (PDF page 19), chapter 3 Cryptography, paragraph after "One-way functions".
- **Quoted text:** "even if a cracker would attempt to try and execute a dictionary attack on our hash values with or without a rainbow table, it would be easily countered by adding a custom salt value to the used public known hash function." and "However, a rainbow table contains plaintext passwords already with encryption. Ordinarily, these attacks are not working as there in common is a specific counter on the login attempts in web services."
- **Correction:** A rainbow table does not hold passwords together with their hash values; it holds chains of precomputed values, of which only the first and the last element are stored, and a password is recovered by recomputing a chain. A salt that differs for each stored password prevents the use of such precomputed tables, but it does not counter a dictionary attack on a single salted hash: an ordinary salt is stored with the hash, as [3] requires in section 5.1.1.2, and each guess is simply hashed together with it. A counter of failed logins limits guessing through the login itself; it does not protect hash values that have been stolen and are attacked offline.
- **Class:** factual, not affecting results
- **Evidence:** The work's reference [3] (NIST SP 800-63B), section 5.1.1.2: stored memorized secrets are to be "resistant to offline attacks", salted and hashed with a key derivation function that makes each guess expensive, and "Both the salt value and the resulting hash SHALL be stored"; section 5.2.2, "Rate Limiting (Throttling)", treats the limiting of failed attempts as protection "against online guessing attacks". The paper that introduced rainbow tables, "Making a Faster Cryptanalytic Time-Memory Trade-Off", Advances in Cryptology, CRYPTO 2003, pp. 617-630, DOI 10.1007/978-3-540-45146-4_36, sections 1 and 3: the chains of which "only the first and the last element" is stored, and the condition that all password hashes are computed the same way.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-007

- **Location:** p. 22 (PDF page 22), section 3.2.1 Private-Key Cryptography, last paragraph.
- **Quoted text:** "which is true for AES since it utilizes the public design process, which makes its source codes open for everyone. This in conclusion means that anyone can contribute to the AES algorithm and identify weaknesses to fix."
- **Correction:** AES was selected in a public process and is fixed in a published standard. Because its specification is public, anyone can analyse it and publish weaknesses; the algorithm itself does not take contributions or fixes.
- **Class:** factual, not affecting results
- **Evidence:** FIPS 197, Advanced Encryption Standard (NIST, November 2001), which specifies the algorithm; the work's p. 22 itself dates the introduction of AES to 2001.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-008

- **Location:** p. 23 (PDF page 23), section 3.2.1 Private-Key Cryptography, equations (3.2.1.2) and (3.2.1.3).
- **Quoted text:** "4 x 4 = 16 for our state (3.2.1.2) 192-bit divided by state = 12 rounds (3.2.1.3)"
- **Correction:** Delete (3.2.1.3). The number of rounds is not the key length divided by the 16 bytes of the state: that rule would give 8 rounds for 128-bit keys and 16 for 256-bit keys instead of the 10 and 14 listed on the same page. The standard fixes 10, 12 and 14 rounds for keys of 4, 6 and 8 words of 32 bits (Nk), which equals Nk + 6.
- **Class:** factual, not affecting results
- **Evidence:** FIPS 197, section 5 and its Figure 4 (Key-Block-Round Combinations); the list of round numbers on the same page.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-009

- **Location:** p. 26 (PDF page 26), section 3.2.2 Public-Key Cryptography, first paragraph after Figure 18.
- **Quoted text:** "Only the receiver should be in possession of the key KD using it to encrypt messages which were encrypted using KE."
- **Correction:** Read "decrypt messages" for "encrypt messages".
- **Class:** typographical
- **Evidence:** The work's p. 25: "this message can only be decrypted with the corresponding private key of the receiver".
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-010

- **Location:** p. 27 (PDF page 27), section 3.2.2, equation (3.2.2.8); p. 28 (PDF page 28), equation (3.2.2.16).
- **Quoted text:** p. 27: "Then select: e with gcd(d⋅e, φ(n)) = 1"; p. 28: "Select e with gcd(d⋅e,φ(n)) = gcd(7⋅e,64) = 1"
- **Correction:** Both conditions should read d⋅e mod φ(n) = 1, as (3.2.2.6) states; in the example, 7⋅e mod 64 = 1. As printed, the condition admits every odd e for d = 7 and φ(n) = 64, for example e = 3, with which the example would fail (20^3 mod 85 = 10, and 10^7 mod 85 = 5, not 20). The value chosen, e = 55, meets the correct condition (7⋅55 mod 64 = 1), and the worked example is correct: 20^55 mod 85 = 45 and 45^7 mod 85 = 20.
- **Class:** factual, not affecting results
- **Evidence:** Equation (3.2.2.6) on p. 27; recomputation of the numbers given on p. 28.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-011

- **Location:** p. 29 (PDF page 29), section 3.2.3 Digital Signatures, paragraph after Figure 20.
- **Quoted text:** "Which generally speaking means that even with unlimited computing power, the time needed would exceed the benefit from cracking the one-way function to retrieve the message."
- **Correction:** Inverting a one-way function must be infeasible for an attacker with bounded computing power; with unlimited computing power a preimage can always be found by trying inputs. Only information-theoretic security holds against unlimited computing power, and the work itself ascribes it to the one-time pad (p. 14), not to hash functions.
- **Class:** factual, not affecting results
- **Evidence:** The work's p. 14: "a system is even secure in exceptional cases where a potential adversary has unlimited computing power and time", said of the one-time pad.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-012

- **Location:** p. 31 (PDF page 31), section 3.2.3 Digital Signatures, first paragraph on the page.
- **Quoted text:** "Let’s take a look at an MD5 example of two strings in hexadecimal format, which show the (weak) collision resistance (ref. [24])"
- **Correction:** Read "which show that MD5 is not collision resistant". The two strings differ but have the same MD5 digest, which is a collision, the very event collision resistance should rule out. "Weak collision resistance" is the usual name of second-preimage resistance, which this example does not address.
- **Class:** factual, not affecting results
- **Evidence:** The two strings printed on p. 31, each four lines of 64 hexadecimal digits (128 bytes), recomputed: they differ in six bytes and both have the MD5 digest 79054025255fb1a26e4bc422aef54eb4, as the work states; the source is the work's reference [24].
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-013

- **Location:** p. 34 (PDF page 34), section 3.3.1 Diffie-Hellman Key Exchange, paragraph after Figure 25.
- **Quoted text:** "Even in case the traffic is recorded and later analyzed, there’s absolutely no way to figure out what the key was, even though the exchanges that created it may have been visible. This is where: perfect forward secrecy comes from. Nobody analyzing the traffic at a later date can break in because the key was never saved, never transmitted and never made visible anywhere."
- **Correction:** The secrecy of the agreed key against someone who records the exchange rests on the assumed hardness of the discrete logarithm, as the same paragraph says; it is computational, not absolute. Perfect forward secrecy means that a later compromise of long-term keys does not reveal session keys agreed earlier; Diffie-Hellman provides it when the secret values are generated for each session and then discarded.
- **Class:** factual, not affecting results
- **Evidence:** The same paragraph: "the modular log(x) is thought to be hard to compute". RFC 4949 (Internet Security Glossary, Version 2), entry "perfect forward secrecy".
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-014

- **Location:** p. 39 (PDF page 39), section 4.1 Universal Second Factor, first paragraph.
- **Quoted text:** "Its predecessor is the FIDO2 project, which is covered under the CTAP specification later on."
- **Correction:** Read "Its successor". FIDO2 followed U2F; within FIDO2, U2F is called CTAP1.
- **Class:** factual, not affecting results
- **Evidence:** The work's p. 41: "CTAP1 is the recent name for FIDO U2F"; the specifications overview of the FIDO Alliance (fidoalliance.org/specifications), which says that U2F was relabeled CTAP1 with the release of FIDO2 (seen 2026-09-28).
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-015

- **Location:** p. 42 (PDF page 42), chapter 5, Figure 32; appendix, p. 58 (cRSA.cs) and p. 61 (encryptBtn_Click).
- **Quoted text:** p. 42: "Figure 32, [F32]: Raven One SimuLink overview"; p. 58: "BigInteger t = Convert.ToInt32(text);" and "return Convert.ToString(BigInteger.Pow(t, (int)m_e) % m_n);"; p. 61: "ciphertextBox.Text = m_rsa.encryptPlaintext(plaintextBox.Text);"
- **Correction:** Figure 32 shows the plaintext "Hallo" and, in the field labelled Ciphertext, a string of 344 characters from the Base64 alphabet ending in "==", which decodes to 256 bytes; the detail panel in the figure shows only the computation of the two MD5 digests. The encrypt button passes the plaintext to encryptPlaintext (p. 61). That method converts it with Convert.ToInt32, which accepts only a decimal integer with an optional sign and raises an exception for "Hallo"; for an integer t it returns the remainder of t^3 modulo n = 187 as a decimal number (p = 11, q = 17, e = 3; p. 58), which contains no letters and no "=". The MD5 values in the figure, by contrast, are reproduced exactly by the MD5 code printed in the appendix: d1bf93299de1b68e6d382c893bf1215f for "Hallo" and fbae09a483269207be36423cbeaf2f92 for the 344-character string. The string in the Ciphertext field of Figure 32 therefore cannot have been produced by the encryption code printed in the work; the MD5 values are consistent with the printed code.
- **Class:** claim not supported by the work's evidence
- **Evidence:** The figure on p. 42, read from the embedded image: a transcription of the string in the Ciphertext field has exactly the MD5 digest that the figure shows as cipher digest, which confirms the transcription, and it begins and ends with the ASCII codes the figure's log lists. The appendix code, pp. 53-62. The .NET API reference for Convert.ToInt32(String): a FormatException is raised when the value "does not consist of an optional sign followed by a sequence of digits (0 through 9)". A port of the printed MD5 code reproduces both digests.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-016

- **Location:** p. 43 (PDF page 43), chapter 5, first paragraph; appendix, p. 58 (encryptPlaintext, decryptCiphertext).
- **Quoted text:** "You can encrypt and decrypt messages using RSA"
- **Correction:** The program printed in the appendix encrypts and decrypts decimal integers only. Text such as "Hallo" raises an exception (see E-015); the program has no step that codes a text as an integer, which p. 27 describes as part of RSA encryption. Because the program uses n = 187, of the non-negative integers only those below 187 come back unchanged after encryption and decryption; larger ones that fit in a 32-bit integer come back reduced modulo 187. For example, 200 is encrypted to 140 and decrypted to 13.
- **Class:** claim not supported by the work's evidence
- **Evidence:** The appendix, p. 58: encryptPlaintext and decryptCiphertext apply Convert.ToInt32 to the text and then raise it to the power e = 3 or d = 107 modulo n = 187; pp. 61-62: the encrypt and decrypt buttons pass the text boxes to them. The work's p. 27: "the sender codes the plaintext as an integer number". Recomputation: 200^3 mod 187 = 140 and 140^107 mod 187 = 13.
- **Found:** 2026-09-27
- **Reported:** not reported
- **Status:** confirmed

### E-017

- **Location:** p. 43 (PDF page 43), chapter 5, first paragraph and list of features.
- **Quoted text:** "at the same time generate a digital signature using the SimuLink for your generated messages." and "Digital signature generation and verification using the MD5 cryptographic hash function"
- **Correction:** Read "MD5 digest generation and comparison" for "Digital signature generation and verification". The printed program computes the MD5 digests of the plaintext and of the ciphertext (runMD5Btn_Click, p. 60) and compares two digest strings character by character (validateDigestBtn_Click, p. 61; described on p. 46). It applies no private key to a digest, so it creates and verifies no digital signature in the sense of p. 29.
- **Class:** claim not supported by the work's evidence
- **Evidence:** The work's p. 29: "Messages are signed by encrypting a hash value of the message also called the digest value."; the appendix code, pp. 59-62; p. 46: "There is no other special option done performing the validateDigestBtn_Click(...)."
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-018

- **Location:** p. 44 (PDF page 44), chapter 5, paragraph after Figure 33; p. 47 (PDF page 47), paragraph after Figure 36.
- **Quoted text:** p. 44: "In order to view a workflow of a method, refer to the latter pages for their corresponding uml activity diagrams."; p. 47: "For Raven One SimuLink, there are two main workflows also called algorithms — RSA and MD5, which are described as uml type activity diagrams."
- **Correction:** Only the RSA workflow is shown as an activity diagram (Figure 36, p. 47). The work contains no activity diagram for MD5 or for the main user interface.
- **Class:** factual, not affecting results
- **Evidence:** List of Figures, pp. 65-67, and the figures on pp. 44-47: Figures 33 to 35 are class diagrams (on Figure 35 see E-027), Figure 36 is the only activity diagram.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-019

- **Location:** p. 47 (PDF page 47), chapter 5, equation (5.3) and the paragraphs around it; appendix, pp. 57-58 (constructor of cRSA).
- **Quoted text:** p. 47: "These two large distinct prime numbers are constants in the SimuLink software, for testing purposes.", "d = 1 mod phi_n" and "The decryption key can be found using the extended euclidean algorithm - gcd."; p. 58: "m_p = 11;", "m_q = 17;" and "m_d = (1 + (2 * m_phi_n)) / m_e;"
- **Correction:** (5.3) should read d⋅e mod phi_n = 1, as (3.2.2.6) on p. 27 states. The printed program does not use the extended Euclidean algorithm; it computes d = (1 + 2⋅phi_n) / e. With its fixed primes 11 and 17 this gives e = 3 and d = 107, and 3⋅107 mod 160 = 1, so the program's keys are correct; the formula is not correct in general (for p = 11 and q = 13 it gives e = 7, d = 34 and 7⋅34 mod 120 = 118). The constants 11 and 17 are small primes, not large ones.
- **Class:** factual, not affecting results
- **Evidence:** Equation (3.2.2.6) on p. 27; the constructor on pp. 57-58; recomputation with the printed code's rules, including its integer division.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-020

- **Location:** p. 50 (PDF page 50), section 5.1 Jamestown Online, paragraph after Figure 38.
- **Quoted text:** "In this case, the fingerprint is your private-key while the public-key is transmitted to FIDO servers, used to authenticate on login procedures."
- **Correction:** The fingerprint is not the private key. The authenticator creates the key pair at registration and keeps the private key on the device; the fingerprint only lets the user unlock the use of that key locally and is not sent anywhere. Of the key pair, only the public key is sent to the server.
- **Class:** factual, not affecting results
- **Evidence:** The work's p. 40: "creating a Kpriv and Kpub on the FIDO Authenticator side and sending the Kpub as a verified key to the FIDO Server" and "the Kpriv which was created on registration to authenticate the user by his biometrics".
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-021

- **Location:** p. 52 (PDF page 52), chapter 6 Conclusion, first paragraph.
- **Quoted text:** "At this point of time, MFA — also called password-less authentication comes handy."
- **Correction:** Multi-factor authentication and passwordless authentication are not the same. MFA combines factors of different kinds and can include a password, as the work itself describes; passwordless authentication does without the password. A passwordless method can be multi-factor, but the two terms are not synonyms.
- **Class:** factual, not affecting results
- **Evidence:** The work's p. 12 (passwords as "a viable option for multi factor authentication"), p. 13 (two-factor authentication with a password and a token) and p. 20 (MFA as a combination of the techniques compared there).
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-022

- **Location:** p. 52 (PDF page 52), chapter 6 Conclusion, paragraph after Figure 40.
- **Quoted text:** "The covered algorithms for cryptographic functions like RSA, AES or MAC and the Raven One SimuLink Software do indeed show on a low-level base of software, that it’s possible and secure to enable these modern algorithms."
- **Correction:** The work does not cover MAC (message authentication codes); the term occurs nowhere else in it. The software demonstrates RSA and MD5, but it does not show that they are secure: it uses the primes 11 and 17, while p. 47 says the primes must be large in real use, and it uses MD5, which p. 30 calls "not considered secure anymore".
- **Class:** claim not supported by the work's evidence
- **Evidence:** A search of the whole text finds "MAC" on p. 52 only; the appendix, p. 58 (m_p = 11, m_q = 17); p. 47; p. 30.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-023

- **Location:** p. 54 (PDF page 54), chapter 7 Appendix, I. cMD5.cs, comment above the table K.
- **Quoted text:** "// K[i] := floor(232 × abs (sin(i + 1)))"
- **Correction:** Read floor(2^32 × abs(sin(i + 1))), with 2 raised to the power 32. The table of constants that follows is correct.
- **Class:** typographical
- **Evidence:** RFC 1321, section 3.4: the table element is the integer part of 4294967296 times abs(sin(i)), with i in radians; the printed constants agree with that table.
- **Found:** 2026-09-27
- **Reported:** not reported
- **Status:** confirmed

### E-024

- **Location:** pp. 54-55 (PDF pages 54-55), chapter 7 Appendix, I. cMD5.cs, method Calculate; the claim on p. 43 (PDF page 43), chapter 5.
- **Quoted text:** p. 54: "var addLength = (56 - ((input.Length + 1) % 64)) % 64; // calculates the new length with padding"; p. 55: "byte[] length = BitConverter.GetBytes(input.Length * 8); // bitconverter returns as little-endian"; p. 43: "Both algorithms MD5 and RSA were implemented using the corresponding Request for Comments (RFC, [A26]) by the Internet Engineering Task Force (IETF, [A27])."
- **Correction:** In C#, the remainder of a negative number is negative. For messages whose length in bytes is 56 to 62 modulo 64, addLength therefore becomes negative (from -1 to -7) instead of adding a further block; the buffer is one block too short, and the length field is written over the 0x80 padding byte or over the last message bytes. The printed code returns wrong MD5 digests for these lengths and does not follow RFC 1321 for them; for the other lengths tested, 0 to 255 bytes, its digests are correct. The number of zero bytes after 0x80 must be 55 minus the length modulo 64, taken modulo 64 as a non-negative number, for example `(119-input.Length%64)%64`. The code also writes the length in bits as a 32-bit number, while RFC 1321 requires 64 bits; for inputs of 2^29 bytes (512 MiB) or more it therefore does not follow RFC 1321 either. No digest printed in the work is affected: the inputs in Figure 32 are 5 and 344 bytes long.
- **Class:** factual, not affecting results
- **Evidence:** RFC 1321, sections 3.1 and 3.2 (padding is always performed, and a 64-bit representation of the length follows it); the C# language reference, arithmetic operators ("The sign of the non-zero remainder matches the sign of the left-hand operand"). A port of the printed code with this remainder rule, compared with a reference MD5 for every length from 0 to 255 bytes, is wrong for 56-62, 120-126, 184-190 and 248-254 and right for the other 228 lengths; with the corrected line it is right for all.
- **Found:** 2026-07-31; confirmed by recomputation on 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-025

- **Location:** chapter 9 List of Figures, pp. 65-67 (PDF pages 65-67), entries [F1], [F3] to [F6], [F24], [F37] and [F39]; the figures are on pp. 5, 7-9, 33, 49 and 51.
- **Quoted text:** "[F1] FIDO Alliance and Jamestown corporate identity collage FIDO Alliance logo taken from fidoalliance.org/wp-content/uploads/FIDO_Alliance_tagline.png in April 2021."; "[F3] Ponce City Market, Atlanta"; "[F4] Office space in Ponce City Market, Atlanta"; "[F5] Jamestown 31 Levi’s Plaza, San Francisco"; "[F6] Jamestown 31 Garco Mill, South Carolina"; "[F24] Cryptographic key visualized in binary format Taken from encrypted-tbn0.gstatic.com/images?q=tbn:…"; "[F37] Jamestown Online Kundenportal overview"; "[F39] Jamestown Online-Beitritt Zeichnungsschein overview"
- **Correction:** The work states no source for the photographs in Figures 3 to 6, for the partner company's logo in Figure 1 (the source given covers only the FIDO Alliance logo) or for the screenshots of the partner company's web applications in Figures 37 and 39; p. 49 names the address of the portal shown in Figure 37, online.jamestown.de. For Figure 24 the work gives only the address of an image search thumbnail, which does not identify the original. The sources of these figures are to be added here once they are known.
- **Class:** attribution
- **Evidence:** List of Figures, pp. 65-67: the other figures taken from third parties name a source, web sources together with the month of access.
- **Found:** 2026-09-24 (Figure 24: 2026-09-27)
- **Reported:** not reported
- **Status:** open; sources not yet determined

### E-026

- **Location:** p. 66 (PDF page 66), chapter 9 List of Figures, entry [F21].
- **Quoted text:** "[F21] Digital [F: Steps"
- **Correction:** Read "[F21] Digital Signature: Steps", the caption of Figure 21 on p. 30.
- **Class:** typographical
- **Evidence:** The caption on p. 30: "Figure 21, [F21]: Digital Signature: Steps".
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-027

- **Location:** p. 67 (PDF page 67), chapter 9 List of Figures, entry [F35].
- **Quoted text:** "[F35] Raven One SimuLink main gui uml type activity diagram"
- **Correction:** Read "class diagram" for "activity diagram", as the caption of Figure 35 on p. 46 has it.
- **Class:** typographical
- **Evidence:** The caption on p. 46: "Figure 35, [F35]: Raven One SimuLink main gui uml type class diagram"; p. 44 introduces Figures 33 to 35 as the three class diagrams.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-028

- **Location:** p. 68 (PDF page 68), chapter 11 References, entries [1], [2] and [3].
- **Quoted text:** [1]: "… NIST Special Publication 800-63-3, February 2020."; [2]: "… NIST Special Publication 800-63A, February 2020."; [3]: "… NIST Special Publication 800-63B, February 2020."
- **Correction:** All three publications date from June 2017, with updates as of 2 March 2020, for example "NIST Special Publication 800-63-3, June 2017 (includes updates as of 2 March 2020)." All three were withdrawn on 1 August 2025 and superseded by SP 800-63-4, SP 800-63A-4 and SP 800-63B-4; the work cites the versions of 2017.
- **Class:** factual, not affecting results
- **Evidence:** The publication pages of SP 800-63-3, SP 800-63A and SP 800-63B in the NIST Computer Security Resource Center (csrc.nist.gov/pubs/sp/800/63/3/upd2/final, /a/upd2/final and /b/upd2/final): each reads "Date Published: June 2017 (includes updates as of 03-02-2020)" and "Withdrawn on August 01, 2025" (seen 2026-09-28). The title page of SP 800-63B gives the same date, and its table of errata dates the update 2020-03-02.
- **Found:** 2026-09-24; [2] and [3] confirmed on 2026-09-28
- **Reported:** not reported
- **Status:** confirmed

### E-029

- **Location:** p. 68 (PDF page 68), chapter 11 References, entry [6].
- **Quoted text:** "[6] Tanwar, Rohit; Chowhan, Rahul Singh: Password-Less Authentication: Methods for User Verification and Identification to Login Securely Over Remote Sites. ResearchGate, January 2019."
- **Correction:** Chowhan, Rahul Singh; Tanwar, Rohit: Password-Less Authentication: Methods for User Verification and Identification to Login Securely Over Remote Sites. In: Machine Learning and Cognitive Science Applications in Cyber Security, IGI Global, 2019, pp. 190-212. DOI 10.4018/978-1-5225-8100-0.ch008. The order of the authors is reversed in the work, and ResearchGate is not the publisher.
- **Class:** factual, not affecting results
- **Evidence:** DOI lookup of 10.4018/978-1-5225-8100-0.ch008 (book chapter; authors in the order Chowhan, Tanwar).
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-030

- **Location:** p. 68 (PDF page 68), chapter 11 References, entry [7].
- **Quoted text:** "[7] Teh, Pin Shen; Zhang, Ning; Tan, Syh-Yuan; Shi, Qi; Khoh, Wee How; Nawaz, Raheel: Strengthen user authentication on mobile devices by using user's touch dynamics pattern. SpringerLink, December 2019."
- **Correction:** The article appeared in the Journal of Ambient Intelligence and Humanized Computing 11(10), pp. 4019-4039, 2020, published online on 24 December 2019. DOI 10.1007/s12652-019-01654-y. SpringerLink is the publisher's platform, not the venue.
- **Class:** factual, not affecting results
- **Evidence:** DOI lookup of 10.1007/s12652-019-01654-y.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-031

- **Location:** p. 69 (PDF page 69), chapter 11 References, entry [16].
- **Quoted text:** "[16] Jain, A. K.; Bolle, R.; Pankanti, S.: Biometrics Personal Identification in Network Society. Kluwer Academic Publications, 1999."
- **Correction:** The title is "Biometrics: Personal Identification in Networked Society", and A. K. Jain, R. Bolle and S. Pankanti are its editors, not its authors.
- **Class:** factual, not affecting results
- **Evidence:** DOI lookup of 10.1007/b117227 (book; the three named as editors; subtitle "Personal Identification in Networked Society").
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-032

- **Location:** p. 69 (PDF page 69), chapter 11 References, entry [19].
- **Quoted text:** "… Communication Theory of Secrecy Systems. Bell Technical Journal, 1949."
- **Correction:** The journal is the Bell System Technical Journal, vol. 28, no. 4, pp. 656-715, 1949. DOI 10.1002/j.1538-7305.1949.tb00928.x.
- **Class:** factual, not affecting results
- **Evidence:** DOI lookup of 10.1002/j.1538-7305.1949.tb00928.x.
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-033

- **Location:** p. 69 (PDF page 69), chapter 11 References, entry [22]; cited on p. 21, section 3.1.
- **Quoted text:** "[22] Kerckhoffs, A.: Kerckhoffs’ Principle. SpringerLink, 1883."
- **Correction:** As printed, the entry does not identify one document. It combines the author of the principle and the year 1883 with the later name of the principle and an online platform of the publisher Springer; on that platform, the title "Kerckhoffs’ Principle" belongs to an encyclopedia entry by another author (Encyclopedia of Cryptography and Security, Springer, 2011, DOI 10.1007/978-1-4419-5906-5_487). The principle cited on p. 21 goes back to A. Kerckhoffs, "La cryptographie militaire", Journal des sciences militaires, vol. IX, 1883.
- **Class:** reference could not be traced
- **Evidence:** The entry itself; a Crossref search for the title "Kerckhoffs’ Principle", which finds the encyclopedia entry of 2011 and its later editions (seen 2026-09-28); a transcription of the 1883 article, which gives its place of publication as Journal des sciences militaires, vol. IX, pp. 5-38 (January 1883) and pp. 161-191 (February 1883).
- **Found:** 2026-09-24
- **Reported:** not reported
- **Status:** confirmed

### E-034

- **Location:** p. 46 (PDF page 46), chapter 5 From inconvenient to convenient, Figure 35, in the image of the class diagram.
- **Quoted text:** "ecnryptBtn_Click(sender : object, e : EventArgs) : void"
- **Correction:** Read "encryptBtn_Click", the name of the handler of the Encrypt button in the code.
- **Class:** typographical
- **Evidence:** The listing on p. 61, chapter 7 Appendix, III. Raven One.cs: "private void encryptBtn_Click(object sender, EventArgs e)". The other handlers in Figure 35 are named as in the listing, for example "decryptBtn_Click".
- **Found:** 2026-10-01
- **Reported:** not reported
- **Status:** confirmed

### E-035

- **Location:** p. 45 (PDF page 45), chapter 5 From inconvenient to convenient, Figure 34, in the image of the class diagram.
- **Quoted text:** "- s : int[] { readyOnly }" and "- K : uint[] { readyOnly }"
- **Correction:** Read "{ readOnly }", the UML property of a field that keeps its value after initialisation; the code declares both arrays readonly.
- **Class:** typographical
- **Evidence:** The listing on pp. 53 and 54, chapter 7 Appendix, I. cMD5.cs: "static readonly int[] s = new int[64]" (p. 53) and "static readonly uint[] K = new uint[64]" (p. 54).
- **Found:** 2026-10-02
- **Reported:** not reported
- **Status:** confirmed

### E-036

- **Location:** p. 45 (PDF page 45), chapter 5 From inconvenient to convenient, Figure 34, in the image of the class diagram.
- **Quoted text:** "- getS() : int[]" and "- getK() : uint[]"
- **Correction:** Read "+ getS() : int[]" and "+ getK() : uint[]": both methods are public in the code.
- **Class:** factual, not affecting results
- **Evidence:** The listing on pp. 53 and 54, chapter 7 Appendix, I. cMD5.cs: "public static int[] getS()" (p. 53) and "public static uint[] getK()" (p. 54). The other members of Figure 34 carry the visibility the listing gives them: leftRotate and Calculate public, GetByteString private.
- **Found:** 2026-10-02
- **Reported:** not reported
- **Status:** confirmed

## Properties of the record and the deposited file

These are not errors of the author's text. The items on the catalogue record describe it as retrieved on 2026-10-01, after the library had worked on a request of 2026-09-27; each item says whether a correction was requested. The deposited file is unchanged.

### The deposited file

- **No page numbers.** The file prints no page numbers. The table of contents, the list of abbreviations and the list of figures refer to pages that equal the PDF page numbers; all entries of the table of contents, all 28 entries of the list of abbreviations and all 40 figure entries were checked. Found 2026-09-24.
- **No licence or identifiers in the file.** The file names no licence, DOI or URN. They are stated in the catalogue record: licence CC BY 4.0, DOI 10.57683/EPUB-3598, URN urn:nbn:de:hbz:832-epub4-35985. Found 2026-09-27.
- **Notices of 2021.** The file keeps the restriction notice on p. 2 ("The access to this thesis is restricted until 30th June 2024.") and the blocking notice on p. 71, which restricts access to the thesis and prohibits its publication. Both date the restriction to 30 June 2024. Found 2026-09-24.
- **Files not deposited.** The deposit consists of this PDF only. The appendix file "handed out with this thesis" (p. 43) and the file violetumleditor-2.0.1.jar (p. 44) are not part of it. Found 2026-09-27.
- **Container.** PDF 1.5, 72 pages, 7,035,230 bytes. The file is not PDF/A, is not tagged and declares no document language; its XMP metadata packet is empty, and its document information holds title, author, subject and keywords but no dates. It contains 66 internal links but no link to any of the web addresses it prints. Found 2026-09-27.

### The catalogue record

- **Dates.** The XMetaDissPlus export gives 2021-06-30 as the date of acceptance (dcterms:dateAccepted); that is the date printed on the thesis data page (p. 2) and on the author's declaration (p. 70). The degree certificate, an unpublished document, gives 2021-07-05 as the day the degree was obtained. Several exports give 2026-09-10, the day the record was created, as the date of issue, while the front door states 2026-09-14 as the date of online publication. Found 2026-09-24; correction of the date of acceptance was requested on 2026-09-27, unchanged on 2026-10-01; the date of issue was not raised.
- **CCS classes.** The record's two CCS entries, "Public key cryptosystems" under E.3 and "Authentication" under K.6.5, are unnumbered subentries; the OAI header of the record therefore carries no CCS set. Found 2026-09-24; adding the numbered classes E.3 and K.6.5 beside the subentries was requested on 2026-09-27, unchanged on 2026-10-01.
- **DOI metadata.** The DataCite record of the DOI has not been updated since its registration on 2026-09-14, so the corrections of 2026-10-01 have not reached it: its English abstract still lacks the markers ", [A1]" and ", [A2]", and it has no Spanish title or abstract. It names no contributors (the referees are missing), carries only the subject "004 Informatik", links to no related resource and gives only "Created 2026-09-10" as a date. Its derived citation types are article (BibTeX), RPRT (RIS), article-journal (CSL) and ScholarlyArticle, although its resource type is "Bachelor Thesis"; citations generated from the DOI therefore present the work as a journal article or a report, not as a Bachelor's thesis. Found 2026-09-24; the dates, the type, the subjects and a link to this repository were requested on 2026-09-27, and the missing referees were mentioned without a request; unchanged on 2026-10-01.
- **Languages.** The file prints title and abstract in English only (pp. 1-2). The German, French, Spanish and Turkish titles and abstracts in the record are translations and not part of the work as submitted and examined in 2021; the Spanish ones were added on 2026-10-01 at the author's request. The Turkish versions carry the language code "mul" (multiple languages), because the submission form offers no Turkish. Found 2026-09-24; whether "tur" can be set was asked on 2026-09-27, and on 2026-10-01 the code was still "mul".
- **Corrected on 2026-10-01.** At the author's request of 2026-09-27 the library corrected: the English abstract, which lacked the markers ", [A1]" and ", [A2]" that p. 2 prints after "Jamestown Online (JTO" and "Fast IDentity Online (FIDO" (they refer to the list of abbreviations, p. 63) and now matches p. 2; the entry of Jamestown US-Immobilien GmbH, Köln as contributing corporation, which the XMetaDissPlus export had turned into a second creator (dc:creator) although the work names the company as the employer of the second referee and as the setting of the thesis (pp. 1-2), not as an author, and which is now removed; "Single Sign-On", which stood both as a GND subject and as a free keyword although the work mentions single sign-on in one sentence (p. 13), now removed from both; and two line breaks within the single sentence of the note that names this repository (front door and MARC 21 field 500).
- **Record of the German National Library.** The German National Library took over the record on 2026-09-30, before these corrections. On 2026-10-01 its record still named Jamestown US-Immobilien GmbH, Köln in the statement of responsibility and as a further contributor with the role "Sonstige" (other), and still carried "Single Sign-On" as GND subject heading and as free keyword.

## Updates

Every web address printed in the work was requested on 2026-09-28. Addresses that still lead to the same page, if need be through a redirect to a language version or to the same host with "www", are not listed.

- **Figure 11, List of Figures, p. 65:** halls-of-valhalla.org/beta/articles/one-time-pad,42 returns "not found" (HTTP 404); the home page of that domain now redirects to an unrelated site.
- **Figure 24, List of Figures, p. 66:** the image search thumbnail address returns "not found" (HTTP 404); see E-025.
- **Figure 31, List of Figures, p. 67:** doubleoctopus.com/wp-content/uploads/2019/09/CTAP-authentication.png returns "not found" (HTTP 404).
- **Figure 29, List of Figures, p. 66:** upload.wikimedia.org/wikipedia/commons/thumb/4/47/Auth_flow4.svg.png is not valid as printed (HTTP 400), because a thumbnail address needs a size segment; the file is at commons.wikimedia.org/wiki/File:Auth_flow4.svg.
- **Reference [24], p. 69:** the host name of mscs.dal.ca/~selinger/md5collision does not resolve as printed, without "www"; the page is at www.mscs.dal.ca/~selinger/md5collision/.
- **Reference [5], p. 68:** microsoft.com/security/business/identity-access-management/passwordless-authentication now redirects to microsoft.com/security/business/solutions/passwordless-authentication, with a language segment added.
- **Reference [9], p. 68, and Figure 38, List of Figures, p. 67:** fidoalliance.org/fido2 now redirects to fidoalliance.org/passkeys/.
- **Figure 10, List of Figures, p. 65:** cloud.google.com/titan-security-key now redirects to cloud.google.com/security/products/titan-security-key.
- **RFC addresses, p. 43 and the code comments on pp. 53 and 56:** tools.ietf.org/html/rfc1321 and tools.ietf.org/html/rfc8017 now redirect to www.rfc-editor.org/info/rfc1321/ and www.rfc-editor.org/info/rfc8017/.

One address gave no usable answer and is not judged here: online.jamestown.de (reference [10], p. 68, and p. 49) accepted no connection, neither to an automated request on 2026-09-28 nor in a browser on 2026-10-01.
