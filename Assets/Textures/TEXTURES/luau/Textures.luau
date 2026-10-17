--!strict

-- Resolves a repo-relative texture path (see manifest.json) to an rbxassetid after upload.
-- Ids live in AssetIds.luau. A missing id returns "" (renders nothing) instead of erroring,
-- so UI/world code keeps working while assets are still being uploaded.

local AssetIds = require(script.Parent.AssetIds)
local AtlasData = require(script.Parent.AtlasData)

export type AtlasIcon = { image: string, offset: Vector2, size: Vector2 }

local Textures = {}

function Textures.get(path: string): string
	local id = AssetIds[path]
	if id == nil then
		warn(`[Textures] unknown texture path: {path}`)
		return ""
	end
	return id
end

-- Atlas lookup (preferred for icons: 4 uploads instead of 222). key = "hud/hull".
function Textures.atlasIcon(key: string, glyph: boolean?): AtlasIcon
	local entry = AtlasData.icons[key]
	if entry == nil then
		warn(`[Textures] unknown icon: {key}`)
		return { image = "", offset = Vector2.zero, size = Vector2.zero }
	end
	local cell = if glyph then entry.glyph else entry.plated
	return {
		image = Textures.get(cell.sheet),
		offset = Vector2.new(cell.x, cell.y),
		size = Vector2.new(AtlasData.cell, AtlasData.cell),
	}
end

-- Single-file icon helpers: category/name, e.g. Textures.icon("hud/battery_oxygen")
function Textures.icon(key: string): string
	return Textures.get(`icons/{key}.png`)
end

-- White silhouette; tint with ImageColor3.
function Textures.glyph(key: string): string
	return Textures.get(`icons/glyph/{key}.png`)
end

-- Fill the ImageLabel/ImageButton for a 9-slice panel. `slice` comes from DesignTokens.slices.
function Textures.applySlice(img: ImageLabel | ImageButton, slice: { image: string, center: Rect })
	img.Image = Textures.get(slice.image)
	img.ScaleType = Enum.ScaleType.Slice
	img.SliceCenter = slice.center
	img.BackgroundTransparency = 1
end

-- Build a SurfaceAppearance from a material folder (materials/<name>/*.png).
function Textures.surfaceAppearance(material: string): SurfaceAppearance
	local sa = Instance.new("SurfaceAppearance")
	sa.ColorMap = Textures.get(`materials/{material}/color.png`)
	sa.NormalMap = Textures.get(`materials/{material}/normal.png`)
	sa.RoughnessMap = Textures.get(`materials/{material}/roughness.png`)
	sa.MetalnessMap = Textures.get(`materials/{material}/metalness.png`)
	return sa
end

return Textures
