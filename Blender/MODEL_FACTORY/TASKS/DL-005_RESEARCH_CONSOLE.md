# DL-005 — Underwater Research Console

**Priority:** P0  
**Status:** QUEUED

## Goal
A hero station console used to review discoveries, scan samples and prepare dives. The model is visual only; do not invent or implement gameplay logic.

## Composition
- Compact desk/pedestal with stable weighted base and service access.
- Angled main screen with thick protective bezel and a secondary smaller status panel.
- Three physically distinct control groups: guarded switches, rotary selector knobs and tactile push buttons.
- Recessed specimen tray or scanner pad with a cyan scan ring.
- Cable conduit routed to a real connector point; vents, screws and replaceable access panel.
- Optional upper lamp bar with two adjustable work lights.

## Visual hierarchy
Main display is the focal point; controls should remain readable at gameplay distance without relying on tiny text. Use abstract interface graphics in the preview only, not baked text. Palette: graphite/navy base, warm light-gray casing, cyan scanning elements, amber/orange caution controls.

## Performance
Target 4k–8k triangles, 2–4 materials and a shared 1K texture set. Separate screen, buttons and scan pad only if useful for future animation or material changes. Pivot at the floor center.

## Validation
Check no screen coplanar flicker, buttons are not needle-thin, base sits level, export retains materials and dimensions are documented. Do not attach scripts or change existing UI.

## Generator prompt
“Create a premium stylized underwater scientific research console for a Roblox exploration station. A stable compact pedestal desk, angled main monitor with thick reinforced bezel, smaller status display, tactile guarded switches, rotary knobs, chunky buttons, recessed sample scanning tray with a thin cyan luminous ring, cable conduit, vents and service panel. Graphite and deep navy structure, warm off-white casing, controlled orange caution details, subtle brushed metal, crisp but restrained wear. Strong readable forms at gameplay distance, realistic ergonomic engineering, optimized game topology, UV-ready PBR, no logos or legible text, no floating controls. Floor-center pivot.”
