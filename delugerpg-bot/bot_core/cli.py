from __future__ import annotations

import argparse
import sys

from rich.console import Console

from bot_core.loop import run_loop
from config.settings import settings
from strategies.example_strategy import ExampleStrategy
from clients.mock_client import MockClient

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='DelugeRPG bot framework (TOS-compliant scaffold)'
    )
    parser.add_argument('--client', choices=['mock', 'authorized'], default='mock')
    parser.add_argument('--strategy', choices=['example'], default='example')
    parser.add_argument('--run-seconds', type=int, default=settings.run_seconds)
    parser.add_argument('--i-affirm-i-have-permission', action='store_true', default=False,
                        help='Required for authorized client runs')
    return parser


def resolve_client(name: str, permission_ok: bool):
    if name == 'mock':
        return MockClient()
    if name == 'authorized':
        if not permission_ok:
            console.print('[red]Refusing to run authorized client without explicit permission flag.[/]')
            console.print('Pass --i-affirm-i-have-permission and ensure you have written authorization and API docs.')
            sys.exit(2)
        from clients.authorized_api_client import AuthorizedApiClient  # lazy import
        return AuthorizedApiClient()
    raise ValueError(f'Unknown client: {name}')


def resolve_strategy(name: str):
    if name == 'example':
        return ExampleStrategy()
    raise ValueError(f'Unknown strategy: {name}')


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    client = resolve_client(args.client, args.i_affirm_i_have_permission)
    strategy = resolve_strategy(args.strategy)

    result = run_loop(
        client=client,
        strategy=strategy,
        run_seconds=args.run_seconds,
        capacity=settings.rate_limit.capacity,
        refill_per_sec=settings.rate_limit.refill_per_sec,
    )

    console.log(result)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())