# Knowledge Graph AST Schema & Blast-Radius Specifications

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-knowledge-graph/SKILL.md"
  origin: "Maxilun Knowledge Graph Engine"
-->

Panduan struktur data representasi graf pengetahuan (*Knowledge Graph*), skema simpul-sisi (*node-edge schema*), dan protokol kueri simbolik berbasis AST.

---

## 1. Skema Node & Edge Graph

Graf diekspor ke dalam berkas `maxilun-out/graph.json` menggunakan format JSON terstandarisasi:

```json
{
  "version": "1.0.0",
  "nodes": [
    {
      "id": "file:src/auth/session.ts",
      "type": "FILE",
      "path": "src/auth/session.ts",
      "language": "typescript"
    },
    {
      "id": "func:src/auth/session.ts:verifySession",
      "type": "FUNCTION",
      "name": "verifySession",
      "line": 42,
      "exported": true
    }
  ],
  "edges": [
    {
      "source": "func:src/routes/api.ts:handleLogin",
      "target": "func:src/auth/session.ts:verifySession",
      "type": "CALLS"
    },
    {
      "source": "file:src/routes/api.ts",
      "target": "file:src/auth/session.ts",
      "type": "IMPORTS"
    }
  ]
}
```

---

## 2. Tata Bahasa Kueri Simbol (Symbol Query Grammar)

Gunakan perintah CLI `python cli.py query "<grammar>"` untuk menelusuri graf tanpa membaca berkas teks penuh:

1. **`defOf:<simbol>`**:
   - Mencari titik definisi fungsi, kelas, atau tipe (mengembalikan `file:line`).
2. **`callsIn:<fungsi>`**:
   - Menemukan seluruh pemanggil downstream atau fungsi apa saja yang dipanggil oleh target.
3. **`importersOf:<file>`**:
   - Mengembalikan daftar seluruh berkas yang mengimpor modul target untuk menghitung radius dampak (*blast radius*).

---

## 3. Kalkulasi Radius Dampak (Blast Radius)

Sebelum fungsi publik diubah:
1. **Derajat Ketergantungan Langsung (Degree 1)**: Modul yang langsung mengimpor simbol yang akan diedit.
2. **Derajat Ketergantungan Transitif (Degree 2+)**: Modul hilir yang mengonsumsi hasil keluaran dari modul Degree 1.
3. Jika Degree 1 $> 10$ berkas, eskalasi sebagai keputusan *Type 1 (Irreversible / High-Blast)* sebelum mengubah tanda tangan fungsi.

---

## 4. Arsitektur Incremental AST Cache & Fingerprinting

Maxilun Knowledge Graph menggunakan sistem cache berlapis untuk menjamin kecepatan scan $O(1)$ pada berkas yang tidak berubah:

1. **`stat-index.json`**: Menyimpan `st_size` dan `st_mtime_ns` dari setiap berkas terindeks. Jika filesystem stat sama, berkas tidak dibaca ulang dari disk.
2. **Content Fingerprint (SHA-256)**: Jika timestamp berubah namun isi identik, hash mencegah re-parsing AST.
3. **Per-file Granular AST Cache**: Hasil ekstraksi disimpan di `.maxilun/cache/ast/<version>/<sha256>.json`.
4. **Stabilitas Komunitas**: Signature anggota komunitas disimpan di `.maxilun/community_signatures.json` agar ID dan label modul konsisten antar pemindaian.

---

## 5. Temporal Snapshotting & Architectural Diff

1. **Arsip Snapshot**: Menjalankan `python cli.py scan --snapshot` mengarsipkan artefak ke `maxilun-out/snapshots/YYYY-MM-DD/`.
2. **Komparasi Diff**: Jalankan `python cli.py diff <target1> <target2>` untuk membandingkan dua snapshot bertanggal atau dua berkas `graph.json`:
   - Delta Simbol (`+ / - nodes`)
   - Delta Relasi (`+ / - edges`)
   - Deteksi pergeseran *God Nodes* dan dependensi baru.
