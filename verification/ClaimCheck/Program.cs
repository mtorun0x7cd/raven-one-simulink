// SPDX-FileCopyrightText: 2026 Mert Torun
// SPDX-License-Identifier: MIT
//
// The claim check of Raven One SimuLink.
//
// It runs the MD5 and RSA classes printed in the thesis (src/cMD5.cs and
// src/cRSA.cs, compiled unchanged) and checks every number that README.md and
// SECURITY.md state about them. The MD5 digests are compared with the MD5 of
// the .NET class library as a reference. Each check prints one line, PASS or
// FAIL, and the run ends with a summary. The exit code is 0 when every check
// holds and 1 otherwise. CI compares the output with expected-output.txt.

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Numerics;
using System.Text;
using Raven_One_SimuLink;

namespace ClaimCheck
{
    internal static class Program
    {
        private static int checks;
        private static int failures;

        private static void Check(string name, bool holds, string detail)
        {
            checks++;
            if (!holds)
            {
                failures++;
            }
            Console.WriteLine("{0} {1}: {2}", holds ? "PASS" : "FAIL", name, detail);
        }

        private static string Printed(byte[] input)
        {
            return cMD5.Calculate(input);
        }

        private static string Reference(byte[] input)
        {
            return Convert.ToHexString(System.Security.Cryptography.MD5.HashData(input)).ToLowerInvariant();
        }

        private static byte[] Ascii(string text)
        {
            return Encoding.ASCII.GetBytes(text);
        }

        private static byte[] Hex(string hex)
        {
            return Convert.FromHexString(hex);
        }

        private static string Raises(Func<string> action)
        {
            try
            {
                action();
                return "no exception";
            }
            catch (Exception exception)
            {
                return exception.GetType().Name;
            }
        }

        private static string Ranges(IEnumerable<int> values)
        {
            var parts = new List<string>();
            int[] sorted = values.OrderBy(v => v).ToArray();
            int i = 0;
            while (i < sorted.Length)
            {
                int j = i;
                while (j + 1 < sorted.Length && sorted[j + 1] == sorted[j] + 1)
                {
                    j++;
                }
                parts.Add(i == j ? sorted[i].ToString() : sorted[i] + "-" + sorted[j]);
                i = j + 1;
            }
            return string.Join(", ", parts);
        }

        private static void Md5Checks()
        {
            // RFC 1321, appendix A.5, "Test suite".
            var suite = new (string Input, string Digest)[]
            {
                ("", "d41d8cd98f00b204e9800998ecf8427e"),
                ("a", "0cc175b9c0f1b6a831c399e269772661"),
                ("abc", "900150983cd24fb0d6963f7d28e17f72"),
                ("message digest", "f96b697d7cb7938d525a2f31aaf161d0"),
                ("abcdefghijklmnopqrstuvwxyz", "c3fcd3d76192e4007dfb496cca67e13b"),
                ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "d174ab98d277d9f5a5611c2c9f419d9f"),
                ("12345678901234567890123456789012345678901234567890123456789012345678901234567890", "57edf4a22be3c955ac49da2e2107b67a"),
            };
            bool referenceHolds = suite.All(t => Reference(Ascii(t.Input)) == t.Digest);
            Check("reference-md5", referenceHolds,
                "the MD5 of the .NET class library gives all 7 digests of the RFC 1321 test suite");

            var wrong = suite.Where(t => Printed(Ascii(t.Input)) != t.Digest).ToList();
            bool onlyLong = wrong.Count == 1 && wrong[0].Input.Length == 62;
            Check("md5-rfc1321-suite", onlyLong,
                string.Format("cMD5 gives {0} of the 7 digests of the RFC 1321 test suite; wrong for: {1}",
                    suite.Length - wrong.Count,
                    string.Join(", ", wrong.Select(t => "the " + t.Input.Length + "-byte input"))));

            string admin = Printed(Ascii("admin"));
            Check("md5-admin", admin == "21232f297a57a5a743894a0e4a801fc3", "cMD5(\"admin\") = " + admin);

            // The first of the 64 operations for "admin", computed with the tables
            // and the rotation of cMD5 itself; the padded block is the one cMD5
            // builds for a 5-byte input.
            byte[] block = new byte[64];
            Array.Copy(Ascii("admin"), block, 5);
            block[5] = 0x80;
            Array.Copy(BitConverter.GetBytes(5L * 8), 0, block, 56, 8);
            uint[] k = cMD5.getK();
            int[] s = cMD5.getS();
            uint a = 0x67452301, b = 0xefcdab89, c = 0x98badcfe, d = 0x10325476;
            uint f = (b & c) | (~b & d);
            uint m0 = BitConverter.ToUInt32(block, 0);
            uint dtemp = d;
            d = c;
            c = b;
            b += cMD5.leftRotate(a + f + k[0] + m0, s[0]);
            a = dtemp;
            string blockHex = Convert.ToHexString(block).ToLowerInvariant();
            bool traceHolds = blockHex == "61646d696e80" + new string('0', 100) + "2800000000000000"
                && a == 0x10325476 && b == 0x5bd217a9 && c == 0xefcdab89 && d == 0x98badcfe;
            Check("md5-admin-trace", traceHolds, string.Format(
                "padded block {0}; after operation 0: A = 0x{1:x8}, B = 0x{2:x8}, C = 0x{3:x8}, D = 0x{4:x8}",
                blockHex, a, b, c, d));

            var defective = new List<int>();
            for (int length = 0; length < 256; length++)
            {
                byte[] input = Enumerable.Range(0, length).Select(i => (byte)((i * 31 + 7) & 0xFF)).ToArray();
                if (Printed(input) != Reference(input))
                {
                    defective.Add(length);
                }
            }
            bool defectHolds = defective.SequenceEqual(Enumerable.Range(0, 256).Where(n => n % 64 >= 56 && n % 64 <= 62));
            Check("md5-padding-defect", defectHolds, string.Format(
                "cMD5 differs from the reference for {0} of the lengths 0 to 255 bytes: {1} (length mod 64 from 56 to 62)",
                defective.Count, Ranges(defective)));

            string hallo = Printed(Ascii("Hallo"));
            Check("md5-figure-32-plain", hallo == "d1bf93299de1b68e6d382c893bf1215f", "cMD5(\"Hallo\") = " + hallo);

            string text = File.ReadAllText(Path.Combine(AppContext.BaseDirectory, "figure-32-ciphertext.txt")).TrimEnd('\n');
            int decoded;
            try
            {
                decoded = Convert.FromBase64String(text).Length;
            }
            catch (FormatException)
            {
                decoded = -1;
            }
            string cipher = Printed(Ascii(text));
            Check("md5-figure-32-cipher", text.Length == 344 && decoded == 256 && cipher == "fbae09a483269207be36423cbeaf2f92",
                string.Format("the {0} characters of figure-32-ciphertext.txt are Base64 for {1} bytes; cMD5 gives {2}",
                    text.Length, decoded, cipher));

            byte[] first = Hex(
                "d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f89" +
                "55ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5b" +
                "d8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0" +
                "e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70");
            byte[] second = Hex(
                "d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f89" +
                "55ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5b" +
                "d8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0" +
                "e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70");
            int differing = first.Zip(second, (x, y) => x != y).Count(z => z);
            string digestFirst = Printed(first);
            string digestSecond = Printed(second);
            Check("md5-collision-p31", differing == 6 && digestFirst == digestSecond
                    && digestFirst == "79054025255fb1a26e4bc422aef54eb4" && Reference(first) == digestFirst,
                string.Format("the two 128-byte blocks of thesis p. 31 differ in {0} bytes; cMD5 gives {1} and {2}",
                    differing, digestFirst, digestSecond));

            byte[] umlaut = Encoding.ASCII.GetBytes("\u00e4");
            Check("ascii-non-ascii", umlaut.Length == 1 && umlaut[0] == 63,
                "Encoding.ASCII, which Raven One.cs uses, turns U+00E4 (a with diaeresis) into byte " + umlaut[0] + ", '?'");
        }

        private static (BigInteger E, BigInteger D, BigInteger Phi) ConstructorRule(int p, int q)
        {
            // The rule of the cRSA constructor, applied to other primes; cRSA itself
            // has p = 11 and q = 17 fixed.
            BigInteger phi = (p - 1) * (q - 1);
            BigInteger e = 3;
            while (e < phi)
            {
                if (cRSA.gcd(e, phi) == 1)
                {
                    break;
                }
                e++;
            }
            return (e, (1 + (2 * phi)) / e, phi);
        }

        private static void RsaChecks()
        {
            var rsa = new cRSA();
            BigInteger p = rsa.getP(), q = rsa.getQ(), n = rsa.getN(), phi = rsa.getMPhiN();
            BigInteger e = rsa.getEncryptionKey(), d = rsa.getDecryptionKey();
            Check("rsa-parameters", p == 11 && q == 17 && n == 187 && phi == 160 && e == 3 && d == 107,
                string.Format("p = {0}, q = {1}, n = {2}, phi(n) = {3}, e = {4}, d = {5}", p, q, n, phi, e, d));
            Check("rsa-key-relation", (e * d) % phi == 1,
                string.Format("e * d = {0} = {1} * {2} + {3}", e * d, (e * d) / phi, phi, (e * d) % phi));

            var broken = Enumerable.Range(0, 187)
                .Where(m => rsa.decryptCiphertext(rsa.encryptPlaintext(m.ToString())) != m.ToString()).ToList();
            Check("rsa-round-trip", broken.Count == 0,
                broken.Count == 0 ? "decrypt(encrypt(m)) = m for every m from 0 to 186"
                    : "fails for " + Ranges(broken));

            string c42 = rsa.encryptPlaintext("42");
            string m42 = rsa.decryptCiphertext(c42);
            Check("rsa-example-42", c42 == "36" && m42 == "42",
                string.Format("encrypt(\"42\") = \"{0}\", decrypt(\"{0}\") = \"{1}\"", c42, m42));

            bool reduces = Enumerable.Range(187, 1000 - 187 + 1)
                .All(m => rsa.decryptCiphertext(rsa.encryptPlaintext(m.ToString())) == (m % 187).ToString());
            string c200 = rsa.encryptPlaintext("200");
            string m200 = rsa.decryptCiphertext(c200);
            Check("rsa-reduction", reduces && c200 == "140" && m200 == "13",
                string.Format("decrypt(encrypt(m)) = m mod 187 for every m from 187 to 1000; encrypt(\"200\") = \"{0}\", decrypt(\"{0}\") = \"{1}\"",
                    c200, m200));

            string cNeg = rsa.encryptPlaintext("-5");
            string mNeg = rsa.decryptCiphertext(cNeg);
            Check("rsa-negative", cNeg == "-125" && mNeg == "-5",
                string.Format("encrypt(\"-5\") = \"{0}\", decrypt(\"{0}\") = \"{1}\"", cNeg, mNeg));

            string onText = Raises(() => rsa.encryptPlaintext("Hallo"));
            string onEmpty = Raises(() => rsa.encryptPlaintext(""));
            Check("rsa-text-input", onText == "FormatException" && onEmpty == "FormatException",
                string.Format("encrypt(\"Hallo\") raises {0}; encrypt(\"\") raises {1}", onText, onEmpty));

            string onLarge = Raises(() => rsa.encryptPlaintext("2147483648"));
            Check("rsa-int32-range", onLarge == "OverflowException",
                "encrypt(\"2147483648\"), one more than Int32.MaxValue, raises " + onLarge);

            var own = ConstructorRule(11, 17);
            var other = ConstructorRule(11, 13);
            Check("rsa-closed-form", own.E == 3 && own.D == 107 && (own.E * own.D) % own.Phi == 1
                    && other.E == 7 && other.D == 34 && (other.E * other.D) % other.Phi == 118,
                string.Format("the constructor's rule d = (1 + 2 phi) / e gives e = {0}, d = {1} for p = 11, q = 17 (e * d mod {2} = {3}) "
                    + "and e = {4}, d = {5} for p = 11, q = 13 (e * d mod {6} = {7})",
                    own.E, own.D, own.Phi, (own.E * own.D) % own.Phi, other.E, other.D, other.Phi, (other.E * other.D) % other.Phi));
        }

        private static int Main()
        {
            Md5Checks();
            RsaChecks();
            Console.WriteLine(failures == 0
                ? string.Format("OK: {0} of {0} checks hold", checks)
                : string.Format("FAIL: {0} of {1} checks failed", failures, checks));
            return failures == 0 ? 0 : 1;
        }
    }
}
