from __future__ import annotations

import time
from typing import Dict, Any

from rich.console import Console

from bot_core.rate_limiter import TokenBucketLimiter
from bot_core.types import BotContext, GameClient, Strategy


console = Console()


def run_loop(
    *,
    client: GameClient,
    strategy: Strategy,
    run_seconds: int,
    capacity: int,
    refill_per_sec: float,
) -> Dict[str, Any]:
    limiter = TokenBucketLimiter(capacity=capacity, refill_rate_per_sec=refill_per_sec)
    started = time.monotonic()
    tick_index = 0
    metadata: Dict[str, Any] = {}

    console.log(f"Starting loop with client={client.identify()} strategy={getattr(strategy, 'name', 'unknown')}")

    while time.monotonic() - started < run_seconds:
        if not limiter.acquire(timeout_sec=5.0):
            console.log("Rate limiter timeout; exiting loop.")
            break

        context = BotContext(tick_index=tick_index, metadata=metadata)
        state = client.fetch_state(context)
        action = strategy.decide(context, state)
        result = client.perform_action(context, action)

        console.log({
            'tick': tick_index,
            'state': state,
            'action': action,
            'result': result,
        })

        tick_index += 1
        time.sleep(0.25)  # small sleep to avoid tight loop

    console.log("Loop finished.")
    return {'ticks': tick_index}