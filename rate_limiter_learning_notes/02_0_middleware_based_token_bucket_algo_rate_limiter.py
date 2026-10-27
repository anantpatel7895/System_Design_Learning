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


class TokenBucketRateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # ✅ Skip health check
        if request.url.path == "/health":
            return await call_next(request)

        ip = request.client.host
        tokens_key = f"rate:{ip}:tokens"
        timestamp_key = f"rate:{ip}:last_refill"

        now = time.time()

        try:
            # 1️⃣ Read current state
            tokens = await redis_client.get(tokens_key) # Redis GET returns a string or None,
            last_refill = await redis_client.get(timestamp_key)

            if tokens is None or last_refill is None:
                # First request
                tokens = MAX_TOKENS
                last_refill = now
            else:
                tokens = float(tokens)
                last_refill = float(last_refill)

            # 2️⃣ Refill tokens
            elapsed = now - last_refill
            refill = elapsed * REFILL_RATE
            tokens = min(MAX_TOKENS, tokens + refill)

            # 3️⃣ Check availability
            if tokens < 1:
                retry_after = int((1 - tokens) / REFILL_RATE)
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too Many Requests"},
                    headers={"Retry-After": str(retry_after)},
                )

            # 4️⃣ Consume token
            tokens -= 1

            # 5️⃣ Save state
            await redis_client.set(tokens_key, tokens)
            await redis_client.set(timestamp_key, now)

        except Exception:
            # Redis down → allow request (graceful degradation)
            pass

        return await call_next(request)


from fastapi import FastAPI

app = FastAPI()
app.add_middleware(TokenBucketRateLimitMiddleware)



@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/hello")
async def hello():
    return {"msg": "hello"}

