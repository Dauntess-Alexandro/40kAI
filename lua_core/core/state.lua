local state = {}

function state.new(params)
    return {
        grid_w = params.grid_w,
        grid_h = params.grid_h,
        units = params.units,
        active_side = params.active_side,
        phase = params.phase,
        tick = params.tick,
        max_ticks = params.max_ticks or 50,
    }
end

function state.clone(src)
    local units_copy = {}
    for i, unit in ipairs(src.units) do
        units_copy[i] = {
            id = unit.id,
            side = unit.side,
            x = unit.x,
            y = unit.y,
            hp = unit.hp,
        }
    end
    return {
        grid_w = src.grid_w,
        grid_h = src.grid_h,
        units = units_copy,
        active_side = src.active_side,
        phase = src.phase,
        tick = src.tick,
        max_ticks = src.max_ticks,
    }
end

function state.to_obs(src)
    local units_obs = {}
    for i, unit in ipairs(src.units) do
        units_obs[i] = {
            id = unit.id,
            side = unit.side,
            x = unit.x,
            y = unit.y,
            hp = unit.hp,
        }
    end
    return {
        tick = src.tick,
        active_side = src.active_side,
        phase = src.phase,
        units = units_obs,
    }
end

return state
