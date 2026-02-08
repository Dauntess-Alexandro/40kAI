local state_module = require("core.state")

local step = {}

local dir_delta = {
    up = {0, -1},
    down = {0, 1},
    left = {-1, 0},
    right = {1, 0},
    stay = {0, 0},
}

local function find_unit(units, unit_id)
    for _, unit in ipairs(units) do
        if unit.id == unit_id then
            return unit
        end
    end
    return nil
end

function step.apply(src_state, action)
    local new_state = state_module.clone(src_state)
    local events = {}
    local info = {}

    local unit_id = action and action.unit_id or nil
    local dir = action and action.dir or "stay"

    local unit = unit_id and find_unit(new_state.units, unit_id) or nil
    if not unit then
        info.error = "unit_not_found"
    else
        local delta = dir_delta[dir] or dir_delta.stay
        local new_x = unit.x + delta[1]
        local new_y = unit.y + delta[2]
        if new_x < 0 or new_x >= new_state.grid_w or new_y < 0 or new_y >= new_state.grid_h then
            info.invalid_move = true
        else
            if new_x ~= unit.x or new_y ~= unit.y then
                table.insert(events, {
                    type = "move",
                    unit_id = unit.id,
                    from = {unit.x, unit.y},
                    to = {new_x, new_y},
                })
            end
            unit.x = new_x
            unit.y = new_y
        end
    end

    new_state.tick = new_state.tick + 1

    local reward = 0
    local done = new_state.tick >= new_state.max_ticks

    return new_state, reward, done, info, events
end

return step
