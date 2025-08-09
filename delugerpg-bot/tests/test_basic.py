from __future__ import annotations

from bot_core.rate_limiter import TokenBucketLimiter
from bot_core.loop import run_loop
from clients.mock_client import MockClient
from strategies.example_strategy import ExampleStrategy


def test_token_bucket_limiter_allows_progress():
    limiter = TokenBucketLimiter(capacity=2, refill_rate_per_sec=1000)
    assert limiter.acquire()
    assert limiter.acquire()
    assert limiter.acquire()


def test_run_loop_with_mock_client():
    client = MockClient(seed=42)
    strategy = ExampleStrategy()
    result = run_loop(client=client, strategy=strategy, run_seconds=1, capacity=10, refill_per_sec=100)
    assert result['ticks'] > 0