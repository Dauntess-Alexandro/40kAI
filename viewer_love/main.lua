local json = require("json")

-- Controls:
-- LMB drag = pan
-- Wheel = zoom
-- R = reset view (center 0,0; zoom=1)
-- F = fit to units (center on bbox + zoom to fit)

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
local did_initial_fit = false

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

local function to_world(px, py)
  local wx = (px / camera.zoom - camera.x) / cell_size
  local wy = (py / camera.zoom - camera.y) / cell_size
  return wx, wy
end

local function draw_grid()
  local w = love.graphics.getWidth()
  local h = love.graphics.getHeight()
  local wx0, wy0 = to_world(0, 0)
  local wx1, wy1 = to_world(w, h)
  local min_x = math.floor(math.min(wx0, wx1))
  local max_x = math.ceil(math.max(wx0, wx1))
  local min_y = math.floor(math.min(wy0, wy1))
  local max_y = math.ceil(math.max(wy0, wy1))

  love.graphics.setColor(0.2, 0.2, 0.2, 1)
  for x = min_x, max_x do
    local sx1, sy1 = to_screen(x, min_y)
    local sx2, sy2 = to_screen(x, max_y)
    love.graphics.line(sx1, sy1, sx2, sy2)
  end
  for y = min_y, max_y do
    local sx1, sy1 = to_screen(min_x, y)
    local sx2, sy2 = to_screen(max_x, y)
    love.graphics.line(sx1, sy1, sx2, sy2)
  end
end

local function set_camera_center(cx, cy)
  local w = love.graphics.getWidth()
  local h = love.graphics.getHeight()
  camera.x = w / 2 / camera.zoom - cx * cell_size
  camera.y = h / 2 / camera.zoom - cy * cell_size
end

local function reset_view()
  camera.zoom = 1
  camera.x = 0
  camera.y = 0
end

local function fit_to_units()
  if not snapshot or not snapshot.units or #snapshot.units == 0 then
    return
  end
  local min_x, max_x = nil, nil
  local min_y, max_y = nil, nil
  for _, unit in ipairs(snapshot.units) do
    if unit.x ~= nil and unit.y ~= nil then
      min_x = min_x and math.min(min_x, unit.x) or unit.x
      max_x = max_x and math.max(max_x, unit.x) or unit.x
      min_y = min_y and math.min(min_y, unit.y) or unit.y
      max_y = max_y and math.max(max_y, unit.y) or unit.y
    end
  end
  if not min_x or not min_y then
    return
  end

  local w = love.graphics.getWidth()
  local h = love.graphics.getHeight()
  local padding_cells = 3
  local span_x = math.max(1, (max_x - min_x) + padding_cells * 2)
  local span_y = math.max(1, (max_y - min_y) + padding_cells * 2)
  local zoom_x = w / (span_x * cell_size)
  local zoom_y = h / (span_y * cell_size)
  camera.zoom = clamp(math.min(zoom_x, zoom_y), 0.2, 4)

  local center_x = (min_x + max_x) / 2
  local center_y = (min_y + max_y) / 2
  set_camera_center(center_x, center_y)
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

  if snapshot and not did_initial_fit then
    fit_to_units()
    did_initial_fit = true
  end
end

function love.draw()
  love.graphics.clear(0.08, 0.08, 0.1, 1)

  draw_grid()

  local units_count = 0
  local min_x, max_x = nil, nil
  local min_y, max_y = nil, nil
  if snapshot and snapshot.units then
    for _, unit in ipairs(snapshot.units) do
      if unit.x ~= nil and unit.y ~= nil then
        units_count = units_count + 1
        min_x = min_x and math.min(min_x, unit.x) or unit.x
        max_x = max_x and math.max(max_x, unit.x) or unit.x
        min_y = min_y and math.min(min_y, unit.y) or unit.y
        max_y = max_y and math.max(max_y, unit.y) or unit.y
      end
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
      love.graphics.setColor(1, 1, 1, 0.9)
      love.graphics.print(tostring(unit.id or "?"), sx + radius + 2, sy - radius - 2)
    end
  end

  love.graphics.setColor(1, 1, 1, 1)
  local status = string.format(
    "NO SNAPSHOT. Waiting... path=%s",
    snapshot_path
  )
  if snapshot then
    local cam_cx, cam_cy = to_world(love.graphics.getWidth() / 2, love.graphics.getHeight() / 2)
    status = string.format(
      "tick=%s | active=%s | phase=%s | cam=(%.2f,%.2f) zoom=%.2f | units=%d | min=(%s,%s) max=(%s,%s)",
      tostring(snapshot.tick or "-"),
      tostring(snapshot.active_side or "-"),
      tostring(snapshot.phase or "-"),
      cam_cx,
      cam_cy,
      camera.zoom,
      units_count,
      min_x and tostring(min_x) or "-",
      min_y and tostring(min_y) or "-",
      max_x and tostring(max_x) or "-",
      max_y and tostring(max_y) or "-"
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

function love.keypressed(key)
  if key == "r" then
    reset_view()
  elseif key == "f" then
    fit_to_units()
  end
end
