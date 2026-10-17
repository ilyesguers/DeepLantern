# GitHub Workflow — Review First

GitHub stores approved docs, code source, art references, and source assets. Roblox Studio is the live DataModel/playtest environment; GitHub does not automatically synchronize with Studio.

For each task:
1. Read the source-of-truth docs.
2. Inspect current files and exact Studio hierarchy.
3. Create an isolated branch or clearly scoped change.
4. Present plan, paths, risks, and test plan.
5. Implement only after user approval.
6. Run available static checks and Studio tests.
7. Summarize diff, actual tests, risks, rollback, and unsaved state.
8. Update CHANGELOG and agent handoff.

Folders: `Art/VisualReference/` for reference boards; `Assets/Textures/` for actual textures; `Assets/Models/` for exported models; `Blender/` for model pipeline; `Roblox/` for Studio integration notes. Never label reference images as production textures/models. Large binary files require deliberate storage planning.