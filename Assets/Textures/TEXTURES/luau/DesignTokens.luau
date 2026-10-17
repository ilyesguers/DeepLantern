--!strict

-- Deep Lantern design tokens. Single source of truth for colours, type, spacing and motion.
-- Follows the roblox-agent-skills "roblox-ui" guidelines: semantic roles, no inline colours at call sites.
-- GDD Part 9: dark navy / restrained teal-cyan / warm amber / crimson alert; glass panels, 1px teal borders,
-- subtle chamfer, glow only when functional. No continuous per-frame UI updates.

export type Slice = {
	image: string,
	center: Rect,
}

export type Tokens = {
	color: {
		abyss: Color3,
		deep: Color3,
		navy: Color3,
		panel: Color3,
		teal: Color3,
		aqua: Color3,
		aquaSoft: Color3,
		purple: Color3,
		amber: Color3,
		gold: Color3,
		white: Color3,
		text: Color3,
		textMuted: Color3,
		success: Color3,
		warning: Color3,
		danger: Color3,
		info: Color3,
	},
	space: { xs: number, sm: number, md: number, lg: number, xl: number, xxl: number },
	text: { caption: number, bodySm: number, body: number, bodyLg: number, h3: number, h2: number, h1: number, display: number },
	radius: { chamfer: number },
	touch: { minTarget: number },
	toastSeconds: number,
	dimAfterSeconds: number,
	font: { body: Font, display: Font, mono: Font },
	motion: { fast: TweenInfo, base: TweenInfo, slow: TweenInfo },
	-- Resource bar colour by state (Battery/Oxygen, Hull). Always pair with icon + text (colour-blind safe).
	resource: { normal: Color3, low: Color3, critical: Color3, cargo: Color3, research: Color3 },
	slices: {
		panel: Slice,
		panelDim: Slice,
		panelElevated: Slice,
		panelAlert: Slice,
		panelWarning: Slice,
		panelDiscovery: Slice,
		toast: Slice,
		button: Slice,
		bar: Slice,
	},
}

local function hex(h: string): Color3
	return Color3.fromHex(h)
end

local tokens: Tokens = {
	color = {
		abyss = hex("#050E1F"),
		deep = hex("#081E3B"),
		navy = hex("#0B2447"),
		panel = hex("#0D2A52"),
		teal = hex("#14B8A6"),
		aqua = hex("#00D1FF"),
		aquaSoft = hex("#6BEAFF"),
		purple = hex("#8B5CF6"),
		amber = hex("#F59E0B"),
		gold = hex("#FBBF24"),
		white = hex("#E6F1FF"),
		text = hex("#E6F1FF"),
		textMuted = hex("#8FA8C8"),
		success = hex("#4ADE80"),
		warning = hex("#FBBF24"),
		danger = hex("#EF4444"),
		info = hex("#2AD8FF"),
	},
	-- Pixel values for UIPadding / UIListLayout.Padding on a 1080p reference; scale with UIScale.
	space = { xs = 4, sm = 8, md = 12, lg = 16, xl = 24, xxl = 32 },
	text = { caption = 12, bodySm = 14, body = 16, bodyLg = 18, h3 = 24, h2 = 32, h1 = 40, display = 56 },
	radius = { chamfer = 7 },
	touch = { minTarget = 48 }, -- GDD Part 9: mobile hitboxes >= ~48x48
	toastSeconds = 3, -- GDD Part 9: toasts auto-disappear after ~3s
	dimAfterSeconds = 5, -- GDD Part 9: non-essential HUD dims after ~5s stable cruising
	font = {
		body = Font.fromName("BuilderSans", Enum.FontWeight.Medium), -- geometric sans
		display = Font.fromName("BuilderSans", Enum.FontWeight.Bold),
		mono = Font.fromName("RobotoMono", Enum.FontWeight.Regular), -- numeric readouts
	},
	motion = {
		fast = TweenInfo.new(0.12, Enum.EasingStyle.Quad, Enum.EasingDirection.Out),
		base = TweenInfo.new(0.2, Enum.EasingStyle.Quad, Enum.EasingDirection.Out),
		slow = TweenInfo.new(0.35, Enum.EasingStyle.Sine, Enum.EasingDirection.Out),
	},
	resource = {
		normal = hex("#00D1FF"),
		low = hex("#FBBF24"),
		critical = hex("#EF4444"),
		cargo = hex("#F59E0B"),
		research = hex("#8B5CF6"),
	},
	slices = {
		panel = { image = "ui/panels/panel_glass.png", center = Rect.new(16, 16, 48, 48) },
		panelDim = { image = "ui/panels/panel_glass_dim.png", center = Rect.new(16, 16, 48, 48) },
		panelElevated = { image = "ui/panels/panel_glass_elevated.png", center = Rect.new(16, 16, 48, 48) },
		panelAlert = { image = "ui/panels/panel_glass_alert.png", center = Rect.new(16, 16, 48, 48) },
		panelWarning = { image = "ui/panels/panel_glass_warning.png", center = Rect.new(16, 16, 48, 48) },
		panelDiscovery = { image = "ui/panels/panel_glass_discovery.png", center = Rect.new(16, 16, 48, 48) },
		toast = { image = "ui/panels/panel_toast.png", center = Rect.new(14, 14, 50, 18) },
		button = { image = "ui/buttons/button_primary_default.png", center = Rect.new(14, 12, 50, 20) },
		bar = { image = "ui/bars/bar_track.png", center = Rect.new(8, 7, 24, 9) },
	},
}

return table.freeze(tokens)
