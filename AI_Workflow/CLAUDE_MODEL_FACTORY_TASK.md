# Claude task — produce the Deep Lantern model set in Roblox Studio

Read AI_Workflow/CLAUDE_ROBLOX_STUDIO_MODEL_FACTORY.md and AI_Workflow/AI_AGENT_RULES.md before doing anything.

User explicitly does not want Blender. Use Roblox Studio-native construction and the linked skills at https://github.com/afrxo/roblox-agent-skills. The roblox-ui skill is for UI/Fusion, not 3D model generation. Do not claim GitHub access equals Studio access.

First, verify a real Roblox Studio MCP/agent connection and list available studios. If connected, confirm the exact open place and work only in a separately named working copy. Never overwrite save.rbxl or DeepLantern_Backup_Oct09.rbxl, never publish, and do not modify main directly. If not connected, report the exact missing setup and prepare idempotent Luau builder scripts that only create content under Workspace.DeepLantern_ModelFactoryPreview; do not claim they were executed.

Inspect the current project and all existing models before creating duplicates. Follow approved GDD Parts 1–10, PROJECT_STATE.md, AI_START_HERE.md, and the 20 task briefs under Blender/MODEL_FACTORY/TASKS (the folder name is historical; no Blender use). Keep current gameplay, scripts, currencies, UI, exact Zone_TwilightReef identifier and progression unchanged.

Work in order, one asset at a time, starting DL-001 research submarine, then DL-002 research station kit, DL-003 dive beacon, DL-004 sample canisters, DL-005 research console. After each model: build with deliberate, layered silhouettes and cohesive materials; inspect/read back the result; check scale, pivot, collisions, clipping, distance readability and mobile/low-end performance; export .rbxm/.rbxmx if supported; add source, manifest, and evidence to this feature branch; update the status record with only facts verified. Continue through DL-020 after P0 checks pass.

Do not produce generic piles of cubes or excessive tiny Parts. Do not invent texture IDs or represent native Parts as MeshParts. Prefer efficient geometry, few lights, no unnecessary physics or per-frame effects. Review any third-party inserted asset for suspicious scripts before retaining it.

Keep changes on the existing feature branch assets/roblox-studio-model-factory. Create a pull request when the source/export/manifest is ready. Do not merge. Report exact files changed, model status, Studio evidence, actual tests, limitations, and rollback path. A prompt, specification, or builder script alone is not a completed model.