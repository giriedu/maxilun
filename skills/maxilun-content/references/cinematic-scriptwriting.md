# Cinematic Scriptwriting, Spoken Pacing & Google Cloud TTS Integration

Gunakan referensi ini saat menulis naskah narasi video, mengarahkan intonasi suara, menyusun anotasi SSML, atau memproduksi voice-over menggunakan Google Cloud Text-to-Speech untuk video `maxilun-cinecode`.

---

## 1. Filosofi Narasi Spoken: Tulisan untuk Telinga, Bukan untuk Mata

Web copy dibaca dengan mata (scannable, non-linear). Narasi video didengar dengan telinga (sekuensial, temporal, berirama):

| Aspek | Web Copy (`maxilun-content`) | Narasi Video Spoken |
|---|---|---|
| **Medium** | Mata membaca teks di layar | Telinga mendengar gelombang suara |
| **Kontrol Kecepatan** | Pembaca menentukan scroll | Narator menentukan jeda dan emosi |
| **Kepadatan** | Paragraf ringkas terstruktur | Kalimat pendek berjarak (1 ide per napas) |
| **Keheningan** | Spasi putih visual | Jeda audio (`0.4s - 1.2s`) untuk pencernaan ide |
| **Keluaran** | Elemen tipografi DOM | Berkas audio sinkron + metadata cue |

### 5 Prinsip Narasi Sinematik
1. **Tes Baca Nyaring**: Ucapkan setiap baris dengan suara keras sebelum disahkan. Jika lidah terpeleset atau napas terputus, pecah kalimat menjadi dua.
2. **Irama di Atas Tata Bahasa Kaku**: Fragmen kalimat diperbolehkan jika memberikan tekanan emosi yang tepat.
3. **Konkret Menggantikan Sifat**: Hindari kata sifat kosong. Ganti dengan angka fakta atau perbandingan langsung.
4. **Sinkronisasi Titik Temu (Sync Points)**: Setiap kalimat narasi harus memiliki pasangan momen visual yang relevan pada timeline frame video.
5. **Keseimbangan Loudness**: Voice-over wajib di-master pada `-16 LUFS` mono, dengan musik latar yang ter-*ducking* saat suara aktif.

---

## 2. Struktur Data Narasi & Timeline

```typescript
export interface NarrationSegment {
  id: string;
  sceneId: string;
  text: string;                  // Teks bersih tanpa markup
  ssmlText: string;              // Teks teranotasi SSML untuk TTS engine
  startFrame: number;            // Frame awal kemunculan di timeline
  endFrame: number;              // Frame akhir durasi vokal
  durationSeconds: number;
  emotion: 'authoritative' | 'urgent' | 'confident' | 'warm';
  pauseAfterMs: number;          // Durasi jeda hening setelah kalimat
  visualCue: string;             // Deskripsi peristiwa visual yang dipicu
  syncPoint?: {
    frame: number;
    event: string;
  };
}
```

---

## 3. Integrasi Google Cloud TTS & Panduan Suara

### 3.1 Pilihan Suara Direkomendasikan

| Voice ID | Bahasa | Gender | Engine | Karakteristik Suara |
|---|---|---|---|---|
| `id-ID-Wavenet-B` | Bahasa Indonesia | Pria | WaveNet | Berwibawa, tegas, artikulasi formal |
| `id-ID-Wavenet-A` | Bahasa Indonesia | Wanita | WaveNet | Hangat, profesional, jernih |
| `id-ID-Neural2-A` | Bahasa Indonesia | Wanita | Neural2 | Modern, jernih untuk instruksi teknis |
| `en-US-Journey-D` | English (US) | Pria | Journey | Sinematik, bercerita, penuh dinamika |
| `en-US-Neural2-D` | English (US) | Pria | Neural2 | Presisi, percaya diri, tempo stabil |

### 3.2 Format Sintaks SSML (Speech Synthesis Markup Language)

```xml
<speak>
  <prosody rate="medium" pitch="+0st">
    Kesan pertama bisnis kini
    <emphasis level="strong">sembilan puluh empat persen</emphasis>
    ditentukan di layar digital.
    <break time="450ms"/>
  </prosody>
</speak>
```

Aturan penggunaan SSML:
- `<break time="300ms"/>` untuk jeda antar-klausa.
- `<break time="600ms"/>` untuk pergantian scene atau penegasan poin penting.
- `<emphasis level="strong">` untuk satu kata kunci yang membawa pesan utama.
- `<prosody rate="slow">` saat menyebutkan data angka atau instruksi aksi.

---

## 4. Checklist Kualitas Narasi Sebelum Handoff ke CineCode

- [ ] **Word Count**: Tidak melebihi 2.2 kata per detik pada tempo normal (maksimal 65 kata untuk video 30 detik).
- [ ] **Angka Ditulis Fonetik**: Angka seperti "94%" ditulis "sembilan puluh empat persen" dalam naskah SSML agar pembacaan TTS tidak salah intonasi.
- [ ] **Breath Marks & Holds**: Terdapat jeda minimal 1.5 detik hening di akhir video sebelum file selesai agar CTA terbaca utuh.
- [ ] **Sinkronisasi Beat**: Timing `startFrame` vokal selaras dengan birama musik latar.
