from __future__ import annotations

from typing import Dict, Any

from bot_core.types import BotContext


class ExampleStrategy:
    name = 'example'

    def decide(self, context: BotContext, state: Dict[str, Any]) -> Dict[str, Any]:
        monster = state.get('encounter', {}).get('monster', 'slime')
        return {'type': 'attack', 'target': monster}