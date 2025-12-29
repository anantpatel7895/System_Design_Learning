# Latency vs Throughput — Why Latency Changes at Different Throughput Levels(when system is not scalable)

## 1. Core Idea (One Line)
Latency is **not constant**.  
As throughput (load) increases, latency remains stable initially and then **rises sharply after a saturation point**.

---

## 2. Why This Happens (Intuition)
Every system has finite capacity:
- CPU cores
- Database connections
- Thread pools
- Network bandwidth

when
```nginx
arrival_rate ≤ service_rate 
```
👉 requests are processed immediately

```nginx
arrival_rate > service_rate 
```
👉 requests queue up → latency increases

---

## 3. Phases of Latency vs Throughput

### Phase 1: Under-utilized System
- Low throughput
- No queue
- Stable, low latency

Example:
- Throughput: 100 RPS
- Latency: ~20 ms

---

### Phase 2: Near Capacity
- Throughput increases
- Queues begin forming
- Tail latency (P95/P99) rises

Example:
- Throughput: 900 RPS
- P50: 25 ms
- P99: 120 ms

---

### Phase 3: Saturation (Danger Zone)
- Throughput plateaus
- Queues grow rapidly
- Latency explodes
- Timeouts and retries occur

Example:
- Throughput: 1100 RPS
- P50: 60 ms
- P99: 3 seconds

---

## 4. The Latency–Throughput Curve (Knee Point)
A typical system shows:
- Flat latency at low load
- A **knee point** where latency starts rising
- Sharp latency spike beyond the knee

Good systems operate **before the knee point**.

---

## 5. Percentiles Matter More Than Averages
Average latency often hides problems.

| Metric | Behavior Under Load |
|------|---------------------|
| Average | Appears normal |
| P95 | Increases noticeably |
| P99 | Explodes |

Users experience **P95/P99 latency**, not averages.

---

## 6. Little’s Law (Interview Gold)
Little’s Law:

```ini
Latency = Queue Length / Throughput
```


Implications:
- Higher throughput → longer queues → higher latency
- Reducing queues directly reduces latency

---

## 7. Real System Example (API Server)

| Throughput (RPS) | P50 | P95 | P99 |
|------------------|-----|-----|-----|
| 200 | 20 ms | 30 ms | 40 ms |
| 800 | 25 ms | 80 ms | 200 ms |
| 1000 | 40 ms | 200 ms | 1.5 s |

Same system, **different latency at different throughput levels**.

---

## 8. Why Retries Make Things Worse
- Requests timeout
- Clients retry
- Retries increase load
- Increased load increases latency
- More latency causes more retries

This creates a **positive feedback loop (cascading failure)**.

---

## 9. How Good Systems Control Latency Under Load
Techniques used in production systems:
- Rate limiting
- Load shedding
- Backpressure
- Bounded queues
- Circuit breakers

Goal:
Keep the system operating **below saturation**.

---

## 10. Interview-Ready Summary Statement
**Latency is a function of throughput**.  
At low load, latency remains stable.  
As throughput approaches system capacity, queues form and latency—especially P99—rises sharply.  
Well-designed systems operate before the knee point of this curve.
