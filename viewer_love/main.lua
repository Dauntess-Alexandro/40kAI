local json = require("json")

local snapshot_path = "../viewer_out/snapshot.json"
local events_path = "../viewer_out/events.jsonl"

local snapshot = nil
local event_queue = {}
local event_offset = 0
local poll_timer = 0
local poll_interval = 0.05

local cell_size = 32
local camera = { x = 0, y = 0, zoom = 1 }
local dragging = false
local drag_start = { x = 0, y = 0 }
local camera_start = { x = 0, y = 0 }

local move_anims = {}

local function clamp(value, min_value, max_value)
  if value < min_value then
    return min_value
  end
  if value > max_value then
    return max_value
  end
  return value
end

local function lerp(a, b, t)
  return a + (b - a) * t
end

local function read_snapshot()
  local file = io.open(snapshot_path, "r")
  if not file then
    return
  end
  local content = file:read("*a")
  file:close()
  if not content or content == "" then
    return
  end
  local ok, data = pcall(json.decode, content)
  if ok and data then
    snapshot = data
  end
end

local function read_events()
  local file = io.open(events_path, "r")
  if not file then
    return
  end
  file:seek("set", event_offset)
  for line in file:lines() do
    if line ~= "" then
      local ok, data = pcall(json.decode, line)
      if ok and data then
        table.insert(event_queue, data)
      end
    end
  end
  event_offset = file:seek()
  file:close()
end

local function start_move_animation(event)
  local unit_id = tostring(event.unit_id)
  local duration = (event.duration_ms or 250) / 1000
  move_anims[unit_id] = {
    from = event.from or { 0, 0 },
    to = event.to or { 0, 0 },
    t = 0,
    duration = math.max(duration, 0.05),
  }
end

local function process_events()
  if #event_queue == 0 then
    return
  end
  for _, event in ipairs(event_queue) do
    if event.type == "move" then
      start_move_animation(event)
    end
  end
  event_queue = {}
end

local function get_unit_position(unit)
  if not unit then
    return nil
  end
  local unit_id = tostring(unit.id or "")
  local anim = move_anims[unit_id]
  if anim then
    local t = clamp(anim.t / anim.duration, 0, 1)
    local x = lerp(anim.from[1] or 0, anim.to[1] or 0, t)
    local y = lerp(anim.from[2] or 0, anim.to[2] or 0, t)
    return x, y
  end
  return unit.x or 0, unit.y or 0
end

local function to_screen(wx, wy)
  local px = (wx * cell_size + camera.x) * camera.zoom
  local py = (wy * cell_size + camera.y) * camera.zoom
  return px, py
end

local function draw_grid(max_x, max_y)
  love.graphics.setColor(0.2, 0.2, 0.2, 1)
  for x = 0, max_x do
    local sx1, sy1 = to_screen(x, 0)
    local sx2, sy2 = to_screen(x, max_y)
    love.graphics.line(sx1, sy1, sx2, sy2)
  end
  for y = 0, max_y do
    local sx1, sy1 = to_screen(0, y)
    local sx2, sy2 = to_screen(max_x, y)
    love.graphics.line(sx1, sy1, sx2, sy2)
  end
end

function love.load()
  love.window.setTitle("40kAI Viewer (LÖVE2D)")
end

function love.update(dt)
  poll_timer = poll_timer + dt
  if poll_timer >= poll_interval then
    poll_timer = poll_timer - poll_interval
    read_snapshot()
    read_events()
  end

  for unit_id, anim in pairs(move_anims) do
    anim.t = anim.t + dt
    if anim.t >= anim.duration then
      move_anims[unit_id] = nil
    end
  end

  process_events()
end

function love.draw()
  love.graphics.clear(0.08, 0.08, 0.1, 1)

  local max_x = 20
  local max_y = 20
  if snapshot and snapshot.units then
    for _, unit in ipairs(snapshot.units) do
      local ux = unit.x or 0
      local uy = unit.y or 0
      if ux > max_x then
        max_x = ux
      end
      if uy > max_y then
        max_y = uy
      end
    end
  end
  max_x = max_x + 5
  max_y = max_y + 5

  draw_grid(max_x, max_y)

  if snapshot and snapshot.units then
    for _, unit in ipairs(snapshot.units) do
      local ux, uy = get_unit_position(unit)
      local sx, sy = to_screen(ux + 0.5, uy + 0.5)
      local radius = (cell_size * 0.35) * camera.zoom
      if unit.side == "player" then
        love.graphics.setColor(0.2, 0.6, 1.0, 1)
      else
        love.graphics.setColor(1.0, 0.3, 0.3, 1)
      end
      love.graphics.circle("fill", sx, sy, radius)
      love.graphics.setColor(0, 0, 0, 0.6)
      love.graphics.circle("line", sx, sy, radius)
    end
  end

  love.graphics.setColor(1, 1, 1, 1)
  local status = "Ожидание данных..."
  if snapshot then
    status = string.format(
      "tick=%s | active=%s | phase=%s",
      tostring(snapshot.tick or "—"),
      tostring(snapshot.active_side or "—"),
      tostring(snapshot.phase or "—")
    )
  end
  love.graphics.print(status, 12, 12)
end

function love.mousepressed(x, y, button)
  if button == 1 then
    dragging = true
    drag_start.x = x
    drag_start.y = y
    camera_start.x = camera.x
    camera_start.y = camera.y
  end
end

function love.mousemoved(x, y, dx, dy)
  if dragging then
    camera.x = camera_start.x + (x - drag_start.x) / camera.zoom
    camera.y = camera_start.y + (y - drag_start.y) / camera.zoom
  end
end

function love.mousereleased(_, _, button)
  if button == 1 then
    dragging = false
  end
end

function love.wheelmoved(_, y)
  if y == 0 then
    return
  end
  local zoom = camera.zoom * (1 + y * 0.1)
  camera.zoom = clamp(zoom, 0.2, 4)
end
