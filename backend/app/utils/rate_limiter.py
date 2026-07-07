import time
import os
from collections import defaultdict
import threading

class InMemoryRateLimiter:
    """
    Thread-safe, in-memory sliding window rate limiter.
    Does not require Redis or external service dependencies.
    Bypasses validation checks during test suite runs.
    """
    def __init__(self, requests_limit: int, window_seconds: int):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.history = defaultdict(list)
        self.lock = threading.Lock()

    def check_rate_limit(self, key: str) -> bool:
        """
        Increments the request count for a given key (e.g. IP address).
        Returns True if the rate limit is exceeded, False otherwise.
        """
        # Bypass rate limits when executing tests
        if os.environ.get("TESTING") == "True":
            return False
            
        now = time.time()
        with self.lock:
            # Prune obsolete request logs outside of current window
            self.history[key] = [t for t in self.history[key] if now - t < self.window_seconds]
            
            if len(self.history[key]) >= self.requests_limit:
                return True
                
            self.history[key].append(now)
            return False

# Rate limiting instances: 5 attempts per IP address per 60 seconds
login_limiter = InMemoryRateLimiter(requests_limit=5, window_seconds=60)
register_limiter = InMemoryRateLimiter(requests_limit=5, window_seconds=60)
# Rate limiting instances: 30 attempts per IP address per 60 seconds
query_limiter = InMemoryRateLimiter(requests_limit=30, window_seconds=60)
