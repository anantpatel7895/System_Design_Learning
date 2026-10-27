from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

import redis.asyncio as redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


LIMIT = 5
WINDOW = 60  # seconds


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # ✅ 1. Skip health checks
        if request.url.path == "/health":
            return await call_next(request)

        # ✅ 2. Identify client (IP based)
        client_ip = request.client.host
        key = f"rate:{client_ip}"

        try:
            # ✅ 3. Increment request count
            count = await redis_client.incr(key)

            # ✅ 4. Set TTL only once (VERY IMPORTANT)
            if count == 1:
                await redis_client.expire(key, WINDOW)

            # ✅ 5. Block if limit exceeded
            if count > LIMIT:
                retry_after = await redis_client.ttl(key)

                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too Many Requests"},
                    headers={
                        "Retry-After": str(retry_after),
                        "X-RateLimit-Limit": str(LIMIT),
                        "X-RateLimit-Remaining": "0",
                    },
                )

        except Exception:
            # ✅ 6. Redis down → allow limited access (graceful degradation)
            # Simple fallback: allow request
            pass

        # ✅ 7. Continue request
        response = await call_next(request)
        return response


from fastapi import FastAPI

app = FastAPI()
app.add_middleware(RateLimitMiddleware)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/hello")
async def hello():
    return {"msg": "hello"}
