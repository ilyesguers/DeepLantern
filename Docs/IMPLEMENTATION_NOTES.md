# Deep Lantern — Implementation Notes

These notes clarify cross-part inconsistencies without replacing or rewriting the approved GDD. Parts 1–10 remain the authoritative design source.

## Source precedence
1. Approved GDD Parts 1–10
2. Current verified project state and existing in-game behavior
3. These implementation clarifications
4. Visual reference boards (style only)

If the GDD conflicts with current code, report the conflict and ask before changing intended behavior. If authoritative docs conflict, do not guess.

## Cross-part clarifications

### 1. Docking Ring — MVP scope
Some Part 5 context treats expanded social Docking Ring functionality as post-MVP, while Part 8 defines a compact ring for private co-op staging, crew boarding and submarine launch as an MVP feature. Implement the compact functional ring in MVP; expanded/public/social functionality remains post-MVP.

### 2. Quest example — zone naming
A Part 7 example may use `Zone_2_Twilight_Trench`; the official zone name is Twilight Reef. Use `Zone_TwilightReef` as the consistent internal identifier. This is a naming clarification, not a new zone.

### 3. Currents — simulation scope
Current-related gameplay must use lightweight scripted or trigger-based movement/navigation modifiers. Do not implement continuous fluid simulation, complex current physics or per-frame environmental physics systems.

## Technical approach
- Prefer small, reversible changes; preserve existing hierarchy, instance names, remote contracts and public APIs unless a change is approved.
- Keep gameplay server-authoritative and validate client requests on the server.
- Avoid unnecessary per-frame loops and expensive physics.
- Treat mobile layout and low-end performance as requirements.
- Reuse approved asset IDs; never invent IDs.
- Keep UI connected to actual game state, not hard-coded demo values.

## Art and assets
Reference boards are mood/design references, not ready-to-import textures or finished meshes. Production assets require source/usage notes, license/source, dimensions, scale, pivot, collision setup and verified Studio import.

## Testing and reporting
List what was inspected, changed, tested, not tested and remains risky. Never report success for tests not run. Do not save or publish without explicit user approval.