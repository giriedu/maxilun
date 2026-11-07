# Maxilun Desktop References Index

Indeks pustaka rekayasa desktop, arsitektur native, sistem warisan enterprise, dan integrasi GUI.

## Berkas Referensi Domain

1. **`powerbuilder-playbook.md`**:
   Arsitektur PowerScript, siklus hidup transaksi `SQLCA`, manajemen 4 buffer DataWindow (`Primary!`, `Filter!`, `Delete!`, `Original!`), event data, sintaks `.srd`, dan modernisasi REST/C++ interop.
2. **`native-desktop-patterns.md`**:
   Pola native Windows (Win32 message loop, Per-Monitor V2 DPI, GDI handle lifecycle, WinUI 3/WPF MVVM), macOS Cocoa/AppKit & Swift (`NSWindowController`, notarisasi), dan lintas platform C++ Qt (parent-child ownership, queued connections, modern CMake).

## Panduan Pemuatan
Muat dokumen spesifik hanya saat domain tugas menyentuh arsitektur terkait:
- Tugas PowerBuilder atau DataWindow → baca `references/powerbuilder-playbook.md`.
- Tugas Windows Win32/WPF, macOS Cocoa, atau C++ Qt → baca `references/native-desktop-patterns.md`.
