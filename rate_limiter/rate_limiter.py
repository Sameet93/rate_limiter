# File: rate_limiter/rate_limiter.py
import time
from functools import wraps
from .caches import MemoryCache

def rate_limit(limit, period, identifier=lambda: "global", cache=None, auto_ban=False, ban_threshold=None, ban_duration=60):
    if cache is None:
        cache = MemoryCache()  # default backend if none provided

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Determine the key: allow identifier to be a callable (e.g., a lambda that inspects the request)
            key = identifier() if callable(identifier) else identifier

            # If auto_ban is enabled, check if the user is banned
            if auto_ban and cache.is_banned(key):
                raise Exception("Too many requests – you are temporarily banned.")

            # Increase the request count for the key
            current_count = cache.incr(key, period)
            if current_count > limit:
                # Optionally, if a ban threshold is set and exceeded, auto-ban the user
                if auto_ban and ban_threshold is not None and current_count > ban_threshold:
                    cache.ban(key, ban_duration)
                raise Exception("Rate limit exceeded.")
            return func(*args, **kwargs)
        return wrapper
    return decorator

