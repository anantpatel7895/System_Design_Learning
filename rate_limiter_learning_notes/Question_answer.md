# Rate Limiting – Beginner to Production Notes (FastAPI)

## 1. What is Rate Limiting?
Rate limiting restricts how frequently a client can call an API.
It protects the server from abuse and ensures fair usage.

---

## 2. Why Python Memory is Not Enough
- Python `dict` is local to one process
- Multiple servers/workers do not share memory
- App restart clears all data

➡️ Not production safe

---

## 3. Why Redis is Used
Redis provides:
- Shared state across servers
- Atomic counters (`INCR`)
- Automatic expiration (`TTL`)
- High performance

---

## 4. Fixed Window Rate Limiting
Rule:
> X requests per Y seconds per User


Implementation idea:
- Increment counter
- Set TTL only when key is created
- Block when limit exceeded

⚠️ Problem:
- Allows burst at window boundaries

---

## 5. Why TTL(time to live) is Set Only Once
- TTL defines the time window
- Resetting TTL every request causes permanent blocking
- TTL must finish naturally

Rule:
> TTL starts once, window ends once

### EXAMPLE
```python
count = await redis.incr(key)
"""
if key does not exist (otherwise increment it)
↓
Redis creates key = 0
↓
Redis increments to 1
↓
returns 1

"""

if count == 1:
    await redis.expire(key, 60)
```

---

## 6. HTTP 429 & Headers
- HTTP `429 Too Many Requests` is returned when limit breaks
- Important headers:
  - `Retry-After`
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`

`Retry-After` tells the client how long to wait before retrying.

---

## 7. Redis Failure Strategy
When Redis is down:
- Do NOT block everything
- Do NOT allow everything

Best approach:
> Allow some requests to balance availability and safety

---

## 8. Middleware vs Dependency
- Dependency → per-endpoint
- Middleware → global
- Production systems prefer middleware

Health check endpoints should be excluded.

---

## 9. Token Bucket Algorithm (Production Standard)
Concept:
- Bucket holds tokens
- Tokens refill over time
- Each request consumes a token

Benefits:
- Prevents frequent continuous usage
- Allows small bursts
- Smooth traffic
- Industry standard (AWS, Stripe, GitHub)

---

## 10. Key Takeaway
> Token Bucket provides fair, scalable, and production-ready rate limiting.


## 11. Why do we need Redis Lua for Token Bucket?
We use Redis Lua to make the token bucket logic atomic so multiple concurrent requests cannot break the rate limit.
> Concurrency needs atomicity. Redis Lua provides atomicity.


