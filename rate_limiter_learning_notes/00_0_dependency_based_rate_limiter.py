from fastapi import Depends, FastAPI
from fastapi import Request, HTTPException
import redis
from redis import RedisError

LIMIT = 5
WINDOW = 60

async def rate_limiter(request: Request):
    ip = request.client.host
    key = f"rate:{ip}"


    try:
        count = await redis.incr(key)
    except RedisError:
        # fallback logic(in memory)
        allow_small_number_of_requests()


    if count == 1:
        await redis.expire(key, WINDOW)

    remaining = max(0, LIMIT - count)

    if count > LIMIT:
        retry_after = await redis.ttl(key)
        raise HTTPException(
            status_code=429,
            detail="Too Many Requests",
            headers={
                "Retry-After": str(retry_after),
                "X-RateLimit-Limit": str(LIMIT),
                "X-RateLimit-Remaining": "0"
            }
        )
    


app = FastAPI()

@app.get("/hello", dependencies=[Depends(rate_limiter)])
async def hello():
    return {"msg": "hello"}

