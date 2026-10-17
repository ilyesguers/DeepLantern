--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Fusion = require(ReplicatedStorage.Packages.Fusion)
local Children = Fusion.Children
local OnEvent = Fusion.OnEvent

local DesignTokens = require(script.Parent.Parent.DesignTokens)
local Icon = require(script.Parent.Icon)
local Panel = require(script.Parent.Panel)
local ResourceBar = require(script.Parent.ResourceBar)
local HullBar = require(script.Parent.HullBar)

type UsedAs<T> = Fusion.UsedAs<T>

export type DiveHUDProps = {
	BatteryOxygen: UsedAs<number>, -- 0..1, ONE unified resource (GDD: no separate Oxygen/Fuel/Energy)
	Hull: UsedAs<number>, -- 0..1
	CargoUsed: UsedAs<number>,
	CargoCapacity: UsedAs<number>,
	Depth: UsedAs<number>, -- display unit decided in balancing; shown as plain number
	ObjectiveTitle: UsedAs<string>,
	ObjectiveProgress: UsedAs<string>, -- e.g. "2/5"
	Dimmed: UsedAs<boolean>?, -- controller sets true after ~5s of stable cruising, false on important events
	OnLantern: (() -> ())?,
	OnScan: (() -> ())?,
	OnPing: (() -> ())?,
	OnRecall: (() -> ())?,
}

local function ToolButton(scope: Fusion.Scope, iconKey: string, label: string, order: number, onClick: (() -> ())?): ImageButton
	return scope:New "ImageButton" {
		Name = label,
		LayoutOrder = order,
		AutoButtonColor = false,
		BackgroundTransparency = 1,
		Size = UDim2.fromOffset(DesignTokens.touch.minTarget + 8, DesignTokens.touch.minTarget + 8),

		[Children] = Icon(scope, { Key = iconKey, Size = UDim2.fromScale(1, 1) }),

		[OnEvent "Activated"] = function()
			if onClick then
				onClick()
			end
		end,
	}
end

-- Dive HUD per GDD Part 9: Level 1 (critical) always visible; Level 2 dims when cruising.
-- Event-driven: every value arrives as a Fusion state, nothing polls per frame.
local function DiveHUD(scope: Fusion.Scope, props: DiveHUDProps): Frame
	local dimmed = props.Dimmed or false
	local dimTween = scope:Tween(
		scope:Computed(function(use, _)
			return if use(dimmed) then 0.55 else 0
		end),
		DesignTokens.motion.slow
	)

	local batteryFill = props.BatteryOxygen
	local cargoFill = scope:Computed(function(use, _)
		local cap = math.max(use(props.CargoCapacity), 1)
		return use(props.CargoUsed) / cap
	end)

	return scope:New "Frame" {
		Name = "DiveHUD",
		BackgroundTransparency = 1,
		Size = UDim2.fromScale(1, 1),

		[Children] = {
			-- Level 1: critical status, never dimmed.
			Panel(scope, {
				Name = "Status",
				Variant = "default",
				Position = UDim2.new(0, DesignTokens.space.xl, 0, DesignTokens.space.xl),
				Size = UDim2.fromOffset(320, 150),
				Padding = DesignTokens.space.md,
				Children = {
					scope:New "UIListLayout" {
						FillDirection = Enum.FillDirection.Vertical,
						SortOrder = Enum.SortOrder.LayoutOrder,
						Padding = UDim.new(0, DesignTokens.space.sm),
					},
					ResourceBar.new(scope, {
						IconKey = "hud/battery_oxygen",
						Label = "BatteryOxygen",
						Fill = batteryFill,
						FillStyle = ResourceBar.batteryStyle(scope, batteryFill),
						ValueText = scope:Computed(function(use, _)
							return `{math.round(use(batteryFill) * 100)}%`
						end),
						LayoutOrder = 1,
					}),
					HullBar(scope, { Hull = props.Hull, LayoutOrder = 2 }),
					ResourceBar.new(scope, {
						IconKey = "hud/cargo",
						Label = "Cargo",
						Fill = cargoFill,
						FillStyle = "amber",
						ValueText = scope:Computed(function(use, _)
							return `{use(props.CargoUsed)} / {use(props.CargoCapacity)}`
						end),
						LayoutOrder = 3,
					}),
				},
			}),

			Panel(scope, {
				Name = "Depth",
				Variant = "dim",
				AnchorPoint = Vector2.new(0.5, 0),
				Position = UDim2.new(0.5, 0, 0, DesignTokens.space.xl),
				Size = UDim2.fromOffset(180, 48),
				Padding = DesignTokens.space.sm,
				Children = {
					Icon(scope, {
						Key = "hud/depth",
						Size = UDim2.fromOffset(28, 28),
						AnchorPoint = Vector2.new(0, 0.5),
						Position = UDim2.fromScale(0, 0.5),
					}),
					scope:New "TextLabel" {
						BackgroundTransparency = 1,
						AnchorPoint = Vector2.new(1, 0.5),
						Position = UDim2.fromScale(1, 0.5),
						Size = UDim2.new(1, -36, 1, 0),
						FontFace = DesignTokens.font.mono,
						TextSize = DesignTokens.text.h3,
						TextXAlignment = Enum.TextXAlignment.Right,
						TextColor3 = DesignTokens.color.aquaSoft,
						Text = scope:Computed(function(use, _)
							return tostring(math.round(use(props.Depth)))
						end),
					},
				},
			}),

			-- Level 2: dims after stable cruising, brightens on important events.
			scope:New "CanvasGroup" {
				Name = "Secondary",
				BackgroundTransparency = 1,
				Size = UDim2.fromScale(1, 1),
				GroupTransparency = dimTween,

				[Children] = {
					Panel(scope, {
						Name = "Objective",
						Variant = "dim",
						AnchorPoint = Vector2.new(1, 0),
						Position = UDim2.new(1, -DesignTokens.space.xl, 0, DesignTokens.space.xl),
						Size = UDim2.fromOffset(300, 64),
						Padding = DesignTokens.space.md,
						Children = {
							Icon(scope, {
								Key = "hud/objective",
								Size = UDim2.fromOffset(32, 32),
								AnchorPoint = Vector2.new(0, 0.5),
								Position = UDim2.fromScale(0, 0.5),
							}),
							scope:New "TextLabel" {
								BackgroundTransparency = 1,
								AnchorPoint = Vector2.new(1, 0.5),
								Position = UDim2.fromScale(1, 0.5),
								Size = UDim2.new(1, -42, 1, 0),
								FontFace = DesignTokens.font.body,
								TextSize = DesignTokens.text.bodySm,
								TextXAlignment = Enum.TextXAlignment.Left,
								TextWrapped = true,
								TextColor3 = DesignTokens.color.text,
								Text = scope:Computed(function(use, _)
									return `{use(props.ObjectiveTitle)}  {use(props.ObjectiveProgress)}`
								end),
							},
						},
					}),

					scope:New "Frame" {
						Name = "Tools",
						BackgroundTransparency = 1,
						AnchorPoint = Vector2.new(0.5, 1),
						Position = UDim2.new(0.5, 0, 1, -DesignTokens.space.xl),
						Size = UDim2.fromOffset(4 * (DesignTokens.touch.minTarget + 8) + 3 * DesignTokens.space.md, DesignTokens.touch.minTarget + 8),

						[Children] = {
							scope:New "UIListLayout" {
								FillDirection = Enum.FillDirection.Horizontal,
								HorizontalAlignment = Enum.HorizontalAlignment.Center,
								SortOrder = Enum.SortOrder.LayoutOrder,
								Padding = UDim.new(0, DesignTokens.space.md),
							},
							ToolButton(scope, "hud/lantern", "Lantern", 1, props.OnLantern),
							ToolButton(scope, "hud/scanner", "Scanner", 2, props.OnScan),
							ToolButton(scope, "hud/ping", "Ping", 3, props.OnPing),
							ToolButton(scope, "hud/recall", "Recall", 4, props.OnRecall),
						},
					},
				},
			},
		},
	}
end

return DiveHUD
