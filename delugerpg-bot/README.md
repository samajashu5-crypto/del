# DelugeRPG Bot Framework (TOS-Compliant Scaffold)

This project is a safe, extensible bot framework scaffold for DelugeRPG-like games. It is designed for experimentation, strategy prototyping, and integration ONLY when you have explicit authorization and a published API. It ships with a mock client for local simulation.

Important: Do not automate interactions with any website or game without explicit written permission and adherence to their Terms of Service. This repository defaults to a mock client and includes guardrails that block unauthorized online automation.

## Features
- Strategy pattern for modular decision logic
- Mock client for local-only simulations
- Safety guardrails requiring explicit consent flags for any online client
- Config via environment variables (`.env`) with Pydantic validation
- Rate limiting and backoff helpers
- Structured logging with Rich
- Basic tests via pytest

## Quick Start

1. Create a virtual environment (optional) and install dependencies:
   
   ```bash
   cd delugerpg-bot
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and adjust if needed:
   
   ```bash
   cp .env.example .env
   ```

3. Run the bot with the mock client (safe default):
   
   ```bash
   python -m bot_core.cli --client mock --strategy example --run-seconds 5
   ```

4. Run tests:
   
   ```bash
   pytest -q
   ```

## Safety and Compliance
- This framework blocks the `authorized` client unless you provide:
  - A legit API base URL and token in `.env`
  - The explicit run flag `--i-affirm-i-have-permission`
- You are responsible for complying with applicable Terms of Service and laws.

## Structure
```
./
├── bot_core/            # Core loop, CLI, types, rate limiter
├── clients/             # Client implementations
├── strategies/          # Strategy implementations
├── config/              # Settings and environment config
├── tests/               # Unit tests
├── requirements.txt
└── README.md
```

## Extending
- Add a new strategy in `strategies/` and register it in `bot_core/cli.py`.
- Implement a new client by following the interface in `bot_core/types.py`.
- Use the mock client while iterating; switch to an authorized client only if you have permission.