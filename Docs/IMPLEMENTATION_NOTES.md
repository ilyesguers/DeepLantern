# Deep Lantern — Implementation Notes

These notes clarify how to implement the approved GDD without introducing new design decisions.

## Source precedence
1. Approved GDD Parts 1–10
2. Current verified project state and existing in-game behavior
3. This implementation note
4. Visual reference boards (style only)

If the GDD conflicts with the current code, report the conflict and ask before changing intended behavior. If two authoritative docs conflict, do not guess.

## Technical approach
- Prefer small, reversible changes.
- Preserve existing hierarchy, instance names, remote contracts, and public APIs unless a change is approved.
- Avoid unnecessary per-frame loops and expensive physics. Currents should use lightweight triggers/scripts.
- Keep server-authoritative gameplay and validate client requests on the server.
- Treat mobile layout and low-end performance as requirements, not later polish.
- Use existing approved asset IDs when available; never invent IDs.
- Keep UI connected to actual game state, not hard-coded demonstration values.

## Art and assets
Visual references are mood/design references, not ready-to-import textures or finished meshes. Production assets require clear source files, usage notes, license/source, scale, pivot, collision setup, and a verified Studio import.

## Testing/reporting
For each task list what was inspected, changed, tested, not tested, and remains risky. Do not report success for tests that were not run. Do not save/publish without explicit user approval.
