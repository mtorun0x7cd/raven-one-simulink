/*
 * TH Köln
 * Institut für Nachrichtentechnik (INT)
 * 
 * Raven One SimuLink
 * cRSA.cs
 * RSA Class definition written in C#
 * 
 * Author: Mert Torun, M.Sc. (mtorun0x7cd)
 * Contact: info@mtorun0x7cd.com
 * Website: mtorun0x7cd.com
 * Date: 2021-04 - 2021-06
 *
 * SPDX-License-Identifier: MIT
 * Originally released under GPL-3.0-or-later (2021 B.Sc. thesis); relicensed to MIT
 * by the author (sole copyright holder). See NOTICE.
 */
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Numerics;

namespace Raven_One_SimuLink
{
    /// <summary>
    /// RFC for RSA at https://tools.ietf.org/html/rfc8017
    /// </summary>
    class cRSA
    {
        private BigInteger m_p;
        private BigInteger m_q;
        private BigInteger m_n; // n = p * q
        private BigInteger m_phi_n; // phi(n) = (p-1)*(q-1)
        private BigInteger m_e; // Encryption key, public key
        private BigInteger m_d; // Decrption key, private key

        // Greatest common divisor function implemented using euclidean algorithm, see mathematics for more details
        public static BigInteger gcd(BigInteger a, BigInteger b)
        {
            while (a != 0 && b != 0)
            {
                if (a > b)
                {
                    a %= b;
                }
                else
                {
                    b %= a;
                }
            }

            return a | b;
        }

        public BigInteger getP()
        {
            return m_p;
        }
        public BigInteger getQ()
        {
            return m_q;
        }
        public BigInteger getMPhiN()
        {
            return m_phi_n;
        }
        public BigInteger getN()
        {
            return m_n;
        }

        public BigInteger getEncryptionKey()
        {
            return m_e;
        }

        public BigInteger getDecryptionKey()
        {
            return m_d;
        }

        // Constructor
        // p and q have to be large distinct prime numbers (!)
        public cRSA()
        {
            m_p = 11;
            m_q = 17;
            m_n = m_p * m_q;
            m_phi_n = (m_p - 1) * (m_q - 1);

            // for checking that 1 < e < phi(n) 
            // and gcd(e, phi(n)) = 1
            m_e = 3;
            BigInteger track;
            while (m_e < m_phi_n)
            {
                track = gcd(m_e, m_phi_n);

                if (track == 1)
                {
                    break;
                }
                else
                {
                    m_e++;
                }
            }

            m_d = (1 + (2 * m_phi_n)) / m_e;
        }

        public string encryptPlaintext(string text)
        {
            BigInteger t = Convert.ToInt32(text);
            return Convert.ToString(BigInteger.Pow(t, (int)m_e) % m_n);
        }

        public string decryptCiphertext(string text)
        {
            BigInteger t = Convert.ToInt32(text);
            return Convert.ToString(BigInteger.Pow(t, (int)m_d) % m_n);
        }
    }
}
