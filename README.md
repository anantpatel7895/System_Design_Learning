# System_Design_Learning
this is the notes on system design

# 🚀 What Are Coroutines in Python? (Detailed Explanation)

A coroutine is a special Python function defined with async def that can:
- pause at an await
- yield control to let other coroutines run
- resume later from where it paused

This is the foundation of Python’s **async / await** system and the asyncio library.

Coroutines are mainly used for **asynchronous programming**, especially for **I/O work (network calls, file access, timers)**.

## 🔹 Part 1 — Basic Coroutine Example
Example: A simple coroutine that prints a message
```python
import asyncio

async def say_hello():
    print("Hello")
    await asyncio.sleep(1)  # pauses here for 1 second
    print("World")

asyncio.run(say_hello())
```

### What happens?
- say_hello() begins.
- It prints "Hello".
- await asyncio.sleep(1) pauses the coroutine without blocking the program.
- After 1 second, it resumes and prints "World".

## 🔹 Part 2 — Why We Use await

await tells Python:

- “Pause this coroutine and run something else until this result is ready.”

Example:
```python
await asyncio.sleep(2)
```

This doesn't block the CPU — other async tasks can run while waiting.

## 🔹 Part 3 — Running Multiple Coroutines Concurrently
### Example: Running two coroutines at the same time
```python
import asyncio

async def task(name, delay):
    print(f"{name} started")
    await asyncio.sleep(delay)
    print(f"{name} finished after {delay} sec")

async def main():
    # start tasks together
    await asyncio.gather(
        task("A", 2),
        task("B", 1),
    )

asyncio.run(main())
```
### Output order:
```python
A started
B started
B finished after 1 sec
A finished after 2 sec
```

Even though A started first, B finishes first because it waited less.

## 🔹 Part 4 — How Coroutines Work Internally (Beginner-Friendly)

Coroutines are like generators but for async tasks.

### Generator analogy:
- yield in generators
- await in coroutines
- Both pause execution, but:

| Generators         | Coroutines            |
| ------------------ | --------------------- |
| Used for sequences | Used for async tasks  |
| Pause with `yield` | Pause with `await`    |
| Pull-based         | Event loop-controlled |

## 🔹 Part 5 — A More Real-Life Example
### Example: Fetching data from multiple servers concurrently

(Simulated with sleep)
```python
import asyncio

async def fetch(server):
    print(f"Fetching from {server}...")
    await asyncio.sleep(1)  # simulate network delay
    print(f"Done fetching from {server}")
    return f"Data from {server}"

async def main():
    servers = ["server1", "server2", "server3"]
    
    results = await asyncio.gather(*(fetch(s) for s in servers))
    
    print("Results:", results)

asyncio.run(main())
```

### Output:
```python
Fetching from server1...
Fetching from server2...
Fetching from server3...
Done fetching from server2
Done fetching from server3
Done fetching from server1
Results: ['Data from server1', 'Data from server2', 'Data from server3']
```

All three “requests” run without waiting for each other.

## 🔹 Part 6 — Coroutine Lifecycle (Deep Insight)

A coroutine goes through the following stages:

1. Created (when you call it):
```python
coro = say_hello()
```

(Nothing runs yet)

2. Scheduled (when it's passed to event loop):
```python
asyncio.run(coro)
```
- Running
- Paused (when hitting an await)
- Resumed
- Finished

## 🔹 Part 7 — Common Mistakes Beginners Make
### ❌ Mistake: Calling coroutine without awaiting
```python
say_hello()  # does NOT run!
```

It just creates a coroutine object.

### ✔ Correct
```python
await say_hello()        # inside another coroutine
asyncio.run(say_hello()) # top level
```

## 🔹 Summary

| Concept            | Meaning                           |
| ------------------ | --------------------------------- |
| `async def`        | defines a coroutine               |
| `await`            | pauses and yields control         |
| `asyncio.run()`    | starts the event loop             |
| `asyncio.gather()` | runs coroutines concurrently      |
| Coroutines         | lightweight, async, ideal for I/O |

