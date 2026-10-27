local tokens = tonumber(redis.call("GET", KEYS[1]))
local last_time = tonumber(redis.call("GET", KEYS[2]))

if tokens == nil then
    tokens = tonumber(ARGV[1])
    last_time = tonumber(ARGV[3])
end

local elapsed = tonumber(ARGV[3]) - last_time
local refill = elapsed * tonumber(ARGV[2])
tokens = math.min(tonumber(ARGV[1]), tokens + refill)

local allowed = 0
if tokens >= 1 then
    allowed = 1
    tokens = tokens - 1
end

redis.call("SET", KEYS[1], tokens)
redis.call("SET", KEYS[2], ARGV[3])

return {allowed, tokens}
