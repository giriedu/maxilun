# Technical SEO Standards: Crawlability, Metadata & Schema.org

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-seo-audit/SKILL.md"
  origin: "Maxilun SEO Engine"
-->

Guide for running a technical SEO audit, structuring metadata for search crawlers, and meeting the `llms.txt` specification.

---

## 1. Canonicalization Discipline & Crawl Budget

1. **Explicit Canonical Tag**:
   - Every public page must include an absolute `<link rel="canonical" href="https://example.com/path" />`. It prevents duplicate content caused by analytics query strings or pagination.
2. **`robots.txt` Hygiene**:
   - Block sensitive internal paths (`/admin`, `/api/`, `/_next/`) and point to the sitemap index file:
   ```text
   User-agent: *
   Disallow: /api/
   Disallow: /admin/
   Allow: /

   Sitemap: https://example.com/sitemap.xml
   ```
3. **Split Sitemaps Under an Index**:
   - Limit each sitemap file to 50,000 URLs or 50MB (uncompressed). Use `sitemap_index.xml` to split static routes, articles, and product catalogs.

---

## 2. JSON-LD Data Structure (Schema.org)

Embed structured data inside a `<script type="application/ld+json">` tag that the server generates deterministically:

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

## 3. `llms.txt` File Specification

To help AI models discover and understand the product:
- Place the summary file at `/llms.txt` (domain root).
- Serve the detailed documentation as clean, structured Markdown without JavaScript or visual styling.
