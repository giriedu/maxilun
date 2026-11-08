# Web3D Asset Pipeline & Texture Optimization

Standar produksi untuk pemodelan, konversi, kompresi, dan pengemasan aset 3D (Blender & Substance 3D) untuk web interaktif berlatensi rendah.

---

## 1. Pengepakan Tekstur ORM (Occlusion - Roughness - Metallic)

Dalam alur kerja PBR standar, peramban sering memuat 3 file tekstur monokrom terpisah:
1. Ambient Occlusion map (skala abu-abu)
2. Roughness map (skala abu-abu)
3. Metallic map (skala abu-abu)

Memuat 3 tekstur terpisah ini membuang bandwidth seluler dan mengonsumsi 3x slot sampler tekstur GPU.

### Standar Saluran Pengepakan ORM:
Gabungkan ketiga saluran ke dalam **satu file tekstur RGB 8-bit**:
- **Saluran R (Red)**: Ambient Occlusion (AO)
- **Saluran G (Green)**: Roughness
- **Saluran B (Blue)**: Metallic
- *(Opsional) Saluran A (Alpha)*: Opacity / Masking

```
File: asset_name_orm.png (atau .webp / .ktx2)
├── R: Ambient Occlusion
├── G: Roughness
└── B: Metallic
```

### Konfigurasi Material Three.js / R3F untuk Tekstur ORM:
```javascript
const textureLoader = new THREE.TextureLoader();
const ormMap = textureLoader.load('/textures/product_orm.webp');

const material = new THREE.MeshStandardMaterial({
  map: colorMap,
  aoMap: ormMap,             // Baca dari saluran Red
  aoMapIntensity: 1.0,
  roughnessMap: ormMap,      // Baca dari saluran Green
  roughness: 1.0,
  metalnessMap: ormMap,      // Baca dari saluran Blue
  metalness: 1.0
});
```
*Hasil Kinerja: Menghemat 66% memori tekstur VRAM GPU dan memotong request HTTP dari 3 menjadi 1.*

---

## 2. Alur Ekspor Blender ke Web (GLTF / GLB)

Sebelum mengekspor model dari Blender untuk web, terapkan 6 langkah pembersihan wajib:

### Langkah 1: Normalisasi Transformasi (Apply Transforms)
Pilih seluruh mesh dan tekan `Ctrl + A` -> `All Transforms` (Location, Rotation, Scale = 1.0). Ini mencegah distorsi matriks saat diimpor ke Three.js.

### Langkah 2: Audit Jumlah Poligon & Decimate
- Hapus geometri tersembunyi yang tidak terlihat oleh kamera (misal: bagian dalam casing produk).
- Terapkan modifier `Decimate` untuk mereduksi simpul hingga berada di bawah anggaran ($\le 50\text{k}$ triangles untuk mobile).

### Langkah 3: Batasan Armature / Bone Rigging (Mobile WebGL Limit)
- Batasi jumlah *bones per mesh* maksimal **64 bones** agar kompatibel dengan vertex shader mobile.
- Pastikan bobot simpul (*bone weights*) maksimal 4 pengaruh per vertex.

### Langkah 4: Pengaturan Ekspor GLTF 2.0 di Blender
Saat mengekspor melalui `File > Export > glTF 2.0 (.glb/.gltf)`:
- **Format**: `glTF Binary (.glb)` (mengemas geometri, animasi, dan tekstur dalam 1 file biner terkompresi).
- **Include**: Selected Objects, Custom Properties.
- **Transform**: `+Y Up` (standar koordinat WebGL).
- **Geometry**:
  - `Apply Modifiers`: Aktif.
  - `UVs`: Aktif.
  - `Normals`: Aktif.
  - `Tangents`: Aktif (bila menggunakan normal maps).
- **Compression**: Aktifkan **Draco Mesh Compression** (Level 7 untuk geometri non-animasi) atau gunakan pipeline `meshopt`.

---

## 3. Optimasi Pasca-Ekspor (glTF-Transform CLI)

Gunakan utilitas CLI `gltf-transform` untuk mengoptimalkan file `.glb` sebelum dimasukkan ke aset web produksi:

```bash
# 1. Pangkas simpul duplikat dan bersihkan struktur node
npx @gltf-transform/cli dedup input.glb step1.glb

# 2. Kompresi tekstur ke format GPU modern (WebP / KTX2)
npx @gltf-transform/cli webp step1.glb step2.glb --quality 80

# 3. Terapkan kompresi Meshopt untuk dekompresi instan di peramban
npx @gltf-transform/cli meshopt step2.glb output-optimized.glb

# 4. Validasi laporan ukuran dan draw calls
npx @gltf-transform/cli inspect output-optimized.glb
```

---

## 4. Checklist Kualitas Aset Web3D

- [ ] Resolusi tekstur adalah *Power-of-Two* (`512x512`, `1024x1024`, atau maksimal `2048x2048`).
- [ ] Ukuran total file `.glb` siap saji $\le 3.5\text{MB}$ untuk desktop dan $\le 1.5\text{MB}$ untuk landing page mobile.
- [ ] Sumbu rotasi utama menghadap ke depan (`Z+` atau `Y+` sesuai orientasi kamera awal).
- [ ] Titik tumpu (*pivot/origin*) model berada di pusat bounding box atau dasar lantai objek.
- [ ] Tekstur warna dasar (*albedo/diffuse*) memakai ruang warna sRGB; tekstur ORM dan Normal memakai ruang warna Linear.
