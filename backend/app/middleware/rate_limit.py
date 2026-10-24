import time
from collections import defaultdict
from typing import Dict, List
from ..config.settings import settings

class RateLimiter:
    """
    Sliding window rate limiter to protect banking APIs against flooding.
    """
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.history: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, client_key: str) -> bool:
        now = time.time()
        window_start = now - 60.0

        # Filter out timestamps older than 60s
        self.history[client_key] = [t for t in self.history[client_key] if t > window_start]

        if len(self.history[client_key]) >= self.requests_per_minute:
            return False

        self.history[client_key].append(now)
        return True

rate_limiter = RateLimiter(requests_per_minute=settings.RATE_LIMIT_PER_MINUTE)
