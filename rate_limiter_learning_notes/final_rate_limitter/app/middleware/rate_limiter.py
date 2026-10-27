import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.redis import redis_client
from app.core.plans import API_KEY_PLANS, PLANS

from pathlib import Path

LUA_SCRIPT = Path("app/lua/token_bucket.lua").read_text()

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if request.url.path == "/health":
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return JSONResponse(401, {"detail": "API key required"})

        plan_name = API_KEY_PLANS.get(api_key)
        if not plan_name:
            return JSONResponse(403, {"detail": "Invalid API key"})

        plan = PLANS[plan_name]

        tokens_key = f"rate:{api_key}:tokens"
        time_key = f"rate:{api_key}:time"
        now = time.time()

        try:
            allowed, remaining = await redis_client.eval(
                LUA_SCRIPT,
                keys=[tokens_key, time_key],
                args=[
                    plan["max_tokens"],
                    plan["refill_rate"],
                    now,
                ],
            )

            remaining = int(remaining)

            if not allowed:
                retry_after = int((1 - remaining) / plan["refill_rate"])
                return JSONResponse(
                    429,
                    {"detail": "Too Many Requests"},
                    headers={
                        "Retry-After": str(retry_after),
                        "X-RateLimit-Limit": str(plan["max_tokens"]),
                        "X-RateLimit-Remaining": "0",
                    },
                )

        except Exception:
            # Redis down → fail open
            return await call_next(request)

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(plan["max_tokens"])
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
