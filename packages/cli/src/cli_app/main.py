"""Argument parsing and command dispatch for the CLI package."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from core import ConfigurationError, IssueDigestError, IssueStatus

from cli_app.commands.fetch import fetch_items
from cli_app.commands.health import build_health_report
from cli_app.commands.items import list_items, show_item
from cli_app.config import CliConfig
from cli_app.output import emit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="issue-digest",
        description="Developer issue digest workspace CLI.",
    )
    parser.add_argument("--config", type=Path, help="Path to a local TOML config file.")

    subparsers = parser.add_subparsers(dest="command")

    health = subparsers.add_parser(
        "health",
        help="Show local health and optional remote API health.",
    )
    health.add_argument(
        "--remote",
        action="store_true",
        help="Also call the configured API health endpoint.",
    )
    health.add_argument("--output", choices=("text", "json"))
    health.set_defaults(handler=_run_health)

    fetch = subparsers.add_parser("fetch", help="Fetch items from the configured API.")
    fetch.add_argument("--status", choices=tuple(status.value for status in IssueStatus))
    fetch.add_argument("--limit", type=_positive_int)
    fetch.add_argument("--output", choices=("text", "json"))
    fetch.set_defaults(handler=_run_fetch)

    items = subparsers.add_parser("items", help="Work with local in-memory issues.")
    item_subparsers = items.add_subparsers(dest="items_command")

    items_list = item_subparsers.add_parser("list", help="List local issues.")
    items_list.add_argument("--status", choices=tuple(status.value for status in IssueStatus))
    items_list.add_argument("--assignee")
    items_list.add_argument("--search")
    items_list.add_argument("--limit", type=_positive_int)
    items_list.add_argument("--output", choices=("text", "json"))
    items_list.set_defaults(handler=_run_items_list)

    items_show = item_subparsers.add_parser(
        "show",
        help="Show one local issue by id.",
    )
    items_show.add_argument("issue_id")
    items_show.add_argument("--output", choices=("text", "json"))
    items_show.set_defaults(handler=_run_items_show)

    return parser


def run(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 1

    try:
        config = CliConfig.from_env(config_path=args.config)
        payload = handler(args, config)
        output = getattr(args, "output", None) or config.default_output
        emit(payload, output=output, stream=sys.stdout)
        return 0
    except (ConfigurationError, IssueDigestError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


def _run_health(args: argparse.Namespace, config: CliConfig) -> dict[str, object]:
    return build_health_report(config, remote=args.remote)


def _run_fetch(args: argparse.Namespace, config: CliConfig) -> dict[str, object]:
    return fetch_items(config, status=args.status, limit=args.limit)


def _run_items_list(args: argparse.Namespace, config: CliConfig) -> object:
    del config
    status = IssueStatus(args.status) if args.status else None
    return list_items(
        status=status,
        assignee=args.assignee,
        search=args.search,
        limit=args.limit,
    )


def _run_items_show(args: argparse.Namespace, config: CliConfig) -> object:
    del config
    return show_item(args.issue_id)


def _positive_int(raw: str) -> int:
    value = int(raw)
    if value <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return value
