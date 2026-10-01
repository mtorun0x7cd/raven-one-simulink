// SPDX-FileCopyrightText: 2026 Mert Torun
// SPDX-License-Identifier: MIT
//
// The printed files cMD5.cs and cRSA.cs carry "using System.Windows.Forms;"
// but use nothing from that namespace. Windows Forms exists only on Windows,
// so this empty declaration lets the directive resolve on any operating
// system, and the two files compile unchanged.

namespace System.Windows.Forms
{
    internal static class CrossPlatformShim
    {
    }
}
