# Blender Asset Pipeline

Blender is a separate asset-authoring stage; do not assume it is automatically connected to Codex/Claude or Roblox Studio.

For each approved model, create a folder under `Assets/Models/<AssetName>/` containing:
- editable `.blend` source;
- exported `.fbx` (or a format agreed for the asset);
- `README.md` with intended use, scale in studs/meters, origin/pivot, triangle estimate, material/texture list, collision plan, and export settings;
- preview PNG;
- source/license notes for third-party inputs.

## Roblox import checklist
- Confirm sensible scale and pivot/origin.
- Keep geometry and texture sizes efficient.
- Use separate collision geometry where needed.
- Confirm materials/textures are correctly packed or exported.
- Import into a separate working copy in Studio and verify scale, pivot, collisions, texture appearance, and performance before calling it complete.

Start with one low-risk prop, not a full station or submarine. A Blender MCP bridge is optional and must be separately evaluated/configured; do not install unknown scripts blindly. Never save/publish the live place without explicit approval.
