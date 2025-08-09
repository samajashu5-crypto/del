from __future__ import annotations

from typing import Dict, Any

import httpx
from bot_core.types import BotContext
from config.settings import settings


class AuthorizedApiClient:
    def __init__(self, http_timeout_sec: float = 10.0) -> None:
        if not settings.api_base_url or not settings.api_token:
            raise RuntimeError(
                'AuthorizedApiClient requires BOT_API_BASE_URL and BOT_API_TOKEN in .env.'
            )
        self.client = httpx.Client(
            base_url=settings.api_base_url,
            headers={'Authorization': f'Bearer {settings.api_token}'},
            timeout=httpx.Timeout(http_timeout_sec)
        )

    def identify(self) -> str:
        return 'authorized-api-client'

    def fetch_state(self, context: BotContext) -> Dict[str, Any]:
        # Placeholder example; replace with real authorized endpoints as permitted
        resp = self.client.get('/state')
        resp.raise_for_status()
        return resp.json()

    def perform_action(self, context: BotContext, action: Dict[str, Any]) -> Dict[str, Any]:
        resp = self.client.post('/action', json=action)
        resp.raise_for_status()
        return resp.json()