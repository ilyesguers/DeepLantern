--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Fusion = require(ReplicatedStorage.Packages.Fusion)
local Children = Fusion.Children
local peek = Fusion.peek

local DesignTokens = require(script.Parent.Parent.DesignTokens)
local Panel = require(script.Parent.Panel)
local Icon = require(script.Parent.Icon)

export type Kind = "info" | "research" | "warning" | "discovery"
type ToastData = { id: number, text: string, kind: Kind }

local MAX_VISIBLE = 3 -- GDD Part 9: small toasts, never full-screen banners

local KIND_STYLE: { [Kind]: { variant: Panel.Variant, icon: string } } = {
	info = { variant = "default", icon = "hud/check" },
	research = { variant = "discovery", icon = "hud/research_data" },
	warning = { variant = "warning", icon = "hud/warning" },
	discovery = { variant = "discovery", icon = "hud/codex" },
}

-- Small stack of auto-dismissing toasts (~3s). Returns the host Frame and a push() function.
local function ToastHost(scope: Fusion.Scope): (Frame, (text: string, kind: Kind?) -> ())
	local list = scope:Value({} :: { ToastData })
	local nextId = 0

	local function remove(id: number)
		local kept = {}
		for _, toast in peek(list) do
			if toast.id ~= id then
				table.insert(kept, toast)
			end
		end
		list:set(kept)
	end

	local function push(text: string, kind: Kind?)
		nextId += 1
		local id = nextId
		local copy = table.clone(peek(list))
		table.insert(copy, { id = id, text = text, kind = kind or "info" })
		while #copy > MAX_VISIBLE do
			table.remove(copy, 1)
		end
		list:set(copy)
		task.delay(DesignTokens.toastSeconds, remove, id)
	end

	local host = scope:New "Frame" {
		Name = "ToastHost",
		BackgroundTransparency = 1,
		AnchorPoint = Vector2.new(0.5, 1),
		Position = UDim2.new(0.5, 0, 1, -DesignTokens.space.xxl),
		Size = UDim2.fromOffset(360, 200),

		[Children] = {
			scope:New "UIListLayout" {
				FillDirection = Enum.FillDirection.Vertical,
				VerticalAlignment = Enum.VerticalAlignment.Bottom,
				HorizontalAlignment = Enum.HorizontalAlignment.Center,
				SortOrder = Enum.SortOrder.LayoutOrder,
				Padding = UDim.new(0, DesignTokens.space.sm),
			},
			scope:ForValues(list, function(use, innerScope, toast: ToastData)
				local style = KIND_STYLE[toast.kind]
				return Panel(innerScope, {
					Name = `Toast{toast.id}`,
					Variant = style.variant,
					Size = UDim2.new(1, 0, 0, 44),
					LayoutOrder = toast.id,
					Padding = DesignTokens.space.sm,
					Children = {
						Icon(innerScope, {
							Key = style.icon,
							Size = UDim2.fromOffset(28, 28),
							AnchorPoint = Vector2.new(0, 0.5),
							Position = UDim2.fromScale(0, 0.5),
						}),
						innerScope:New "TextLabel" {
							BackgroundTransparency = 1,
							AnchorPoint = Vector2.new(1, 0.5),
							Position = UDim2.fromScale(1, 0.5),
							Size = UDim2.new(1, -38, 1, 0),
							FontFace = DesignTokens.font.body,
							TextSize = DesignTokens.text.bodySm,
							TextXAlignment = Enum.TextXAlignment.Left,
							TextColor3 = DesignTokens.color.text,
							Text = toast.text,
						},
					},
				})
			end),
		},
	}

	return host, push
end

return ToastHost
