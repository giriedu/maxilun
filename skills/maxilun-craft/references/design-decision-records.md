# Design Decision Records (DDR): Adversarial Direction Justification

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

Panduan penyusunan rekaman keputusan desain (*Design Decision Records* / DDR) berbasis evaluasi bersaing (*adversarial evaluation*). Setiap perancangan antarmuka baru atau perombakan visual wajib mendokumentasikan alasan pemilihan arah sebelum menulis baris kode pertama.

---

## 1. Urutan Operasi (Order of Operations)

Sebelum menentukan tata letak dan palet warna:

1. **Riset 3 Pemimpin Kategori Nyata**:
   - Telusuri implementasi terbaik di ranah terkait (misal: reservasi penginapan butik -> periksa *Airbnb Luxe*, *Mr & Mrs Smith*, *Plum Guide*).
   - Identifikasi pola konvensional industri dan tentukan satu pembeda utama (*point of differentiation*) yang sengaja ditolak.
2. **Ekstraksi Palet Fisik Dunia Nyata**:
   - Dilarang memilih nilai hex sembarang dari palet generik internet.
   - Ambil warna dari material fisik yang nyata ada di lingkungan subjek produk:
     - Bengkel cetak / tipografi: Tinta offset pekat, timbal cetak dingin, minyak pelumas baja.
     - Kedai kopi artisan: Biji sangrai gelap, kertas filter alami, keramik glasir tanah liat.
     - Penginapan pedesaan: Kapur dinding batu (*lime wash*), hijau daun hutan lokal, terakota ubin lantai bakar.
3. **Katalog Tipografi Hidup**:
   - Pilih jenis huruf display yang memiliki kaitan historis atau geografis dengan karakter produk (misal: *Lusitana* untuk arsitektur Portugis, *Fraunces* untuk tipografi editorial organik).
   - Pasangkan dengan sans-serif fungsional netral untuk teks operasional, data tabular, dan formulir.
4. **Audit Kunci Desain Lama Sebelum Redesign (Design Lock Assessment)**:
   - Jika tugas berupa *redesign*, periksa token `:root`, layout shell, dan komponen primitif yang ada.
   - Identifikasi apakah ada variabel kusam atau wrapper sempit yang mengunci UI ke template lama.
   - Putuskan titik pembongkaran kunci (*cutover point*) sebelum merombak leaf JSX.
---

## 2. Tiga Arah Desain Bersaing (Three Competing Directions)

Rancang tiga konsep kontras untuk mencegah bias otomatis model AI:

| Arah | Definisi Konsep | Karakteristik Utama | Risiko / Alasan Evaluasi |
|---|---|---|---|
| **Direction 1: The Generic AI Trap** | Pola instinktif pertama yang biasa diambil generator otomatis. | Tumpukan kartu simetris, hero pill badge mengambang, dua tombol solid kembar, tata letak rata-tengah monoton. | Wajib diidentifikasi untuk sengaja ditolak atau dipangkas habis. |
| **Direction 2: Authentic Domain Artifact** | Struktur antarmuka yang berpusat pada objek kerja atau identitas material subjek. | Membangun antarmuka di sekitar satu objek interaktif utama (*The Object IS the Interface*), hierarki editorial proporsional, palet fisik terkalibrasi. | Menjual karakter subjek dan pengalaman penggunaan sebelum menagih aksi transaksi. |
| **Direction 3: Radical Utility & Density** | Pendekatan fokus kecepatan dan efisiensi tugas tinggi. | Kepadatan tabular data terukur, monokrom kontras tinggi, navigasi langsung tanpa ornamen visual sekunder. | Sangat efisien untuk alat kerja harian; evaluasi apakah cocok untuk audiens produk ini. |

---

## 3. Matriks Komparasi & Justifikasi Pemenang

Bandingkan ketiga arah menggunakan kriteria objektif:

1. **Kesesuaian Mental Model Pengguna**: Apakah alur visual selaras dengan cara pengguna memproses informasi di dunia nyata?
2. **Kejujuran Fungsional**: Apakah setiap elemen visual membawa fungsi nyata atau hanya sekadar hiasan?
3. **Ketahanan Lintas Perangkat**: Apakah geometri antarmuka tetap kokoh pada layar mobile 375px hingga desktop lebar tanpa kebocoran scroll?

### Format Dokumentasi DDR

Dokumentasikan keputusan dalam format ringkas 3 paragraf:

```markdown
### DDR-001: [Nama Layar / Komponen]
- **Konteks & Entitas Fisik**: [Material fisik dunia nyata dan jenis huruf terpilih]
- **Arah Terpilih**: Direction 2 ([Nama Arah])
- **Alasan Kemenangan**: [2 kalimat faktual mengapa arah ini paling tepat melayani tugas utama]
- **Elemen yang Ditolak**: [Daftar komponen dari Direction 1 & 3 yang sengaja dibuang dan argumen penolakannya]
```

### Format Dokumentasi Redesign & Pembongkaran Kunci (DDR-DL)

Gunakan format ini saat melakukan *redesign* antarmuka yang sebelumnya terkunci:

```markdown
### DDR-DL-001: [Nama Layar / Area Redesign]
- **Kunci Desain yang Dibongkar**: [Token `:root` lama, wrapper layout sempit, atau primitif usang yang dihapus]
- **Fondasi Baru yang Dipasang**: [Palet OKLCH material fisik domain, display/sans typography, layout kanvas bebas]
- **Pencegahan Tambal Sulam**: [Bukti bahwa CSS lama/zombie dihapus bersih dan tidak menyisakan tabrakan styling]
```

---

## 4. Protokol Subtraksi Antarmuka (Subtraction Pass)

Setelah draf antarmuka tersusun:

1. Hapus satu elemen visual (garis pemisah, badge dekoratif, pembungkus kartu ganda, atau teks keterangan berulang).
2. Periksa apakah pemahaman pengguna atau keterbacaan data menurun.
3. Ulangi proses ini secara iteratif sampai penghapusan berikutnya mulai merusak pemahaman atau fungsi navigasi.
4. Kembalikan elemen terakhir tersebut. Jumlah elemen yang tersisa adalah batas optimal (*densitas murni*).
