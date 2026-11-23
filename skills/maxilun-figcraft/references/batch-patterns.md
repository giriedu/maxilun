# FigCraft MCP Batch & Node Construction Patterns

This reference provides validated payload patterns for FigCraft desktop Live Canvas operations (`figcraft_figcraft-live`).

## 1. Atomic Batch Payload Schema

A typical atomic `batch` payload creates a parent frame and nested Auto Layout children in a single transaction:

```json
{
  "document": 1,
  "label": "Create Bento Feature Section",
  "onError": "abort",
  "commands": [
    {
      "action": "node.create",
      "type": "FRAME",
      "as": "bentoRoot",
      "params": {
        "parent": 1024,
        "name": "Bento_Container",
        "select": false,
        "width": 1200,
        "height": 560,
        "layout": "horizontal",
        "gap": 24,
        "padding": 32,
        "fills": [{"type": "SOLID", "color": "#0F172A"}],
        "cornerRadius": 16
      }
    },
    {
      "action": "node.create",
      "type": "FRAME",
      "as": "colPrimary",
      "params": {
        "parent": {"$ref": "bentoRoot"},
        "name": "Card_Primary_8col",
        "select": false,
        "sizingH": "fill",
        "sizingV": "fill",
        "layout": "vertical",
        "gap": 16,
        "padding": 24,
        "fills": [{"type": "SOLID", "color": "#1E293B"}],
        "strokes": [{"type": "SOLID", "color": "#334155"}],
        "strokeWeight": 1,
        "cornerRadius": 12
      }
    },
    {
      "action": "node.create",
      "type": "TEXT",
      "params": {
        "parent": {"$ref": "colPrimary"},
        "name": "Headline_Text",
        "select": false,
        "characters": "Operational Metric Ledger",
        "fontSize": 24,
        "fontFamily": "Inter",
        "fontWeight": "600",
        "fills": [{"type": "SOLID", "color": "#F8FAFC"}]
      }
    }
  ]
}
```

## 2. Shared Design Tokens Sheet (`#RRGGBB`)

Map OKLCH brand values to deterministic 6-digit hex tokens for FigCraft compatibility:

| Token Name | Hex Value | Semantic Usage |
|---|---|---|
| `--surface-canvas` | `#090D16` | Root frame background fill |
| `--surface-panel` | `#111827` | Section container fill |
| `--surface-card` | `#1F2937` | Bento card and ledger component fill |
| `--border-subtle` | `#374151` | 1px card boundary hairline |
| `--border-focus` | `#6366F1` | Active state accent stroke |
| `--text-primary` | `#F9FAFB` | Headings and primary values |
| `--text-secondary` | `#9CA3AF` | Supporting descriptions, metadata |
| `--accent-action` | `#4F46E5` | Sole primary CTA button fill |

## 3. Auto-Layout Sizing Cheat Sheet

- `sizingH: "hug"`: Container shrinks or expands to hug child widths (buttons, badges).
- `sizingH: "fill"`: Container fills available horizontal space in parent frame (cards, columns).
- `sizingH: "fixed"`: Exact pixel width specified via `width`.
- Concentric Corner Radii: Outer frame `cornerRadius: 16`, padding `24` $\to$ Child card `cornerRadius: 12`, padding `16` $\to$ Nested button `cornerRadius: 8`.

