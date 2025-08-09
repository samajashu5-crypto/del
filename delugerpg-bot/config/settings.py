from __future__ import annotations

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RateLimitConfig(BaseModel):
    capacity: int = Field(default=5, ge=1)
    refill_per_sec: float = Field(default=1.0, gt=0)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', env_prefix='BOT_')

    # General
    log_level: str = 'INFO'
    run_seconds: int = 10

    # Authorized API (must have permission)
    api_base_url: str | None = None
    api_token: str | None = None

    # Rate limiting
    rate_limit: RateLimitConfig = RateLimitConfig()


settings = AppSettings()  # Loaded at import time