# File: rate_limiter/caches.py
import time

class MemoryCache:
    def __init__(self):
        # The store holds keys with a tuple: (value, expiry_timestamp)
        self.store = {}

    def get(self, key):
        entry = self.store.get(key)
        if entry:
            value, expiry = entry
            if time.time() < expiry:
                return value
            # Expired entry; remove it
            del self.store[key]
        return None

    def set(self, key, value, expire):
        self.store[key] = (value, time.time() + expire)

    def incr(self, key, expire):
        current_time = time.time()
        # Retrieve the current count or reset if expired
        entry = self.store.get(key)
        if entry:
            value, expiry = entry
            if current_time > expiry:
                value = 0
        else:
            value = 0
        value += 1
        self.store[key] = (value, current_time + expire)
        return value

    def is_banned(self, key):
        # Check if a ban marker exists and is still active
        ban_entry = self.store.get(f"ban:{key}")
        if ban_entry:
            _, ban_expiry = ban_entry
            if time.time() < ban_expiry:
                return True
            del self.store[f"ban:{key}"]
        return False

    def ban(self, key, ban_duration):
        # Set a ban marker for the key
        self.store[f"ban:{key}"] = (None, time.time() + ban_duration)

