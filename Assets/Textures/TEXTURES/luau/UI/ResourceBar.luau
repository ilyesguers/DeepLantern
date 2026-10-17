--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Fusion = require(ReplicatedStorage.Packages.Fusion)
local Children = Fusion.Children

local DesignTokens = require(script.Parent.Parent.DesignTokens)
local Textures = require(script.Parent.Parent.Textures)
local Icon = require(script.Parent.Icon)

type UsedAs<T> = Fusion.UsedAs<T>

export type FillStyle = "aqua" | "warning" | "critical" | "amber" | "purple" | "white"

export type ResourceBarProps = {
	IconKey: string,
	Label: string,
	Fill: UsedAs<number>, -- 0..1
	FillStyle: UsedAs<FillStyle>,
	ValueText: UsedAs<string>, -- always show text next to colour (colour-blind safe)
	Size: UsedAs<UDim2>?,
	LayoutOrder: UsedAs<number>?,
}

local TWEEN = DesignTokens.motion.base

-- Battery/Oxygen style: normal -> low (yellow) -> critical (red). The GDD defines the colour language but defers
-- exact thresholds to balancing, so these defaults are placeholders to tune in playtesting.
local function batteryStyle(scope: Fusion.Scope, fill: UsedAs<number>, low: number?, critical: number?): Fusion.Computed<FillStyle>
	local lowAt = low or 0.3
	local criticalAt = critical or 0.15
	return scope:Computed(function(use, _)
		local v = use(fill)
		if v <= criticalAt then
			return "critical"
		elseif v <= lowAt then
			return "warning"
		end
		return "aqua"
	end)
end

local function ResourceBar(scope: Fusion.Scope, props: ResourceBarProps): Frame
	local smooth = scope:Tween(
		scope:Computed(function(use, _)
			return math.clamp(use(props.Fill), 0, 1)
		end),
		TWEEN
	)

	return scope:New "Frame" {
		Name = props.Label,
		BackgroundTransparency = 1,
		Size = props.Size or UDim2.new(1, 0, 0, 28),
		LayoutOrder = props.LayoutOrder,

		[Children] = {
			Icon(scope, {
				Key = props.IconKey,
				Size = UDim2.fromOffset(28, 28),
			}),
			scope:New "ImageLabel" {
				Name = "Track",
				BackgroundTransparency = 1,
				AnchorPoint = Vector2.new(0, 0.5),
				Position = UDim2.new(0, 36, 0.5, 0),
				Size = UDim2.new(1, -36 - 64, 0, 14),
				Image = Textures.get(DesignTokens.slices.bar.image),
				ScaleType = Enum.ScaleType.Slice,
				SliceCenter = DesignTokens.slices.bar.center,
				ClipsDescendants = true,

				[Children] = scope:New "ImageLabel" {
					Name = "Fill",
					BackgroundTransparency = 1,
					Size = scope:Computed(function(use, _)
						return UDim2.fromScale(use(smooth), 1)
					end),
					Image = scope:Computed(function(use, _)
						return Textures.get(`ui/bars/bar_fill_{use(props.FillStyle)}.png`)
					end),
					ScaleType = Enum.ScaleType.Slice,
					SliceCenter = DesignTokens.slices.bar.center,
				},
			},
			scope:New "TextLabel" {
				Name = "Value",
				BackgroundTransparency = 1,
				AnchorPoint = Vector2.new(1, 0.5),
				Position = UDim2.new(1, 0, 0.5, 0),
				Size = UDim2.fromOffset(60, 20),
				FontFace = DesignTokens.font.mono,
				TextSize = DesignTokens.text.bodySm,
				TextXAlignment = Enum.TextXAlignment.Right,
				TextColor3 = DesignTokens.color.text,
				Text = props.ValueText,
			},
		},
	}
end

return {
	new = ResourceBar,
	batteryStyle = batteryStyle,
}
