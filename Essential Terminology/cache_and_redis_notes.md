# Cache

- Interacting with cache servers is simple because most cache servers provide **APIs** for common programming languages.




# Redis Notes for Beginners

---

## 1️⃣ What is Redis?

- **Redis** = Remote Dictionary Server
- **In-memory key-value store**, extremely fast
- Use cases:
  - Caching
  - Counters / rate limiting
  - Queues
  - Session management
  - Real-time notifications (Pub/Sub)
- Optional persistence: data can be saved to disk

---

## 2️⃣ Why Redis is Popular

- Super fast (in-memory)
- Supports multiple data types
- Atomic operations
- Simple and lightweight
- Can scale horizontally with **Redis Cluster**
- Easy to integrate with Python, Node.js, Go, etc.

---

## 3️⃣ Redis Architecture

- Server process runs separately from your app
- Clients connect (Python, Node.js, CLI)
- Data lives in RAM, optionally persisted on disk
- Commands are executed atomically (single-threaded)
- Single-threaded, so no locking issues

> App Server → Redis → Data stored in memory


---

## 4️⃣ Redis Data Types

| Data Type      | Description                   | Example                              |
|----------------|-------------------------------|--------------------------------------|
| String         | Simple key-value              | `SET name "Alice"`                   |
| Hash           | Map/dict                     | `HSET user:1 name "Alice"`           |
| List           | Ordered list                  | `LPUSH tasks "task1"`                |
| Set            | Unique, unordered             | `SADD online_users "user1"`          |
| Sorted Set     | Set with scores               | `ZADD leaderboard 100 "Alice"`       |
| Bitmaps        | Store bits efficiently        | `SETBIT mykey 7 1`                   |
| HyperLogLog    | Approximate unique counts     | `PFADD visitors user1`               |
| Streams        | Persistent log for messaging  | `XADD mystream * name Alice`         |

---

## 5️⃣ Redis Commands (Basics)

### Strings
```bash
SET key value          # Set value
GET key                # Get value
DEL key                # Delete key
INCR key               # Increment integer
EXPIRE key 10          # Set TTL() (10 seconds)
```

### Hash

```bash
HSET user:1 name "Alice" age 20
HGETALL user:1
HGET user:1 name
```

### List

```bash
LPUSH tasks "task1"
RPUSH tasks "task2"
LRANGE tasks 0 -1
LPOP tasks
```

### Set
```bash
SADD online_users "user1"
SADD online_users "user2"
SMEMBERS online_users
SISMEMBER online_users "user1"
```

### Sorted Set
```bash
ZADD leaderboard 100 "Alice"
ZADD leaderboard 150 "Bob"
ZRANGE leaderboard 0 -1 WITHSCORES
```

### Pub/Sub
```bash
SUBSCRIBE channel
PUBLISH channel "message"
```

## 6️⃣ Redis Persistence

### RDB (snapshotting)
- Saves a snapshot of data at intervals
- Fast restore, but some data may be lost

### AOF (Append Only File)
- Logs every write command
- More durable, slower than RDB
- Can replay commands to recover data

### Hybrid
- Many setups use RDB + AOF for durability and speed

## 7️⃣ Redis Expiry / TTL (Time-to-Live)

- Useful for caching or temporary data
```bash
SET temp "123" EX 10   # Expires in 10 seconds
TTL temp               # Check remaining time
PERSIST temp           # Remove expiry
```

## 8️⃣ Redis Pub/Sub
- Publisher: sends messages to channel
- Subscriber: listens to channel
- Messages are ephemeral (not stored)

### Example
```python
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
pubsub = r.pubsub()

pubsub.subscribe("my_channel")
for message in pubsub.listen():
    if message["type"] == "message":
        print("Received:", message["data"])
```

### more example

```python
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# String
r.set("name", "Alice")
print(r.get("name"))

# Counter
r.incr("visits")
print(r.get("visits"))

# Hash
r.hset("user:1", mapping={"name": "Alice", "age": 20})
print(r.hgetall("user:1"))

# List
r.lpush("tasks", "task1")
r.rpush("tasks", "task2")
print(r.lrange("tasks", 0, -1))
```

# what is lua script or lua programming language in redis

In Redis, a Lua script is a user-defined program written in the Lua programming language that is executed directly on the Redis server. This allows developers to embed complex application logic into the database, performing conditional updates and multiple operations as a single, unified command

### Key Characteristics
- **Atomicity** : Redis guarantees that scripts are executed atomically. No other commands from any client will run while the script is executing, ensuring data consistency without the need for complex locks.

- **Efficiency** : By running logic on the server ("where the data lives"), scripts eliminate multiple network round-trips between the client and server.

- **Sandboxed Environment** : Scripts run in a secure, isolated context that prevents them from accessing the host file system or network, focusing only on Redis data.

- **Script Caching** : Redis automatically caches scripts by their SHA1 hash. You can use the EVALSHA command to run a cached script using only its hash, which saves bandwidth by not resending the full source code. 
