/*
 * TH Köln
 * Institut für Nachrichtentechnik (INT)
 *
 * Raven One SimuLink
 * Program.cs
 * Application entry point
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
using System.Windows.Forms;

namespace Raven_One_SimuLink
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());
        }
    }

    public class RSA : Form
    {
    }

    public class MD5 : Form
    {
    }

    public class About : Form
    {
    }

    public partial class Form1 : Form
    {
        public TextBox plaintextBox = new TextBox();
        public TextBox ciphertextBox = new TextBox();
        public TextBox plainDigestBox = new TextBox();
        public TextBox cipherDigestBox = new TextBox();
        public TextBox detailBox = new TextBox();
        public TextBox validationDigestBox = new TextBox();

        public Button runMD5Btn = new Button();
        public Button validateDigestBtn = new Button();
        public Button encryptBtn = new Button();
        public Button decryptBtn = new Button();

        private void InitializeComponent()
        {
            this.SuspendLayout();
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Name = "Form1";
            this.Text = "Raven One SimuLink";
            this.ResumeLayout(false);
        }
    }
}
