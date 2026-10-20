# Deep Lantern Model Factory Progress

Last updated: 2026-10-20
Current stage: GDD SCOPE AUDITED — PREPARATION
Current asset: DL-001 — Existing Scout / research submarine visual asset
Status: QUEUED
Actual 3D models uploaded: 0
Roblox Studio validation: NOT STARTED (intentionally deferred)

## Session checkpoint
- Read Assets/ModelFactory/README.md, PROMPT.md and GDD_COMPLIANCE_AUDIT.md first.
- Approved GDD source: GDD/DeepLantern_GDD_Parts_1-10_APPROVED.txt. It is authoritative and locked.
- Detailed briefs remain under Blender/MODEL_FACTORY/TASKS/; that directory name is historical, and Blender is not used.
- No model is complete until genuine 3D model bytes are committed under Assets/ModelFactory/Models/<ID>/.
- This audit is a plan review only; no model files have been created or Studio-tested.

## Queue status
| ID | Asset | Priority | Status | GDD guardrail | GitHub path |
|---|---|---|---|---|---|
| DL-001 | Existing Scout / research submarine visual asset | P0 | QUEUED | Do not replace gameplay/controller contracts or invent a new class | — |
| DL-002 | MVP modular station kit | P0 | QUEUED | Outpost → Station → Complex only; no Citadel/Deep Empire | — |
| DL-014 | Sub Dock / compact Docking Ring-compatible pad | P0 | QUEUED | Compact MVP function only; no public/social expansion | — |
| DL-005 | Research Lab console | P0 | QUEUED | Existing terminal visual prop only | — |
| DL-003 | Static dive/research beacon | P0 | QUEUED | Existing zone landmark; no player-built network or GPS | — |
| DL-004 | Sample canister family | P0 | QUEUED | Existing biological sample/cargo/debrief categories only | — |
| DL-006 | Coral family | P1 | QUEUED | Shallows/Twilight Reef only | — |
| DL-007 | Kelp cluster | P1 | QUEUED | Kelp Forest dressing; no complex ecosystem | — |
| DL-008 | Seafloor rock kit | P1 | QUEUED | Static geological dressing; no procedural generation | — |
| DL-009 | Bioluminescent flora | P1 | QUEUED | Existing MVP zones; no unapproved event logic | — |
| DL-011 | Twilight Reef arch | P1 | QUEUED | Landmark within Zone_TwilightReef; not a new zone | — |
| DL-010 | Small wreckage set | P1 | QUEUED | Static points of interest in an existing MVP zone | — |
| DL-015 | Cave entrance pieces | P1 | QUEUED | Existing-zone secret only; no Lost Ruins zone | — |
| DL-012 | Individual relic props | P1 | QUEUED | Existing Codex/Archive relics; full Lost Ruins is post-MVP | — |
| DL-013 | Aquarium/Gallery discovery display | P2 | QUEUED | Visual showcase only; no passive income/stat bonuses | — |
| DL-016 | Cables and hoses | P2 | QUEUED | Static dressing; no simulated cable physics or power network | — |
| DL-017 | Diegetic signage kit | P2 | QUEUED | Wayfinding only; no GPS quest markers/minimap | — |
| DL-018 | Research crates | P2 | QUEUED | Existing cargo/station dressing only | — |
| DL-020 | Lighting fixture meshes | P2 | QUEUED | Fixture meshes only; Studio lights added later | — |
| DL-019 | Small Codex fauna | P3 | QUEUED | Non-lethal, light/simple; no capture inventory or complex ecosystem | — |

## GDD compliance audit
See Assets/ModelFactory/GDD_COMPLIANCE_AUDIT.md for the full 20-item scope review, MVP/post-MVP boundaries, and acceptance checklist.

## Update rules
After each genuine model commit, update the relevant row with exact paths and commit SHA. Use BLOCKED if no real model generator/export is available. UPLOADED_TO_GITHUB only means actual model bytes are committed, not that Roblox Studio has imported or validated them. Every new Claude session must read recent commits and this file before acting.