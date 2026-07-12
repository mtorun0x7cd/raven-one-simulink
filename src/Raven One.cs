/*
 * TH Köln
 * Institut für Nachrichtentechnik (INT)
 * 
 * Raven One SimuLink
 * Raven One.cs
 * Main GUI definition written in C#
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
using System.Text;

namespace Raven_One_SimuLink
{
    public partial class Form1 : Form
    {
        private readonly cRSA m_rsa;

        public Form1()
        {
            InitializeComponent();
            m_rsa = new cRSA();
        }

        // Menu Strip: File -> Close
        private void closeToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Environment.Exit(0);
        }

        // Menu Strip: File -> Restart
        private void restartToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Application.Restart();
            Environment.Exit(0);
        }

        // Menu Strip: File -> Algorithms -> RSA
        private void overviewToolStripMenuItem_Click(object sender, EventArgs e)
        {
            RSA rsaForm = new RSA();
            rsaForm.Show();
        }

        // Menu Strip: File -> Algorithms -> MD5
        private void mD5ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MD5 md5Form = new MD5();
            md5Form.Show();
        }

        // Menu Strip: About
        private void aboutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            About aboutForm = new About();
            aboutForm.Show();
        }

        // Generate digest button
        private void runMD5Btn_Click(object sender, EventArgs e)
        {
            plainDigestBox.Clear();
            cipherDigestBox.Clear();
            detailBox.Clear();
            bool ptext = false;
            bool ctext = false;
            cMD5 md5Class = new cMD5();
            string plaintext = plaintextBox.Text;
            string ciphertext = ciphertextBox.Text;

            // Only compute digest if not empty
            if (!String.IsNullOrEmpty(plaintext))
            {
                byte[] plaintextBytes = Encoding.ASCII.GetBytes(plaintext);
                string plainDigest = cMD5.Calculate(plaintextBytes);
                plainDigestBox.Text = plainDigest;
                detailBox.Text += "Generating plaintext digest value using MD5 algorithm"
                    + Environment.NewLine + "Plaintext: " + plaintext + Environment.NewLine + "Plaintext as ASCII Codes: ";
                foreach (byte x in plaintextBytes)
                {
                    detailBox.Text += x.ToString() + " ";
                }
                detailBox.Text += Environment.NewLine + "Plaintext digest value: " + plainDigest + Environment.NewLine;
                ptext = true;
            }
            if (!String.IsNullOrEmpty(ciphertext))
            {
                byte[] ciphertextBytes = Encoding.ASCII.GetBytes(ciphertext);
                string cipherDigest = cMD5.Calculate(ciphertextBytes);
                cipherDigestBox.Text = cipherDigest;
                detailBox.Text += "Generating ciphertext digest value using MD5 algorithm"
                    + Environment.NewLine + "Ciphertext: " + ciphertext + Environment.NewLine + "Ciphertext as ASCII Codes: ";
                foreach (byte x in ciphertextBytes)
                {
                    detailBox.Text += x.ToString() + " ";
                }
                detailBox.Text += Environment.NewLine + "Ciphertext digest value: " + cipherDigest;
                ctext = true;
            }

            if (!ptext && !ctext)
            {
                detailBox.Text = "Error, please input plaintext or ciphertext values...";
            }
        }

        // Validate digest button
        private void validateDigestBtn_Click(object sender, EventArgs e)
        {
            detailBox.Clear();
            string cipherDigest = cipherDigestBox.Text;
            string validateDigest = validationDigestBox.Text;

            // Only compute validation if not empty
            if (!String.IsNullOrEmpty(cipherDigest) && !String.IsNullOrEmpty(validateDigest))
            {
                detailBox.Text += "Cipher digest: " + cipherDigest + Environment.NewLine
                    + "Validation digest: " + validateDigest + Environment.NewLine;
                byte[] cipherDigestBytes = Encoding.ASCII.GetBytes(cipherDigest);
                byte[] validationDigestBytes = Encoding.ASCII.GetBytes(validateDigest);
                detailBox.Text += "Cipher digest as ASCII codes: ";
                foreach (byte x in cipherDigestBytes)
                {
                    detailBox.Text += x.ToString() + " ";
                }
                detailBox.Text += Environment.NewLine + "Validation digest as ASCII codes: ";
                foreach (byte x in validationDigestBytes)
                {
                    detailBox.Text += x.ToString() + " ";
                }
                detailBox.Text += Environment.NewLine;
                bool valid = false;
                valid = String.Compare(cipherDigest, validateDigest) == 0 ? true : false;

                if (valid)
                {
                    detailBox.Text += "Both digest values are equal";
                }
                else
                {
                    detailBox.Text += "Both digest values are not equal";
                }
            }
            else
            {
                detailBox.Text += "Error, please compute valid cipher digest and input validation digest accordingly";
            }
        }

        // Encrypt button
        private void encryptBtn_Click(object sender, EventArgs e)
        {
            ciphertextBox.Clear();
            cipherDigestBox.Clear();
            detailBox.Clear();

            ciphertextBox.Text = m_rsa.encryptPlaintext(plaintextBox.Text);

            detailBox.Text +=
                "P-Value: " + m_rsa.getP() + Environment.NewLine
                + "Q-Value: " + m_rsa.getQ() + Environment.NewLine
                + "N = p * q Value: " + m_rsa.getN() + Environment.NewLine
                + "Phi(n) = (p-1)*(q-1) Value: " + m_rsa.getMPhiN() + Environment.NewLine
                + "Encryption key: " + m_rsa.getEncryptionKey() + Environment.NewLine
                + "Decryption key: " + m_rsa.getDecryptionKey() + Environment.NewLine
                + "Encrypted Value using p^e mod n which is "
                + plaintextBox.Text + "^" + m_rsa.getEncryptionKey() + " % " + m_rsa.getN()
                + Environment.NewLine + "Result: " + ciphertextBox.Text;
        }

        // Decrypt button
        private void decryptBtn_Click(object sender, EventArgs e)
        {
            plaintextBox.Clear();
            plainDigestBox.Clear();
            detailBox.Clear();

            plaintextBox.Text = m_rsa.decryptCiphertext(ciphertextBox.Text);

            detailBox.Text +=
                "P-Value: " + m_rsa.getP() + Environment.NewLine
                + "Q-Value: " + m_rsa.getQ() + Environment.NewLine
                + "N = p * q Value: " + m_rsa.getN() + Environment.NewLine
                + "Phi(n) = (p-1)*(q-1) Value: " + m_rsa.getMPhiN() + Environment.NewLine
                + "Encryption key: " + m_rsa.getEncryptionKey() + Environment.NewLine
                + "Decryption key: " + m_rsa.getDecryptionKey() + Environment.NewLine
                + "Decrypted Value using c^d mod n which is "
                + ciphertextBox.Text + "^" + m_rsa.getDecryptionKey() + " % " + m_rsa.getN()
                + Environment.NewLine + "Result: " + plaintextBox.Text;
        }
    }
}
