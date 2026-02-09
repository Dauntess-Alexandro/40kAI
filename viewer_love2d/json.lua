-- json.lua (rxi/json.lua) - MIT License
-- Minimal JSON encode/decode for Love2D viewer.
-- Source: https://github.com/rxi/json.lua (embedded for convenience)

local json = { _version = "0.1.2" }

-----------------------------------------------------------------------------
-- Encode
-----------------------------------------------------------------------------

local encode

local escape_char_map = {
  ["\\"] = "\\\\",
  ["\""] = "\\\"",
  ["\b"] = "\\b",
  ["\f"] = "\\f",
  ["\n"] = "\\n",
  ["\r"] = "\\r",
  ["\t"] = "\\t"
}

local escape_char_map_inv = { ["\\/"] = "/" }
for k, v in pairs(escape_char_map) do
  escape_char_map_inv[v] = k
end

local function escape_char(c)
  return escape_char_map[c] or string.format("\\u%04x", c:byte())
end

local function encode_nil()
  return "null"
end

local function encode_table(val, stack)
  local res = {}
  stack = stack or {}

  if stack[val] then
    error("circular reference")
  end

  stack[val] = true

  if val[1] ~= nil or next(val) == nil then
    -- array
    for i, v in ipairs(val) do
      res[#res + 1] = encode(v, stack)
    end
    stack[val] = nil
    return "[" .. table.concat(res, ",") .. "]"
  else
    -- object
    for k, v in pairs(val) do
      if type(k) ~= "string" then
        error("invalid table: mixed or invalid key types")
      end
      res[#res + 1] = encode(k, stack) .. ":" .. encode(v, stack)
    end
    stack[val] = nil
    return "{" .. table.concat(res, ",") .. "}"
  end
end

local function encode_string(val)
  return '"' .. val:gsub('[%z\1-\31\\\"]', escape_char) .. '"'
end

local function encode_number(val)
  if val ~= val or val <= -math.huge or val >= math.huge then
    error("unexpected number value")
  end
  return string.format("%.14g", val)
end

encode = function(val, stack)
  local t = type(val)
  if t == "nil" then
    return encode_nil()
  elseif t == "table" then
    return encode_table(val, stack)
  elseif t == "string" then
    return encode_string(val)
  elseif t == "number" then
    return encode_number(val)
  elseif t == "boolean" then
    return tostring(val)
  else
    error("unexpected type: " .. t)
  end
end

function json.encode(val)
  return (encode(val))
end

-----------------------------------------------------------------------------
-- Decode
-----------------------------------------------------------------------------

local parse

local function create_set(...)
  local res = {}
  for i = 1, select("#", ...) do
    res[select(i, ...)] = true
  end
  return res
end

local space_chars = create_set(" ", "\t", "\r", "\n")
local delim_chars = create_set(" ", "\t", "\r", "\n", "]", "}", ",")
local escape_chars = create_set("\\", "/", '"', "b", "f", "n", "r", "t", "u")
local literals = create_set("true", "false", "null")

local literal_map = {
  ["true"] = true,
  ["false"] = false,
  ["null"] = nil
}

local function next_char(str, idx, set, negate)
  for i = idx, #str do
    if set[str:sub(i, i)] ~= negate then
      return i
    end
  end
  return #str + 1
end

local function decode_error(str, idx, msg)
  local line_count = 1
  local col_count = 1
  for i = 1, idx - 1 do
    col_count = col_count + 1
    if str:sub(i, i) == "\n" then
      line_count = line_count + 1
      col_count = 1
    end
  end
  error(string.format("%s at line %d col %d", msg, line_count, col_count))
end

local function codepoint_to_utf8(n)
  local f = math.floor
  if n <= 0x7f then
    return string.char(n)
  elseif n <= 0x7ff then
    return string.char(f(n / 64) + 192, n % 64 + 128)
  elseif n <= 0xffff then
    return string.char(f(n / 4096) + 224, f(n % 4096 / 64) + 128, n % 64 + 128)
  elseif n <= 0x10ffff then
    return string.char(f(n / 262144) + 240, f(n % 262144 / 4096) + 128,
      f(n % 4096 / 64) + 128, n % 64 + 128)
  end
  error(string.format("invalid unicode codepoint '%x'", n))
end

local function parse_unicode_escape(s)
  local n1 = tonumber(s:sub(1, 4), 16)
  local n2 = tonumber(s:sub(7, 10), 16)
  if n2 then
    return codepoint_to_utf8((n1 - 0xd800) * 0x400 + (n2 - 0xdc00) + 0x10000)
  else
    return codepoint_to_utf8(n1)
  end
end

local function parse_string(str, i)
  local res = ""
  local j = i + 1
  local k = j

  while j <= #str do
    local c = str:sub(j, j)
    if c == '"' then
      res = res .. str:sub(k, j - 1)
      return res, j + 1
    elseif c == "\\" then
      res = res .. str:sub(k, j - 1)
      j = j + 1
      local esc = str:sub(j, j)
      if esc == "u" then
        local hex = str:sub(j + 1, j + 4)
        local hex2 = str:sub(j + 5, j + 10)
        if not hex:match("%x%x%x%x") then
          decode_error(str, j, "invalid unicode escape in string")
        end
        if hex2:match("^\\u%x%x%x%x$") then
          res = res .. parse_unicode_escape(hex .. hex2)
          j = j + 10
        else
          res = res .. parse_unicode_escape(hex)
          j = j + 4
        end
      elseif escape_chars[esc] then
        res = res .. escape_char_map_inv["\\" .. esc]
      else
        decode_error(str, j, "invalid escape char '" .. esc .. "' in string")
      end
      k = j + 1
    end
    j = j + 1
  end

  decode_error(str, i, "expected closing quote for string")
end

local function parse_number(str, i)
  local x = next_char(str, i, delim_chars)
  local s = str:sub(i, x - 1)
  local n = tonumber(s)
  if not n then
    decode_error(str, i, "invalid number '" .. s .. "'")
  end
  return n, x
end

local function parse_literal(str, i)
  local x = next_char(str, i, delim_chars)
  local word = str:sub(i, x - 1)
  if not literals[word] then
    decode_error(str, i, "invalid literal '" .. word .. "'")
  end
  return literal_map[word], x
end

local function parse_array(str, i)
  local res = {}
  i = i + 1
  while true do
    i = next_char(str, i, space_chars, true)
    if str:sub(i, i) == "]" then
      i = i + 1
      break
    end
    local val
    val, i = parse(str, i)
    res[#res + 1] = val
    i = next_char(str, i, space_chars, true)
    local c = str:sub(i, i)
    if c == "]" then
      i = i + 1
      break
    end
    if c ~= "," then
      decode_error(str, i, "expected ']' or ','")
    end
    i = i + 1
  end
  return res, i
end

local function parse_object(str, i)
  local res = {}
  i = i + 1
  while true do
    i = next_char(str, i, space_chars, true)
    if str:sub(i, i) == "}" then
      i = i + 1
      break
    end
    if str:sub(i, i) ~= '"' then
      decode_error(str, i, "expected string for key")
    end
    local key
    key, i = parse_string(str, i)
    i = next_char(str, i, space_chars, true)
    if str:sub(i, i) ~= ":" then
      decode_error(str, i, "expected ':' after key")
    end
    i = next_char(str, i + 1, space_chars, true)
    local val
    val, i = parse(str, i)
    res[key] = val
    i = next_char(str, i, space_chars, true)
    local c = str:sub(i, i)
    if c == "}" then
      i = i + 1
      break
    end
    if c ~= "," then
      decode_error(str, i, "expected '}' or ','")
    end
    i = i + 1
  end
  return res, i
end

parse = function(str, idx)
  idx = next_char(str, idx, space_chars, true)
  local c = str:sub(idx, idx)
  if c == "{" then
    return parse_object(str, idx)
  elseif c == "[" then
    return parse_array(str, idx)
  elseif c == '"' then
    return parse_string(str, idx)
  elseif c == "-" or c:match("%d") then
    return parse_number(str, idx)
  else
    return parse_literal(str, idx)
  end
end

function json.decode(str)
  if type(str) ~= "string" then
    error("expected argument of type string")
  end
  local res, idx = parse(str, 1)
  idx = next_char(str, idx, space_chars, true)
  if idx <= #str then
    decode_error(str, idx, "trailing garbage")
  end
  return res
end

return json
