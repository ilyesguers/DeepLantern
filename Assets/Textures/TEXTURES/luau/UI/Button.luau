--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Fusion = require(ReplicatedStorage.Packages.Fusion)
local Children = Fusion.Children
local OnEvent = Fusion.OnEvent
local peek = Fusion.peek

local DesignTokens = require(script.Parent.Parent.DesignTokens)
local Textures = require(script.Parent.Parent.Textures)

type UsedAs<T> = Fusion.UsedAs<T>

export type Style = "primary" | "secondary" | "danger"
type ButtonState = "default" | "hover" | "pressed" | "focus"

export type ButtonProps = {
	Text: UsedAs<string>,
	Style: Style?,
	OnClick: (() -> ())?,
	Disabled: UsedAs<boolean>?,
	Size: UsedAs<UDim2>?,
	Position: UsedAs<UDim2>?,
	AnchorPoint: UsedAs<Vector2>?,
	LayoutOrder: UsedAs<number>?,
}

-- One state value drives the visual (never a matrix of booleans). Hit target >= 48px (GDD Part 9).
local function Button(scope: Fusion.Scope, props: ButtonProps): ImageButton
	local style: Style = props.Style or "primary"
	local pointer = scope:Value("default" :: ButtonState)

	local state = scope:Computed(function(use, _)
		if use(props.Disabled or false) then
			return "disabled"
		end
		return use(pointer)
	end)

	local function setState(value: ButtonState)
		pointer:set(value)
	end

	return scope:New "ImageButton" {
		Name = "Button",
		BackgroundTransparency = 1,
		AutoButtonColor = false,
		Size = props.Size or UDim2.fromOffset(180, DesignTokens.touch.minTarget),
		Position = props.Position,
		AnchorPoint = props.AnchorPoint,
		LayoutOrder = props.LayoutOrder,
		Active = scope:Computed(function(use, _)
			return not use(props.Disabled or false)
		end),
		Image = scope:Computed(function(use, _)
			return Textures.get(`ui/buttons/button_{style}_{use(state)}.png`)
		end),
		ScaleType = Enum.ScaleType.Slice,
		SliceCenter = DesignTokens.slices.button.center,

		[Children] = {
			scope:New "UISizeConstraint" {
				MinSize = Vector2.new(DesignTokens.touch.minTarget, DesignTokens.touch.minTarget),
			},
			scope:New "TextLabel" {
				BackgroundTransparency = 1,
				Size = UDim2.fromScale(1, 1),
				FontFace = DesignTokens.font.display,
				Text = props.Text,
				TextScaled = true,
				TextColor3 = scope:Computed(function(use, _)
					return if use(state) == "disabled" then DesignTokens.color.textMuted else DesignTokens.color.white
				end),
				[Children] = {
					scope:New "UIPadding" {
						PaddingTop = UDim.new(0.22, 0),
						PaddingBottom = UDim.new(0.22, 0),
						PaddingLeft = UDim.new(0.1, 0),
						PaddingRight = UDim.new(0.1, 0),
					},
					scope:New "UITextSizeConstraint" { MaxTextSize = DesignTokens.text.bodyLg },
				},
			},
		},

		[OnEvent "MouseEnter"] = function()
			setState("hover")
		end,
		[OnEvent "MouseLeave"] = function()
			setState("default")
		end,
		[OnEvent "MouseButton1Down"] = function()
			setState("pressed")
		end,
		[OnEvent "MouseButton1Up"] = function()
			setState("hover")
		end,
		[OnEvent "SelectionGained"] = function()
			setState("focus")
		end,
		[OnEvent "SelectionLost"] = function()
			setState("default")
		end,
		[OnEvent "Activated"] = function()
			if props.OnClick and not peek(props.Disabled or false) then
				props.OnClick()
			end
		end,
	}
end

return Button
