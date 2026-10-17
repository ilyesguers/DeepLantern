--!strict

-- Mount the Dive HUD with fake values. Drop in StarterPlayerScripts to preview (requires Fusion in
-- ReplicatedStorage.Packages and the UI folder next to DesignTokens/Textures in ReplicatedStorage).

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Fusion = require(ReplicatedStorage.Packages.Fusion)
local Children = Fusion.Children
local scoped = Fusion.scoped

local UI = ReplicatedStorage.DeepLantern.UI
local DiveHUD = require(UI.DiveHUD)
local ToastHost = require(UI.Toast)

local playerGui = Players.LocalPlayer:WaitForChild("PlayerGui") :: PlayerGui
local scope = scoped(Fusion)

local battery = scope:Value(0.78)
local hull = scope:Value(0.8)
local cargoUsed = scope:Value(4)
local depth = scope:Value(428)
local dimmed = scope:Value(false)

local toastHost, pushToast = ToastHost(scope)

scope:New "ScreenGui" {
	Name = "DiveHUDDemo",
	ResetOnSpawn = false,
	IgnoreGuiInset = true,
	Parent = playerGui,

	[Children] = {
		DiveHUD(scope, {
			BatteryOxygen = battery,
			Hull = hull,
			CargoUsed = cargoUsed,
			CargoCapacity = 12,
			Depth = depth,
			ObjectiveTitle = "Scan coral samples",
			ObjectiveProgress = "3/5",
			Dimmed = dimmed,
			OnScan = function()
				pushToast("Species scanned", "discovery")
			end,
			OnRecall = function()
				pushToast("Recall started", "warning")
			end,
		}),
		toastHost,
	},
}

-- Demo only: drain the battery in steps (events), never per frame.
task.spawn(function()
	for _ = 1, 6 do
		task.wait(2)
		battery:set(math.max(Fusion.peek(battery) - 0.15, 0))
		depth:set(Fusion.peek(depth) + 40)
	end
	dimmed:set(true)
end)
