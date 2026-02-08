local rng = require("core.rng")
local state = require("core.state")

local reset = {}

function reset.apply(seed)
    local prng = rng.new(seed or 1)
    local grid_w = 5
    local grid_h = 5

    local units = {
        {id = 11, side = "model", x = 2, y = 2, hp = 10},
        {id = 21, side = "player", x = 4, y = 4, hp = 10},
    }

    local new_state = state.new({
        grid_w = grid_w,
        grid_h = grid_h,
        units = units,
        active_side = "model",
        phase = "movement",
        tick = 0,
        max_ticks = 50,
    })

    return new_state, prng
end

return reset
