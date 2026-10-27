# REQUIREMENTS

- LOAD BALANCER (NGINIX, AWS ELB)
- REDIS

# RATE LIMITER

In a network system, a rate limiter is used to control the rate of traffic sent by a client or a
service. In the HTTP world, a rate limiter limits the number of client requests allowed to be
sent over a specified period. If the API request count exceeds the threshold defined by the
rate limiter, all the excess calls are blocked. Here are a few examples:

- A user can write no more than 2 posts per second.
- You can create a maximum of 10 accounts per day from the same IP address.
- You can claim rewards no more than 5 times per week from the same device.


# What is Throttling?

Rate Limiting is a process that is used to define the rate and speed at which consumers can access APIs. Throttling is the process of controlling the usage of the APIs by customers during a given period. Throttling can be defined at the application level and/or API level. When a throttle limit is crossed, the server returns HTTP status **“429 - Too many requests"**.


# REFERENCE

- [Rate Limiter](https://systemsdesign.cloud/SystemDesign/RateLimiter?utm_source=chatgpt.com)

