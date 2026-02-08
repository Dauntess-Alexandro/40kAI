local script_path = debug.getinfo(1, "S").source:sub(2)
local script_dir = script_path:match("(.*/)") or "./"
package.path = package.path .. ";" .. script_dir .. "../lua_core/?.lua;" .. script_dir .. "../lua_core/core/?.lua"

local socket = require("socket")
local json = require("core.json")
local reset = require("core.reset")
local step = require("core.step")
local state_module = require("core.state")

local host = {}

local debug_enabled = os.getenv("HOST_DEBUG") == "1"
local function log(message)
    if debug_enabled then
        io.stdout:write("[HOST] " .. message .. "\n")
        io.stdout:flush()
    end
end

local function send_line(client, payload)
    client:send(json.encode(payload) .. "\n")
end

local function handle_request(request, context, client)
    if request.cmd == "reset" then
        local seed = request.seed or 1
        local new_state, prng = reset.apply(seed)
        context.state = new_state
        context.prng = prng
        send_line(client, {
            ok = true,
            obs = state_module.to_obs(context.state),
            info = {seed = seed},
        })
        return true
    elseif request.cmd == "step" then
        if not context.state then
            send_line(client, {ok = false, error = "state_not_initialized"})
            return true
        end
        local new_state, reward, done, info, events = step.apply(context.state, request.action or {})
        context.state = new_state
        send_line(client, {
            ok = true,
            obs = state_module.to_obs(context.state),
            reward = reward,
            done = done,
            info = info,
            events = events,
        })
        return true
    elseif request.cmd == "close" then
        send_line(client, {ok = true})
        return false
    end

    send_line(client, {ok = false, error = "unknown_command"})
    return true
end

function host.run()
    local port = tonumber(os.getenv("HOST_PORT")) or 8765
    local server = assert(socket.bind("127.0.0.1", port))
    log("listening on 127.0.0.1:" .. port)

    local client = server:accept()
    client:settimeout(0.1)
    log("client connected")

    local context = {state = nil, prng = nil}
    local running = true

    while running do
        local line, err = client:receive("*l")
        if line then
            log("recv: " .. line)
            local ok, decoded = pcall(json.decode, line)
            if not ok then
                send_line(client, {ok = false, error = "invalid_json"})
            else
                local ok_cmd, keep_running = pcall(handle_request, decoded, context, client)
                if not ok_cmd then
                    send_line(client, {ok = false, error = "internal_error"})
                else
                    running = keep_running
                end
            end
        elseif err == "timeout" then
            -- keep waiting
        else
            log("client disconnected")
            running = false
        end
    end

    client:close()
    server:close()
    log("shutdown")
end

host.run()
