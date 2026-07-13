"""CLI for searching ArkhamDB cards by name."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from arkhamdb.cards import (
    DEFAULT_CACHE_PATH,
    fetch_all_cards,
    format_match,
    markdown_link,
    pick_level_zero,
    search_cards_by_name,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search ArkhamDB cards by name and print card codes or markdown links.",
    )
    parser.add_argument(
        "names",
        nargs="+",
        help="One or more card names to look up (exact match by default).",
    )
    parser.add_argument(
        "--partial",
        action="store_true",
        help="Use case-insensitive partial name matching instead of exact match.",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Print a markdown link for the level 0 printing when available.",
    )
    parser.add_argument(
        "--all-versions",
        action="store_true",
        help="Print every matching printing instead of only level 0 for markdown output.",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Re-download the card list instead of using the local cache.",
    )
    parser.add_argument(
        "--cache-path",
        type=Path,
        default=DEFAULT_CACHE_PATH,
        help=f"Local cache file for the card list (default: {DEFAULT_CACHE_PATH}).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cards = fetch_all_cards(cache_path=args.cache_path, force_refresh=args.refresh)
    results = search_cards_by_name(args.names, cards=cards, exact=not args.partial)

    exit_code = 0
    for name, matches in results.items():
        print(f"\n=== {name} ({len(matches)} match{'es' if len(matches) != 1 else ''}) ===")
        if not matches:
            print("  (no matches)")
            exit_code = 1
            continue

        if args.markdown and not args.all_versions:
            chosen = pick_level_zero(matches)
            if chosen:
                print(f"  {markdown_link(chosen.name, chosen.code)}")
            continue

        for match in matches:
            line = format_match(match)
            if args.markdown:
                line = f"{markdown_link(match.name, match.code)}  # {line}"
            print(f"  {line}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
