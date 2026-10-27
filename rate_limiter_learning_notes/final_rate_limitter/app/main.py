from fastapi import FastAPI
from app.middleware.rate_limiter import RateLimitMiddleware
from app.api.routes import router

app = FastAPI()

app.add_middleware(RateLimitMiddleware)
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok"}
