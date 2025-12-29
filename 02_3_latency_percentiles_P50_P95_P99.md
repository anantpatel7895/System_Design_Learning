# Latency & Percentiles — Final Clarified Notes

These notes clarify how **latency**, **measurement windows**, and **percentiles (P50, P95, P99)** work together in real production systems.

---

## 1. What Latency Is

Latency is always calculated using **both start and end time**.
> Latency = end_time − start_time


There is **no latency metric without start and end time**.

---

## 2. What Percentiles Operate On

Percentiles do **not** operate on requests.  
Percentiles operate on **latency values**.

Process:
1. Measure latency for each request
2. Collect latency values
3. Sort latency values
4. Compute P50 / P95 / P99

---

## 3. What the Measurement Window Means

A measurement window is a fixed time range, for example:
- last 10 seconds
- last 1 minute
- last 5 minutes

**Only requests that complete within the window are included.**

Start time does **not** decide inclusion.

---

## 4. Inclusion Rule (Very Important)

> A request is included **if and only if it finishes inside the window**, regardless of when it started.

| Request | Start | End | Included |
|------|------|------|---------|
| R1 | 11:50 | 12:00:10 | Yes |
| R2 | 12:00:20 | 12:00:30 | Yes |
| R3 | 11:59 | 12:01:05 | No |

---

## 5. How Latency and Window Work Together

- **Start time** → used to compute latency
- **End time** → used to decide window inclusion

These are **two separate concerns**.

---

## 6. How Percentiles Are Calculated

Example latencies collected in a window:
> [10 ms, 20 ms, 25 ms, 40 ms, 2.5 s]


Sorted:
> [10 ms, 20 ms, 25 ms, 40 ms, 2.5 s]

```nginx
index of request = percentile * N
```
> where N is total number of request in that time frame

Percentiles:
- P50 → 25 ms (0.5 * 5 = 2.5 ~= 3)
- P95 → 2.5 s (0.95 * 5 = 4.75 ~= 5)
- P99 → 2.5 s (0.99 * 5 = 49.5 ~= 5)

---

## 7. Why Long-Running Requests Matter

If a request:
- starts long before the window
- finishes inside the window

Then:
- its **full latency** is counted
- it can dominate **P99**

This is intentional and correct.

---

## 8. Why Metrics Can Look Delayed

If a system slows down:
- requests start timing out
- but only appear in metrics **after they finish**

This causes **delayed P99 spikes**, not incorrect metrics.

---

## 9. Common Misconceptions

❌ Requests must start and end in the window  
❌ Percentiles are based on start time  
❌ Averages are sufficient for latency analysis  

✅ Completion time decides inclusion  
✅ Latency values are what percentiles use  
✅ Tail latency (P99) reveals real problems  

---

## 10. One-Sentence Summary

Latency is calculated using start and end time, but percentiles are computed over latency values of requests that **complete within the measurement window**, regardless of when they started.

---

## 11. Final Mental Model

- Finish line → decides who is counted
- Start line → decides how long it took
- Percentiles → rank the durations

---

## 12. Final Takeaway

> **Latency uses start and end time.  
> Percentiles use latency values.  
> Window inclusion depends only on completion time.**

