from __future__ import annotations

import random
from typing import Dict, Any

from bot_core.types import BotContext


class MockClient:
    def __init__(self, seed: int | None = None) -> None:
        self.random = random.Random(seed)

    def identify(self) -> str:
        return 'mock-client'

    def fetch_state(self, context: BotContext) -> Dict[str, Any]:
        return {
            'player': {'hp': 100, 'xp': context.tick_index * 2},
            'encounter': {'monster': self.random.choice(['slime', 'bat', 'rat'])},
        }

    def perform_action(self, context: BotContext, action: Dict[str, Any]) -> Dict[str, Any]:
        outcome = self.random.choice(['success', 'miss'])
        reward = self.random.randint(1, 5) if outcome == 'success' else 0
        return {'outcome': outcome, 'reward': reward}