--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Fusion = require(ReplicatedStorage.Packages.Fusion)
local Children = Fusion.Children

local Textures = require(script.Parent.Parent.Textures)

type UsedAs<T> = Fusion.UsedAs<T>

export type IconProps = {
	Key: string, -- "hud/hull", "resources/crystal", ...
	Glyph: boolean?, -- white silhouette, tinted by Tint
	Tint: UsedAs<Color3>?,
	Size: UsedAs<UDim2>?,
	Position: UsedAs<UDim2>?,
	AnchorPoint: UsedAs<Vector2>?,
	LayoutOrder: UsedAs<number>?,
}

local function Icon(scope: Fusion.Scope, props: IconProps): ImageLabel
	local atlas = Textures.atlasIcon(props.Key, props.Glyph)
	return scope:New "ImageLabel" {
		Name = "Icon",
		BackgroundTransparency = 1,
		Size = props.Size or UDim2.fromOffset(32, 32),
		Position = props.Position,
		AnchorPoint = props.AnchorPoint,
		LayoutOrder = props.LayoutOrder,
		Image = atlas.image,
		ImageRectOffset = atlas.offset,
		ImageRectSize = atlas.size,
		ImageColor3 = props.Tint or Color3.new(1, 1, 1),

		[Children] = scope:New "UIAspectRatioConstraint" { AspectRatio = 1 },
	}
end

return Icon
