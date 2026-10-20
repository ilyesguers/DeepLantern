# Deep Lantern — GitHub-first 3D Model Factory (No Blender)

This is the authoritative workflow for producing the 20 assets. Do not connect to Roblox Studio; GitHub is the delivery location. Roblox Studio inspection/import is a later phase handled separately by the user.

## What Claude must do
1. Read this file, `PROMPT.md`, `PROGRESS.md`, the relevant task brief, and the latest commits before starting. Check git status and existing asset folders to avoid duplicates.
2. Work on branch `assets/roblox-studio-model-factory` or a new feature branch based on it; never commit to `main` directly, delete/overwrite unrelated files, or modify the live game.
3. Follow the detailed model brief files under `Blender/MODEL_FACTORY/TASKS/`. That folder name is historical; Blender is not used. Each task contains visual design, variants, performance targets and a generator prompt.
4. Create ONE model/set at a time. Use a real available 3D model generator or authorized asset-generation tool and obtain the actual downloadable 3D bytes. Do not substitute an image, prompt, or procedural text file for a 3D model.
5. Upload/commit that model's real source file if available, Roblox-compatible export (.fbx/.glb/.obj where the tool supports it), textures/maps, preview, manifest, and import notes under `Assets/ModelFactory/Models/<ID>/`.
6. Check that files exist and are non-empty, record actual file formats and metadata, and review rights/licensing. Do not claim topology/triangle counts unless measured from real mesh data. Do not claim Roblox Studio import/tests were done; those happen later.
7. Update `PROGRESS.md` in the same commit or immediately after each completed model. Continue to the next queue item only after the current deliverables are committed and status is truthful.

## If no 3D generator is available
Do not fake a model and do not report success. Create `Assets/ModelFactory/Models/<ID>/BLOCKED.md` explaining exactly what is missing, preserve the detailed prompt, update progress to BLOCKED, and continue only if another genuine tool is available. GitHub alone stores files; it does not generate 3D geometry by itself.

## Shared style and project constraints
Premium stylized underwater exploration; navy/graphite station engineering, off-white enamel, restrained orange safety details, cyan/teal and selective violet bioluminescence. Beautiful and mysterious, not horror. Strong silhouettes readable at gameplay distance, purposeful detail, no floating decorations, no razor-thin parts, no million-face meshes, no excessive glow. Mobile/low-end performance matters. Keep all gameplay, UI, currency, zones, and scripts unchanged. Preserve exact existing identifier `Zone_TwilightReef` in documentation if referenced; assets must not invent mechanics.

## Queue
P0: DL-001 submarine; DL-002 modular station kit; DL-003 dive beacon; DL-004 sample canisters; DL-005 research console.
P1: DL-006 coral family; DL-007 kelp; DL-008 rocks; DL-009 bioluminescent flora; DL-010 wreckage; DL-011 Twilight Reef arch; DL-012 ancient relic.
P2: DL-013 discovery display; DL-014 docking pad; DL-015 cave entrance; DL-016 cables/hoses; DL-017 signage; DL-018 crates; DL-020 lighting kit.
P3: DL-019 small fauna (lower priority because rigging/animation is a later separate task).

## Per-model package
- `model.<actual-extension>`: real model export, not placeholder.
- `source.<actual-extension>`: editable source if provided by the generator; omit if unavailable and state why.
- `Textures/`: only real required maps, named clearly.
- `preview.png`: genuine preview render/image; not a substitute for the model.
- `manifest.json`: id, name, status, generator/source, file list, dimensions, scale/units, pivot, measured mesh stats (if available), material/texture list, license/rights, limitations, Roblox import guidance.
- `README.md`: brief, variant list, usage, suggested import/collision settings, known limitations.

Allowed statuses: QUEUED, IN_PROGRESS, UPLOADED_TO_GITHUB, BLOCKED, NEEDS_REVIEW. UPLOADED_TO_GITHUB means real model file bytes are committed. It does not mean Roblox Studio validated the asset.
