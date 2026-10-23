# Deep Lantern Model Factory — GDD Compliance Audit

Audit date: 2026-10-20
Authority reviewed: GDD/DeepLantern_GDD_Parts_1-10_APPROVED.txt, PROJECT_STATE.md, Docs/IMPLEMENTATION_NOTES.md, AI_Workflow/AI_AGENT_RULES.md.
Scope: planned asset briefs only. This is a design-scope audit, not evidence that models exist or have passed Roblox Studio import.

## Verdict
The 20 briefs can support the approved game if the constraints below are applied. The original queue was too loosely scoped in a few places: station assets could accidentally imply post-MVP station tiers, a relic/arch/cave could imply an unapproved extra zone or a full Lost Ruins area, and a console/beacon/sign could be mistaken for new gameplay systems. This audit locks their scope.
- Actual 3D models committed: 0.
- Briefs audited: 20.
- Roblox Studio imports verified: 0.
- GDD Parts 1–10 remain authoritative. Do not invent mechanics from visual briefs.

## MVP and post-MVP rules inherited from the GDD
1. MVP environments are Station, Shallows, Kelp Forest, and Twilight Reef. Abyss, Lost Ruins, The Hollow, Beyond and deeper-zone content remain post-MVP unless the GDD is explicitly revised.
2. MVP station progression is Outpost → Station → Complex. Citadel and Deep Empire are post-MVP.
3. The compact functional Docking Ring is MVP for private co-op staging, boarding and launch. Expanded/public/social functionality is post-MVP.
4. Keep the core loop PLAN → DIVE → DECIDE → DEBRIEF → UPGRADE → GO DEEPER, exactly two currencies (Credits and Research Data), Codex stages Sighted → Scanned → Studied → Mastered, solo parity, optional private/friend co-op for 2–4, mobile/low-end performance.
5. No new zones, currencies, mechanics, NPC fleets, player-built infrastructure, GPS quest-marker system, passive-income station props, gacha/RNG progression, capture inventory for fauna, PvP/combat, or new resource-management systems.
6. Artifacts/relics, biological samples, minerals, field consumables, static beacons, caves/secrets, environmental anomalies, lighting, and station/gallery displays are compatible as physical/visual content when kept inside approved MVP zones and existing systems.
7. Asset art must prioritize silhouette, atmosphere, fog/lighting and selective emissives over huge meshes, excessive particles, complex physics or high object counts.

## Per-asset disposition
| ID | Asset group | GDD fit | Allowed scope / restrictions |
|---|---|---|---|
| DL-001 | Research submarine | MVP core | Visual asset for the existing MVP Scout / submarine workflow. Do not introduce another playable class, new controls, or altered stats. Preserve existing gameplay model/contracts; replacement/integration happens later in Studio. |
| DL-002 | Research station kit | MVP core | Only Outpost, Station, Complex and the documented MVP wings: Power Core, Sub Dock, Workshop, Research Lab, Aquarium/Gallery, Archive, Observatory. Modular reuse; no Citadel/Deep Empire or massive hub. |
| DL-003 | Dive beacon / sonar buoy | MVP-compatible | Static anchored navigation/research landmark in an existing handcrafted MVP zone. No player-built network, GPS markers, passive rewards, or new system. |
| DL-004 | Sample canister family | MVP-compatible | Biological samples / field consumables and existing cargo/debrief flow only. No new inventory type, currencies, crafting or capture mechanics. |
| DL-005 | Research console | MVP core support | Visual prop for existing Research Lab/terminal interactions. No new terminal feature or invented UI/API. |
| DL-006 | Coral family | MVP environment | Place only in Shallows/Twilight Reef where appropriate. Use reusable silhouettes; avoid hundreds of active pieces. |
| DL-007 | Kelp cluster | MVP environment | Kelp Forest only (or approved existing placements). Keep simple and performant; no complex ecosystem simulation. |
| DL-008 | Seafloor rock kit | MVP environment | Reusable geological dressing in approved zones; no procedural world generation or destructible terrain system. |
| DL-009 | Bioluminescent flora | MVP environment | Kelp Forest/Twilight Reef dressing and discovery visuals. No unapproved dynamic bloom/event logic or heavy particle systems. |
| DL-010 | Wreckage set | MVP-compatible, conditional | Small static points of interest within an existing MVP zone only. No new zone, large wreck-dungeon, structural simulation, or combat. |
| DL-011 | Twilight Reef arch | MVP landmark | One readable landmark in the existing Twilight Reef zone (Zone_TwilightReef); not a new region or traversal mechanic. |
| DL-012 | Ancient relic | MVP-compatible, conditional | One/few discoverable relic props compatible with existing Relics & Artifacts/Codex/Archive. A full Lost Ruins environment and zone progression are post-MVP. |
| DL-013 | Discovery display | MVP core support | Aquarium/Gallery display for mastered marine life and relics. Visual showcase only: no passive income or stat bonuses. |
| DL-014 | Docking pad / service arm | MVP core | Must fit the existing Sub Dock and compact MVP Docking Ring. Do not add public matchmaking, crowd/social plaza, new launch mechanics, or replace existing functional pad without Studio review. |
| DL-015 | Cave entrance kit | MVP-compatible, conditional | A small secret/point of interest inside an existing MVP zone. No new zone, procedural cave generation, GPS marker, or deferred advanced Ruins content. |
| DL-016 | Cable / hose kit | MVP support | Reusable station/dock/environment dressing. Static/anchored where possible; no simulated cable physics or interactive power network. |
| DL-017 | Signage kit | MVP support | Physical wayfinding and diegetic labels only. No quest-marker GPS, minimap, or new UI systems. Use concise readable text; do not bake unsupported language-specific gameplay text into meshes. |
| DL-018 | Research crates | MVP-compatible | Existing cargo/station prop dressing only. No passive droppers, storage-management minigame, grid inventory, or additional resource type. |
| DL-019 | Small fauna | MVP-compatible, later in asset queue | Non-lethal Codex creatures using light shared/simple rigs when actually needed. No creature capture inventory, predator/prey ecosystem, complex AI, or combat. If only a static mesh is available, label it unrigged; do not claim animation. |
| DL-020 | Lighting fixture kit | MVP support | Fixture meshes/props only in asset stage. Actual SpotLight/SurfaceLight setup is a later Studio integration step; use limited lights, no excessive dynamic shadows or particles. |

## Revised production priority
**P0 — core MVP visual anchors**
1. DL-001 submarine asset (only after checking that its silhouette/details complement, rather than duplicate or break, the existing submarine).
2. DL-002 MVP station modular kit (scope restricted as above).
3. DL-014 Sub Dock / compact Docking Ring-compatible pad kit.
4. DL-005 Research console.
5. DL-003 static dive/research beacon.
6. DL-004 sample canister family.

**P1 — MVP zone dressing and discoveries**
DL-006 coral, DL-007 kelp, DL-008 rocks, DL-009 bioluminescent flora, DL-011 Twilight Reef arch, DL-010 small wreckage, DL-015 cave entrance pieces, DL-012 individual relic props.

**P2 — supporting station / presentation props**
DL-013 discovery display, DL-016 cables/hoses, DL-017 signage, DL-018 crates, DL-020 lighting fixtures.

**P3 — creature assets**
DL-019 small fauna, after confirming the MVP Codex's initial creature needs and keeping rigging/animation as a separately verified scope.

## Acceptance checklist for every generated asset
- [ ] The brief identifies the existing GDD feature/zone it supports.
- [ ] No post-MVP zone/tier or new gameplay system has slipped into the design.
- [ ] A real 3D model export exists; a prompt or image does not count.
- [ ] Source/export, required textures, preview, license/source and manifest are committed.
- [ ] Scale, units, pivot, bounds and mesh statistics are recorded only when actually measured.
- [ ] Mesh is appropriate for Roblox/mobile; no unnecessarily dense topology or razor-thin parts.
- [ ] No unrequested scripts, hidden loaders, unknown dependencies or invented Roblox asset IDs.
- [ ] Status is UPLOADED_TO_GITHUB only when actual model bytes are committed; Roblox Studio import remains a separate later status.

## Current limitation
This audit confirms intended scope against the approved GDD text. It does not prove visual match to the ten reference boards or compatibility with the live Studio place. The current repository notes say the live place is not present in GitHub and Studio imports have not been verified. Do not claim otherwise.