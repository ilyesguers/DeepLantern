-- Deep Lantern: free procedural asset-pack preview
-- Run manually in Roblox Studio's Command Bar in a TEST PLACE only.
-- Creates a new folder in Workspace; it never edits existing game objects.
-- Delete Workspace.DeepLantern_AssetPack_Preview to roll back.
local Workspace = game:GetService("Workspace")
local folderName = "DeepLantern_AssetPack_Preview"
assert(not Workspace:FindFirstChild(folderName), "Preview folder already exists; delete it manually before rerunning.")

local pack = Instance.new("Folder")
pack.Name = folderName
pack.Parent = Workspace

local C = {
    navy = Color3.fromRGB(17, 35, 54),
    metal = Color3.fromRGB(44, 65, 79),
    teal = Color3.fromRGB(30, 177, 173),
    cyan = Color3.fromRGB(76, 231, 242),
    amber = Color3.fromRGB(255, 174, 67),
    glass = Color3.fromRGB(21, 93, 111),
    coral1 = Color3.fromRGB(44, 145, 139),
    coral2 = Color3.fromRGB(70, 183, 164),
    rock = Color3.fromRGB(48, 73, 80),
}
local function part(parent, name, size, cf, color, material, shape)
    local p = Instance.new("Part")
    p.Name = name
    p.Size = size
    p.CFrame = cf
    p.Anchored = true
    p.Color = color
    p.Material = material or Enum.Material.Metal
    p.TopSurface = Enum.SurfaceType.Smooth
    p.BottomSurface = Enum.SurfaceType.Smooth
    if shape then p.Shape = shape end
    p.Parent = parent
    return p
end
local function model(name, position)
    local m = Instance.new("Model")
    m.Name = name
    m.Parent = pack
    m:SetAttribute("PackStatus", "ProceduralPreview_NotStudioVerified")
    m.PrimaryPart = part(m, "Root", Vector3.new(1,1,1), CFrame.new(position), C.navy, Enum.Material.SmoothPlastic)
    m.PrimaryPart.Transparency = 1
    m.PrimaryPart.CanCollide = false
    return m
end
local function console(position)
    local m = model("ResearchConsole", position)
    local x,y,z = position.X, position.Y, position.Z
    part(m,"Base",Vector3.new(5,0.7,2.4),CFrame.new(x,y+0.35,z),C.navy)
    part(m,"Body",Vector3.new(4.4,2.2,1.5),CFrame.new(x,y+1.65,z+0.15),C.metal)
    part(m,"ScreenFrame",Vector3.new(3.5,1.35,0.18),CFrame.new(x,y+2.15,z-0.68),C.navy)
    local screen = part(m,"Display",Vector3.new(3.18,1.05,0.08),CFrame.new(x,y+2.15,z-0.79),C.glass,Enum.Material.Neon)
    screen:SetAttribute("DecorativeOnly", true)
    part(m,"StatusLight",Vector3.new(0.18,0.18,0.12),CFrame.new(x+1.75,y+1.05,z-0.72),C.amber,Enum.Material.Neon,Enum.PartType.Ball)
    for i=1,4 do
        part(m,"Button"..i,Vector3.new(0.28,0.12,0.16),CFrame.new(x-1.1+(i-1)*0.48,y+1.05,z-0.72),i%2==0 and C.cyan or C.teal,Enum.Material.Neon)
    end
end
local function beacon(position)
    local m = model("DiveBeacon", position)
    local x,y,z = position.X,position.Y,position.Z
    part(m,"Foot",Vector3.new(1.5,0.25,1.5),CFrame.new(x,y+0.125,z),C.navy)
    part(m,"Stem",Vector3.new(0.35,2,0.35),CFrame.new(x,y+1.2,z),C.metal)
    part(m,"Lamp",Vector3.new(0.9,0.7,0.9),CFrame.new(x,y+2.45,z),C.cyan,Enum.Material.Neon,Enum.PartType.Ball)
    local light=Instance.new("PointLight"); light.Color=C.cyan; light.Brightness=1.2; light.Range=12; light.Parent=m.Lamp
end
local function sample(position)
    local m = model("SampleCanister", position)
    local x,y,z=position.X,position.Y,position.Z
    part(m,"Canister",Vector3.new(0.9,1.5,0.9),CFrame.new(x,y+0.75,z),C.metal,Enum.Material.Metal,Enum.PartType.Cylinder)
    part(m,"Cap",Vector3.new(1,0.18,1),CFrame.new(x,y+1.55,z),C.amber,Enum.Material.Metal,Enum.PartType.Cylinder)
    part(m,"Core",Vector3.new(0.45,0.65,0.45),CFrame.new(x,y+0.8,z-0.47),C.teal,Enum.Material.Neon)
end
local function coral(position, seed)
    local m=model("KelpCoral_Cluster_"..seed,position)
    local rng=Random.new(seed)
    local x,y,z=position.X,position.Y,position.Z
    part(m,"BaseRock",Vector3.new(2.2,0.7,2),CFrame.new(x,y+0.35,z),C.rock,Enum.Material.Slate,Enum.PartType.Ball)
    for i=1,5 do
        local h=rng:NextNumber(1.1,2.6)
        local dx=rng:NextNumber(-0.8,0.8)
        local dz=rng:NextNumber(-0.7,0.7)
        local p=part(m,"Branch"..i,Vector3.new(rng:NextNumber(0.25,0.48),h,rng:NextNumber(0.25,0.48)),CFrame.new(x+dx,y+0.65+h/2,z+dz)*CFrame.Angles(math.rad(rng:NextNumber(-12,12)),0,math.rad(rng:NextNumber(-18,18))),i%2==0 and C.coral1 or C.coral2,Enum.Material.SmoothPlastic)
        p.Shape=Enum.PartType.Cylinder
    end
end

console(Vector3.new(0,0,0))
beacon(Vector3.new(8,0,0))
sample(Vector3.new(12,0,0))
coral(Vector3.new(18,0,0),21)
coral(Vector3.new(23,0,0),88)
print("Deep Lantern preview created. Inspect Workspace."..folderName.." in this TEST PLACE only.")
