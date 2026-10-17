--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Fusion = require(ReplicatedStorage.Packages.Fusion)
local Children = Fusion.Children

local DesignTokens = require(script.Parent.Parent.DesignTokens)
local Textures = require(script.Parent.Parent.Textures)
local Icon = require(script.Parent.Icon)

type UsedAs<T> = Fusion.UsedAs<T>

export type HullBarProps = {
	Hull: UsedAs<number>, -- 0..1
	Segments: number?, -- default 6
	Size: UsedAs<UDim2>?,
	LayoutOrder: UsedAs<number>?,
}

-- Segmented hull bar (GDD Part 9: "Hull: segmented bar"). Last remaining segment renders as damaged (red).
local function HullBar(scope: Fusion.Scope, props: HullBarProps): Frame
	local count = props.Segments or 6

	local filled = scope:Computed(function(use, _)
		return math.ceil(math.clamp(use(props.Hull), 0, 1) * count - 1e-6)
	end)

	local segments = {}
	for i = 1, count do
		table.insert(
			segments,
			scope:New "ImageLabel" {
				Name = `Segment{i}`,
				BackgroundTransparency = 1,
				LayoutOrder = i,
				Size = UDim2.new(1 / count, -4, 0, 14),
				Image = scope:Computed(function(use, _)
					local n = use(filled)
					local kind = if i > n then "empty" elseif n == 1 then "damaged" else "full"
					return Textures.get(`ui/bars/hull_segment_{kind}.png`)
				end),
			}
		)
	end

	return scope:New "Frame" {
		Name = "Hull",
		BackgroundTransparency = 1,
		Size = props.Size or UDim2.new(1, 0, 0, 28),
		LayoutOrder = props.LayoutOrder,

		[Children] = {
			Icon(scope, { Key = "hud/hull", Size = UDim2.fromOffset(28, 28) }),
			scope:New "Frame" {
				Name = "Segments",
				BackgroundTransparency = 1,
				AnchorPoint = Vector2.new(0, 0.5),
				Position = UDim2.new(0, 36, 0.5, 0),
				Size = UDim2.new(1, -36 - 64, 0, 14),

				[Children] = {
					scope:New "UIListLayout" {
						FillDirection = Enum.FillDirection.Horizontal,
						SortOrder = Enum.SortOrder.LayoutOrder,
						Padding = UDim.new(0, 4),
					},
					segments,
				},
			},
			scope:New "TextLabel" {
				BackgroundTransparency = 1,
				AnchorPoint = Vector2.new(1, 0.5),
				Position = UDim2.new(1, 0, 0.5, 0),
				Size = UDim2.fromOffset(60, 20),
				FontFace = DesignTokens.font.mono,
				TextSize = DesignTokens.text.bodySm,
				TextXAlignment = Enum.TextXAlignment.Right,
				TextColor3 = DesignTokens.color.text,
				Text = scope:Computed(function(use, _)
					return `{use(filled)}/{count}`
				end),
			},
		},
	}
end

return HullBar
