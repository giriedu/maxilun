# Technical SEO Standards: Crawlability, Metadata & Schema.org

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-seo-audit/SKILL.md"
  origin: "Maxilun SEO Engine"
-->

Panduan pelaksanaan audit SEO teknis, struktur metadata mesin perayap (*search crawler*), dan spesifikasi `llms.txt`.

---

## 1. Disiplin Kanonisasi & Crawl Budget

1. **Tag Kanonikal Eksplisit**:
   - Setiap halaman publik wajib menyertakan `<link rel="canonical" href="https://example.com/path" />` absolut untuk mencegah duplikasi konten akibat query string analitik atau paginasi.
2. **Higienitas `robots.txt`**:
   - Blokir jalur internal sensitif (`/admin`, `/api/`, `/_next/`) dan tunjukkan lokasi berkas indeks sitemap:
   ```text
   User-agent: *
   Disallow: /api/
   Disallow: /admin/
   Allow: /

   Sitemap: https://example.com/sitemap.xml
   ```
3. **Pemisahan Sitemap Berindeks**:
   - Batasi setiap berkas sitemap maksimal 50.000 URL atau 50MB (uncompressed). Gunakan `sitemap_index.xml` untuk membagi rute statis, artikel, dan katalog produk.

---

## 2. Struktur Data JSON-LD (Schema.org)

Sematkan data terstruktur di dalam tag `<script type="application/ld+json">` yang dihasilkan deterministik dari server:

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Acme Ledger",
  "operatingSystem": "Web",
  "applicationCategory": "BusinessApplication",
  "offers": {
    "@type": "Offer",
    "price": "29.00",
    "priceCurrency": "USD"
  }
}
```

---

## 3. Spesifikasi File `llms.txt`

Untuk memfasilitasi penemuan dan pemahaman model kecerdasan buatan terhadap produk:
- Letakkan berkas ringkasan di `/llms.txt` (akar domain).
- Sajikan rincian dokumentasi terstruktur dalam format Markdown bersih tanpa JavaScript atau styling visual.
