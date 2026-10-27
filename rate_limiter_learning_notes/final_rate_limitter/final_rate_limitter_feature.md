# Goal: Production-ready Distributed Rate Limiter (FastAPI)

- ✅ Distributed (multi-instance safe)
- ✅ Redis-backed
- ✅ Token Bucket (atomic via Lua)
- ✅ API-key based
- ✅ Plan-based limits (FREE / PAID)
- ✅ Middleware
- ✅ Proper headers
- ✅ Ready for Kubernetes / autoscaling

## Step 1 — High-level architecture (mental model)
```java
Client
  |
  |  HTTP (X-API-Key)
  v
FastAPI (multiple instances)
  |
  |  Redis Lua (atomic)
  v
Redis (shared state)
```

Key idea
> FastAPI instances are stateless
> Redis holds all rate-limit state

This is what makes it **distributed**.

## Step 2 — Project folder structure (IMPORTANT)
```text
rate_limiter_service/
│
├── app/
│   ├── main.py                  # FastAPI entrypoint
│   │
│   ├── core/
│   │   ├── config.py             # settings (limits, env)
│   │   ├── redis.py              # redis client
│   │   └── plans.py              # FREE / PAID plans
│   │
│   ├── middleware/
│   │   └── rate_limiter.py       # token bucket middleware
│   │
│   ├── lua/
│   │   └── token_bucket.lua      # atomic redis logic
│   │
│   ├── api/
│   │   └── routes.py             # example APIs
│   │
│   └── utils/
│       └── security.py           # api-key helpers
│
├── docker/
│   └── Dockerfile
│
├── docker-compose.yml            # FastAPI + Redis
├── requirements.txt
└── README.md
```

## Build & Run (test locally)
```bash
docker build -t rate-limiter .
docker run -p 8000:8000 rate-limiter
```

with redis (recommended)
```bash
docker-compose up --build
```