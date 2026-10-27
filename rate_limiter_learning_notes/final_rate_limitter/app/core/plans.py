API_KEY_PLANS = {
    "free-key-123": "FREE",
    "paid-key-456": "PAID",
}


PLANS = {
    "FREE": {
        "max_tokens": 5,
        "refill_rate": 1 / 12,   # 5 per minute
    },
    "PAID": {
        "max_tokens": 20,
        "refill_rate": 1 / 3,    # 20 per minute
    },
}
