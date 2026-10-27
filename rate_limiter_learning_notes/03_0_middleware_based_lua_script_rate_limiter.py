import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

MAX_TOKENS = 5
REFILL_RATE = 1 / 12  # tokens per second


LUA_SCRIPT = """
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
"""


class TokenBucketMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if request.url.path == "/health":
            return await call_next(request)

        ip = request.client.host
        tokens_key = f"rate:{ip}:tokens"
        time_key = f"rate:{ip}:time"

        now = time.time()

        try:
            allowed, remaining = await redis_client.eval(
                LUA_SCRIPT,
                keys=[tokens_key, time_key],
                args=[MAX_TOKENS, REFILL_RATE, now],
            )

            remaining = int(remaining)

            if not allowed:
                retry_after = int((1 - remaining) / REFILL_RATE)

                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too Many Requests"},
                    headers={
                        "Retry-After": str(retry_after),
                        "X-RateLimit-Limit": str(MAX_TOKENS),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(now + retry_after)),
                    },
                )

        except Exception:
            # Redis down → allow request (graceful degradation)
            return await call_next(request)

        response = await call_next(request)

        # ✅ success headers
        response.headers["X-RateLimit-Limit"] = str(MAX_TOKENS)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response


from fastapi import FastAPI

app = FastAPI()
app.add_middleware(TokenBucketMiddleware)



@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/hello")
async def hello():
    return {"msg": "hello"}