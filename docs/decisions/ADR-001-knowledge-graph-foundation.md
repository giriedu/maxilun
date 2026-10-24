# ADR-001: Knowledge Graph Foundation & Symbol Directed Graph Model

**Status**: Accepted  
**Tanggal**: 2026-10-21  
**Pembuat**: Maxilun Architecture

## Konteks
Agen AI pengembang sering kali menghabiskan konteks jendela (token window) untuk membaca berkas besar secara berulang hanya untuk mencari satu lokasi fungsi. Hal ini memicu latensi tinggi dan risiko halusinasi situs simbol.

## Opsi yang Dievaluasi
1. **Opsi A: Navigasi Grep & Glob Dinamis Murni**
   - *Pro*: Tanpa dependensi eksternal, tanpa waktu indexing awal.
   - *Kontra*: Tidak dapat melacak rute pemanggilan (*calls in / calls out*) secara terstruktur, menghabiskan banyak putaran obrolan.
2. **Opsi B: Knowledge Graph Terarah Lokal (Directed Graph AST + Query CLI)**
   - *Pro*: Pemetaan simbol instan `file:line`, resolusi impor statis deterministik, eksekusi query dalam satu panggilan.
   - *Kontra*: Memerlukan scanner ringan (Python AST / regex parser) pada awal sesi.

## Keputusan
Memilih **Opsi B**: Knowledge Graph lokal sebagai fondasi navigasi (Tier 1) yang diintegrasikan ke seluruh 16 spesialis via `maxilun-knowledge-graph` dan `cli.py query`.

## Konsekuensi
- Seluruh spesialis eksekutor wajib memanfaatkan cache graf atau perintah `cli.py query` sebelum membaca berkas penuh.
- Tugas sepele (typo, perbaikan 1 baris) diberi pengecualian jalur cepat (*fast path*) agar tidak terbebani waktu pemindaian.
