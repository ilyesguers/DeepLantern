# Deep Lantern Model Factory Progress

Last updated: 2026-10-20
Current stage: PREPARATION
Current asset: DL-001 — Deep-Diving Research Submarine
Status: QUEUED
Actual 3D models uploaded: 0
Roblox Studio validation: NOT STARTED (intentionally deferred)

## Session checkpoint
- The task briefs are under `Blender/MODEL_FACTORY/TASKS/`; the folder name is historical and Blender is not to be used.
- The reusable continuation prompt is `Assets/ModelFactory/PROMPT.md`.
- The GitHub-first workflow is `Assets/ModelFactory/README.md`.
- No model should be counted complete until actual 3D model file bytes are committed to `Assets/ModelFactory/Models/<ID>/`.

## Queue status
| ID | Asset | Priority | Status | GitHub path | Notes |
|---|---|---|---|---|---|
| DL-001 | Research submarine | P0 | QUEUED | — | First task |
| DL-002 | Modular research station kit | P0 | QUEUED | — | 12 reusable modules |
| DL-003 | Dive beacon / sonar buoy | P0 | QUEUED | — | Bottom pivot |
| DL-004 | Sample canister family | P0 | QUEUED | — | 3 variants |
| DL-005 | Research console | P0 | QUEUED | — | Visual prop only |
| DL-006 | Coral family | P1 | QUEUED | — | 5 silhouettes |
| DL-007 | Kelp cluster | P1 | QUEUED | — | Small/medium/tall |
| DL-008 | Seafloor rock kit | P1 | QUEUED | — | 6 forms |
| DL-009 | Bioluminescent flora | P1 | QUEUED | — | 3 assets |
| DL-010 | Wreckage set | P1 | QUEUED | — | 6 props |
| DL-011 | Twilight Reef arch | P1 | QUEUED | — | Landmark |
| DL-012 | Ancient relic | P1 | QUEUED | — | Landmark |
| DL-013 | Discovery display | P2 | QUEUED | — | Visual prop only |
| DL-014 | Docking pad and service arm | P2 | QUEUED | — | Keep gameplay unchanged |
| DL-015 | Cave entrance kit | P2 | QUEUED | — | Modular pieces |
| DL-016 | Cable/hose kit | P2 | QUEUED | — | Reusable pieces |
| DL-017 | Signage kit | P2 | QUEUED | — | Blank replaceable signs |
| DL-018 | Research crates | P2 | QUEUED | — | 3 variants |
| DL-019 | Small fauna | P3 | QUEUED | — | Animation/rigging later |
| DL-020 | Lighting fixture kit | P2 | QUEUED | — | Meshes only; Studio lights later |

## Update rules
After each real model commit, update that row and add the commit SHA and exact file paths. Status must be BLOCKED if no genuine model-generation/export tool can create a 3D file. UPLOADED_TO_GITHUB only means the file exists in the repository, not that it has been imported or validated in Roblox Studio. The next session must read recent commits and this file before acting.
