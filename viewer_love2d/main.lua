local json = require("json")

local ASSET_DIR = "assets"
local STATE_FILE = "viewer_state.json"
local STATE_POLL_SEC = 0.15

local assets = {
  ground = {},
  props = {},
  shadows = {},
  fx = {},
  decals = {},
  units = {}
}

local state = {
  camera = { x = 0, y = 0, zoom = 1.0 },
  ground = { tile = nil },
  units = {},
  props = {},
  fx = {},
  decals = {}
}

local lastStateError = nil
local pollTimer = 0
local firstGroundKey = nil

local function fileStem(name)
  return name:gsub("%.png$", "")
end

local function loadCategory(category)
  local dir = string.format("%s/%s", ASSET_DIR, category)
  if not love.filesystem.getInfo(dir, "directory") then
    return
  end

  for _, name in ipairs(love.filesystem.getDirectoryItems(dir)) do
    if name:match("%.png$") then
      local path = string.format("%s/%s", dir, name)
      local img = love.graphics.newImage(path)
      if category == "ground" then
        img:setWrap("repeat", "repeat")
      end
      assets[category][name] = img
      if category == "ground" and not firstGroundKey then
        firstGroundKey = name
      end
    end
  end
end

local function loadAssets()
  loadCategory("ground")
  loadCategory("props")
  loadCategory("shadows")
  loadCategory("fx")
  loadCategory("decals")
  loadCategory("units")
end

local function readStateFile()
  local data = love.filesystem.read(STATE_FILE)
  if not data then
    lastStateError = "Нет viewer_state.json рядом с main.lua"
    return
  end

  local ok, decoded = pcall(json.decode, data)
  if not ok then
    lastStateError = "Ошибка JSON: " .. tostring(decoded)
    return
  end

  state = decoded
  state.camera = state.camera or { x = 0, y = 0, zoom = 1.0 }
  state.ground = state.ground or { tile = nil }
  state.units = state.units or {}
  state.props = state.props or {}
  state.fx = state.fx or {}
  state.decals = state.decals or {}
  lastStateError = nil
end

local function getImage(category, name)
  if not name then
    return nil
  end
  return assets[category][name]
end

local function drawGround(camX, camY, zoom)
  local groundKey = state.ground and state.ground.tile or firstGroundKey
  local img = getImage("ground", groundKey)
  if not img then
    love.graphics.clear(0.18, 0.2, 0.18)
    return
  end

  local screenW, screenH = love.graphics.getDimensions()
  local tileW, tileH = img:getWidth(), img:getHeight()

  local worldLeft = camX - (screenW / 2) / zoom
  local worldTop = camY - (screenH / 2) / zoom

  local startX = worldLeft - (worldLeft % tileW) - tileW
  local startY = worldTop - (worldTop % tileH) - tileH

  local endX = camX + (screenW / 2) / zoom + tileW
  local endY = camY + (screenH / 2) / zoom + tileH

  for y = startY, endY, tileH do
    for x = startX, endX, tileW do
      love.graphics.draw(img, x, y)
    end
  end
end

local function drawDecals()
  for _, decal in ipairs(state.decals) do
    local img = getImage("decals", decal.type)
    if img then
      local rot = decal.rotation or 0
      local scale = decal.scale or 1
      love.graphics.draw(img, decal.x, decal.y, rot, scale, scale, img:getWidth() / 2, img:getHeight() / 2)
    end
  end
end

local function drawShadow(entry)
  if not entry.shadow then
    return
  end
  local shadow = getImage("shadows", entry.shadow)
  if not shadow then
    return
  end
  local offsetX = entry.shadowOffsetX or 8
  local offsetY = entry.shadowOffsetY or 8
  love.graphics.setColor(1, 1, 1, 0.9)
  love.graphics.draw(shadow, entry.x + offsetX, entry.y + offsetY, 0, 1, 1, shadow:getWidth() / 2, shadow:getHeight() / 2)
  love.graphics.setColor(1, 1, 1, 1)
end

local function drawProps()
  for _, prop in ipairs(state.props) do
    drawShadow(prop)
    local img = getImage("props", prop.sprite)
    if img then
      love.graphics.draw(img, prop.x, prop.y, prop.rotation or 0, prop.scale or 1, prop.scale or 1, img:getWidth() / 2, img:getHeight() / 2)
    end
  end
end

local function drawUnits()
  for _, unit in ipairs(state.units) do
    drawShadow(unit)
    local img = getImage("units", unit.sprite)
    if img then
      local rot = (unit.dir or 0) * math.pi / 180
      love.graphics.draw(img, unit.x, unit.y, rot, unit.scale or 1, unit.scale or 1, img:getWidth() / 2, img:getHeight() / 2)
    end
  end
end

local function drawFx()
  for _, fx in ipairs(state.fx) do
    local img = getImage("fx", fx.type)
    if img then
      love.graphics.draw(img, fx.x, fx.y, fx.rotation or 0, fx.scale or 1, fx.scale or 1, img:getWidth() / 2, img:getHeight() / 2)
    end
  end
end

function love.load()
  love.graphics.setBackgroundColor(0.12, 0.12, 0.12)
  loadAssets()
  readStateFile()
end

function love.update(dt)
  pollTimer = pollTimer + dt
  if pollTimer >= STATE_POLL_SEC then
    pollTimer = 0
    readStateFile()
  end
end

function love.draw()
  local cam = state.camera or { x = 0, y = 0, zoom = 1.0 }
  local zoom = cam.zoom or 1.0

  local screenW, screenH = love.graphics.getDimensions()
  love.graphics.push()
  love.graphics.translate(screenW / 2, screenH / 2)
  love.graphics.scale(zoom, zoom)
  love.graphics.translate(-cam.x, -cam.y)

  drawGround(cam.x, cam.y, zoom)
  drawDecals()
  drawProps()
  drawUnits()
  drawFx()

  love.graphics.pop()

  love.graphics.setColor(1, 1, 1, 1)
  love.graphics.print("Love2D viewer | FPS: " .. tostring(love.timer.getFPS()), 12, 10)
  if lastStateError then
    love.graphics.setColor(1, 0.4, 0.4, 1)
    love.graphics.print(lastStateError, 12, 30)
  end
  love.graphics.setColor(1, 1, 1, 1)
end
