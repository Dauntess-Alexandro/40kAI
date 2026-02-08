local json = {}

local function is_array(tbl)
    local max_index = 0
    for k, _ in pairs(tbl) do
        if type(k) ~= "number" then
            return false
        end
        if k > max_index then
            max_index = k
        end
    end
    for i = 1, max_index do
        if tbl[i] == nil then
            return false
        end
    end
    return true
end

local function escape_str(value)
    local replacements = {
        ["\\"] = "\\\\",
        ["\""] = "\\\"",
        ["\b"] = "\\b",
        ["\f"] = "\\f",
        ["\n"] = "\\n",
        ["\r"] = "\\r",
        ["\t"] = "\\t",
    }
    return value:gsub("[\\\"\b\f\n\r\t]", replacements)
end

function json.encode(value)
    local value_type = type(value)
    if value_type == "nil" then
        return "null"
    elseif value_type == "number" then
        return tostring(value)
    elseif value_type == "boolean" then
        return value and "true" or "false"
    elseif value_type == "string" then
        return '"' .. escape_str(value) .. '"'
    elseif value_type == "table" then
        if is_array(value) then
            local items = {}
            for i = 1, #value do
                items[i] = json.encode(value[i])
            end
            return "[" .. table.concat(items, ",") .. "]"
        end
        local items = {}
        for k, v in pairs(value) do
            table.insert(items, json.encode(tostring(k)) .. ":" .. json.encode(v))
        end
        return "{" .. table.concat(items, ",") .. "}"
    end
    error("unsupported json type: " .. value_type)
end

function json.decode(text)
    local pos = 1

    local function skip_ws()
        while true do
            local c = text:sub(pos, pos)
            if c == " " or c == "\n" or c == "\r" or c == "\t" then
                pos = pos + 1
            else
                break
            end
        end
    end

    local function parse_string()
        pos = pos + 1
        local result = {}
        while true do
            local c = text:sub(pos, pos)
            if c == "" then
                error("unterminated string")
            end
            if c == "\"" then
                pos = pos + 1
                break
            end
            if c == "\\" then
                local esc = text:sub(pos + 1, pos + 1)
                if esc == "\"" or esc == "\\" or esc == "/" then
                    table.insert(result, esc)
                    pos = pos + 2
                elseif esc == "b" then
                    table.insert(result, "\b")
                    pos = pos + 2
                elseif esc == "f" then
                    table.insert(result, "\f")
                    pos = pos + 2
                elseif esc == "n" then
                    table.insert(result, "\n")
                    pos = pos + 2
                elseif esc == "r" then
                    table.insert(result, "\r")
                    pos = pos + 2
                elseif esc == "t" then
                    table.insert(result, "\t")
                    pos = pos + 2
                else
                    error("invalid escape")
                end
            else
                table.insert(result, c)
                pos = pos + 1
            end
        end
        return table.concat(result)
    end

    local function parse_number()
        local start_pos = pos
        while text:sub(pos, pos):match("[%d%+%-%e%E%\.]") do
            pos = pos + 1
        end
        local number_str = text:sub(start_pos, pos - 1)
        local number_val = tonumber(number_str)
        if not number_val then
            error("invalid number")
        end
        return number_val
    end

    local function parse_value()
        skip_ws()
        local c = text:sub(pos, pos)
        if c == "{" then
            pos = pos + 1
            local obj = {}
            skip_ws()
            if text:sub(pos, pos) == "}" then
                pos = pos + 1
                return obj
            end
            while true do
                skip_ws()
                local key = parse_string()
                skip_ws()
                if text:sub(pos, pos) ~= ":" then
                    error("expected :")
                end
                pos = pos + 1
                obj[key] = parse_value()
                skip_ws()
                local next_char = text:sub(pos, pos)
                if next_char == "}" then
                    pos = pos + 1
                    break
                end
                if next_char ~= "," then
                    error("expected ,")
                end
                pos = pos + 1
            end
            return obj
        elseif c == "[" then
            pos = pos + 1
            local arr = {}
            skip_ws()
            if text:sub(pos, pos) == "]" then
                pos = pos + 1
                return arr
            end
            while true do
                table.insert(arr, parse_value())
                skip_ws()
                local next_char = text:sub(pos, pos)
                if next_char == "]" then
                    pos = pos + 1
                    break
                end
                if next_char ~= "," then
                    error("expected ,")
                end
                pos = pos + 1
            end
            return arr
        elseif c == '"' then
            return parse_string()
        elseif c == "t" and text:sub(pos, pos + 3) == "true" then
            pos = pos + 4
            return true
        elseif c == "f" and text:sub(pos, pos + 4) == "false" then
            pos = pos + 5
            return false
        elseif c == "n" and text:sub(pos, pos + 3) == "null" then
            pos = pos + 4
            return nil
        else
            return parse_number()
        end
    end

    local value = parse_value()
    skip_ws()
    return value
end

return json
