# Credits

maxilun-craft is an original module: its workflow (Brief, token lock,
layered build, proof tests), its wording, its token formulas and the
`slopscan.py` checker were written for Maxilun. No text or code was copied
from the sources below. They informed the thinking and deserve credit.

- **unslop** by Damir Sokolovsky (@heydamir), CC BY 4.0,
  https://github.com/heydamir/unslop - the idea of auditing a screen for
  recognisable "signs" of generated UI and fixing them in ordered passes
  led by a product-derived direction.
- **Motion** (motion.dev, formerly Framer Motion), MIT - the animation
  library documented in `references/motion.md`. Code samples there are our
  own, written against its public API.
- **Framer agent plugin** (github.com/framer/agent-plugins), MIT - an MCP
  connector to Framer projects. It contains no design guidance to adapt; it
  is referenced only as an optional tool the module can drive.
- WCAG 2.2 for contrast and target-size thresholds.

If you redistribute this module, keep this file.
