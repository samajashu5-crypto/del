from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Dict, Any


@dataclass
class BotContext:
    """Shared state passed between strategy and client each tick."""
    tick_index: int
    metadata: Dict[str, Any]


class GameClient(Protocol):
    def identify(self) -> str:
        """Return a short client identifier."""

    def fetch_state(self, context: BotContext) -> Dict[str, Any]:
        """Fetch current game state (mock or real).
        Must be rate-limited and resilient to failures in concrete implementations.
        """

    def perform_action(self, context: BotContext, action: Dict[str, Any]) -> Dict[str, Any]:
        """Perform an action and return the outcome payload."""


class Strategy(Protocol):
    name: str

    def decide(self, context: BotContext, state: Dict[str, Any]) -> Dict[str, Any]:
        """Return an action dict based on current state and context."""