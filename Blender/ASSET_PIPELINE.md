# Blender Asset Pipeline

1. Use approved visual references and GDD; ask before adding new gameplay function.
2. Keep editable `.blend` source files separate from exported files.
3. Export a suitable format (usually FBX for meshes; confirm Studio import needs).
4. Record intended Roblox scale, origin/pivot, orientation, material slots, collision approach, triangle budget, and texture references.
5. Use clear filenames and version numbers. Do not overwrite a previously approved model.
6. Test import in a working Studio copy and inspect scale, pivot, collisions, texture appearance, and performance.
7. Do not claim a model is made/imported until the artifact exists and has been tested.

Suggested structure: `Blender/Source/`, `Assets/Models/Exports/`, `Assets/Textures/`, `Assets/Models/README.md`.