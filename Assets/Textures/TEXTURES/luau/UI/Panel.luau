--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Fusion = require(ReplicatedStorage.Packages.Fusion)
local Children = Fusion.Children

local DesignTokens = require(script.Parent.Parent.DesignTokens)
local Textures = require(script.Parent.Parent.Textures)

type UsedAs<T> = Fusion.UsedAs<T>

export type Variant = "default" | "dim" | "elevated" | "alert" | "warning" | "discovery"

export type PanelProps = {
	Name: string?,
	Variant: Variant?,
	Size: UsedAs<UDim2>?,
	Position: UsedAs<UDim2>?,
	AnchorPoint: UsedAs<Vector2>?,
	LayoutOrder: UsedAs<number>?,
	Padding: number?, -- pixels, defaults to DesignTokens.space.lg
	Children: any?,
}

local slices = DesignTokens.slices
local VARIANT_SLICE = {
	default = slices.panel,
	dim = slices.panelDim,
	elevated = slices.panelElevated,
	alert = slices.panelAlert,
	warning = slices.panelWarning,
	discovery = slices.panelDiscovery,
}

-- Chamfered glass panel. The chamfer is baked into the 9-slice, so no UICorner here.
local function Panel(scope: Fusion.Scope, props: PanelProps): ImageLabel
	local slice = VARIANT_SLICE[props.Variant or "default"]
	local pad = props.Padding or DesignTokens.space.lg

	return scope:New "ImageLabel" {
		Name = props.Name or "Panel",
		BackgroundTransparency = 1,
		Size = props.Size or UDim2.fromScale(0.2, 0.2),
		Position = props.Position,
		AnchorPoint = props.AnchorPoint,
		LayoutOrder = props.LayoutOrder,
		Image = Textures.get(slice.image),
		ScaleType = Enum.ScaleType.Slice,
		SliceCenter = slice.center,

		[Children] = {
			scope:New "UIPadding" {
				PaddingTop = UDim.new(0, pad),
				PaddingBottom = UDim.new(0, pad),
				PaddingLeft = UDim.new(0, pad),
				PaddingRight = UDim.new(0, pad),
			},
			props.Children,
		},
	}
end

return Panel
