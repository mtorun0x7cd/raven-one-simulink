/*
 * SPDX-FileCopyrightText: 2026 Mert Torun
 * SPDX-License-Identifier: MIT
 *
 * Raven One SimuLink
 * Program.cs
 * Entry point, written in 2026; not part of the thesis
 *
 * The thesis prints three source files of the program (Appendix I to III).
 * Its designer file and its three description forms were not preserved.
 * This file declares the entry point and the forms and controls that
 * "Raven One.cs" uses, so that the printed files compile. It does not lay
 * the controls out, so the window of a build is empty.
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
