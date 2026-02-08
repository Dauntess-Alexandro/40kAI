local rng = {}

function rng.new(seed)
    local self = {state = seed or 1}
    return setmetatable(self, {__index = rng})
end

function rng:seed(seed)
    self.state = seed or 1
end

function rng:next_u32()
    -- xorshift32
    local x = self.state & 0xFFFFFFFF
    x = x ~ (x << 13) & 0xFFFFFFFF
    x = x ~ (x >> 17) & 0xFFFFFFFF
    x = x ~ (x << 5) & 0xFFFFFFFF
    self.state = x
    return x
end

function rng:next_float()
    return self:next_u32() / 0xFFFFFFFF
end

return rng
