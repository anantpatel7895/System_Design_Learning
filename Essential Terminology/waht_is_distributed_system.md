# What “distributed” really means (beginner definition)

A system is distributed if:
> Multiple independent processes coordinate using a networked shared system.

## ❌ It does NOT mean:
- Must be on different machines
- Must be in different data centers

## ✔ It DOES mean:
- No shared memory
- Communicate over network
- Can fail independently
- Can scale independently

# Same server ≠ same process

| Scenario                          | Distributed? |
| --------------------------------- | ------------ |
| 3 threads in one Python process   | ❌ No         |
| 3 FastAPI containers on same host | ✅ Yes        |
| 3 pods in Kubernetes              | ✅ Yes        |
| 3 EC2 instances                   | ✅ Yes        |
| 3 uvicorn worker in container     | ✅ Yes  (uvicorn app.main:app --workers 4)      |
