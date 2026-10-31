# Visual Reference → Web Motion Direction

Read this when a user provides example websites, screenshots, or a visual target for a motion-led website/app. The goal is to extract useful design and motion decisions, then create an original experience for the user's product.

## 1. Inspect and separate the references

Use an available browser or page preview to inspect the provided references directly. Review the initial viewport and, when possible, scroll through the full page and try important interactions. If only search/page text is available, say the motion or visual behavior could not be verified; do not infer effects from marketing copy alone.

For each reference, record only observed or user-requested qualities in a small matrix:

| Reference | Visual language | Motion/interaction | Useful lesson | Do not copy |
|---|---|---|---|---|
| URL/name | Composition, type, color, image/3D treatment | Trigger, movement, transition, response | One or two transferable principles | Distinctive layout, copy, assets, identity |

References can contribute different ingredients. For example, one may guide scroll storytelling, another editorial image composition, another immersive WebGL camera work, and another spatial/product explanation. Do not blend every reference equally or treat a product company's subject matter as proof that its own website is a full 3D scene.

## 2. Choose one coherent art direction

State one primary design thesis for the new product: audience, mood, visual hierarchy, typography/image treatment, primary motion signature, and the role of 3D. Select at most two main reference directions; use other links for a specific isolated lesson. If the references point in conflicting directions, ask one short question only when that choice materially changes the design. Otherwise choose the direction that best serves the product and label it as an assumption.

Translate references into original decisions. Never copy their text, artwork, logos, distinctive layouts, or exact animation sequence. Avoid generic effects added only because the reference looks impressive: every major movement should explain a product idea, guide attention, or give interaction feedback.

## 3. Turn the direction into a motion plan

Before implementing, outline the experience in sections or scenes. For each major beat record:

- what the visitor sees and understands;
- what triggers motion (page load, scroll range, pointer/touch, click, or live state);
- which object or layer moves and along which axis/depth;
- the transition and settled state;
- the user's way to skip, reverse, navigate, or recover;
- reduced-motion and mobile behavior.

Keep content readable while motion runs. Do not bind essential navigation or information solely to scroll position, hover, gyro input, or a WebGL canvas.

For immersive, editorial, portfolio, or cinematic scene pages, omit breadcrumb navigation and any eyebrow/kicker/overline/category label placed immediately above the hero H1 (for example, `GATEWAY WHATSAPP · SELF-HOSTED`). Let the hero begin with its main heading. Do not style an `h2` as a breadcrumb or hierarchy trail (for example, `HOME / PLATFORM / CHAMBER 01`); use headings as standalone content labels with meaning. If orientation between scenes is needed, show a separate scene index as navigation, visually distinct from headings. Apply this rule to the motion-led hero; conventional application screens may use breadcrumbs when they clarify deep navigation.

## 4. Review the actual implementation

When a local browser/preview is available, inspect the running result at desktop and mobile sizes. Review at least the initial state, one mid-scroll/scene transition, an interactive state, and the ending/CTA. Compare the result to the written direction, identify the largest visual mismatch, make a focused correction, and preview again. Check for broken loading, unreadable text over motion, clipped layouts, accidental horizontal scroll, and jarring camera changes.

Do not report that it is "like the reference", polished, responsive, or smooth based only on code inspection. Link the preview or report what was actually inspected; mark unavailable device/browser checks as unverified. If no preview exists in the platform, deliver the implementation and state that visual QA was not performed.
