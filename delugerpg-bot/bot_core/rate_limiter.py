import threading
import time
from typing import Optional


class TokenBucketLimiter:
    """Simple thread-safe token bucket rate limiter.

    capacity: maximum tokens
    refill_rate_per_sec: tokens added per second
    """

    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = max(1, capacity)
        self.refill_rate_per_sec = max(0.001, refill_rate_per_sec)
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self, tokens: float = 1.0, timeout_sec: Optional[float] = None) -> bool:
        deadline = None if timeout_sec is None else time.monotonic() + timeout_sec
        while True:
            with self._lock:
                now = time.monotonic()
                elapsed = now - self._last_refill
                self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate_per_sec)
                self._last_refill = now
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return True
            if deadline is not None and time.monotonic() >= deadline:
                return False
            time.sleep(0.01)