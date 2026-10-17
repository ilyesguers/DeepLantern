# Roblox Studio Agent / MCP Setup Checklist

1. Save a separate working copy of the place; do not overwrite `save.rbxl` or `DeepLantern_Backup_Oct09.rbxl`.
2. In Roblox Studio, open Assistant settings and locate MCP Servers (wording varies by Studio version); enable Studio as an MCP server.
3. Follow the official `Roblox/roblox-studio-agent-plugin` setup for the selected agent/client.
4. Restart the client or start a new thread if required.
5. Ask the agent to list open Roblox Studio windows and inspect the project.
6. First use is inspection-only. Confirm the agent actually sees the correct place before authorizing edits.

Official setup repository: https://github.com/Roblox/roblox-studio-agent-plugin

Never share credentials, tokens, or private secrets in prompts. Tools may transmit scripts, properties, console output, and screenshots to the AI provider. Review permissions and data handling before use.