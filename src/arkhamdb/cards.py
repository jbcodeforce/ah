"""Look up Arkham Horror LCG cards on ArkhamDB."""

from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ARKHAMDB_API = "https://arkhamdb.com/api/public"
DEFAULT_CACHE_PATH = Path.home() / ".cache" / "arkhamdb" / "cards.json"


@dataclass(frozen=True)
class CardMatch:
    code: str
    name: str
    type_code: str | None
    faction_code: str | None
    xp: int | None
    pack_code: str | None

    @classmethod
    def from_api(cls, card: dict[str, Any]) -> CardMatch:
        return cls(
            code=card["code"],
            name=card["name"],
            type_code=card.get("type_code"),
            faction_code=card.get("faction_code"),
            xp=card.get("xp"),
            pack_code=card.get("pack_code"),
        )


def card_url(code: str) -> str:
    return f"https://arkhamdb.com/card/{code}"


def markdown_link(name: str, code: str) -> str:
    return f"[{name}]({card_url(code)})"


def _ssl_context() -> ssl.SSLContext:
    """Build an SSL context; use certifi CA bundle when installed."""
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def fetch_all_cards(
    *,
    cache_path: Path | None = DEFAULT_CACHE_PATH,
    force_refresh: bool = False,
) -> list[dict[str, Any]]:
    """Download the full card list from ArkhamDB, optionally caching locally."""
    if cache_path and cache_path.exists() and not force_refresh:
        return json.loads(cache_path.read_text(encoding="utf-8"))

    request = urllib.request.Request(
        f"{ARKHAMDB_API}/cards/",
        headers={"User-Agent": "ah-docs-tools/0.1"},
    )
    try:
        with urllib.request.urlopen(
            request,
            timeout=120,
            context=_ssl_context(),
        ) as response:
            cards = json.load(response)
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed to fetch cards from ArkhamDB: {exc}") from exc

    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cards), encoding="utf-8")

    return cards


def search_cards_by_name(
    names: list[str],
    *,
    cards: list[dict[str, Any]] | None = None,
    exact: bool = True,
) -> dict[str, list[CardMatch]]:
    """Return ArkhamDB matches keyed by the requested name."""
    if cards is None:
        cards = fetch_all_cards()

    results: dict[str, list[CardMatch]] = {}
    for name in names:
        needle = name.casefold()
        matches: list[CardMatch] = []
        for card in cards:
            card_name = card.get("name", "")
            haystack = card_name.casefold()
            if exact:
                if haystack != needle:
                    continue
            elif needle not in haystack:
                continue
            matches.append(CardMatch.from_api(card))

        matches.sort(key=lambda match: (match.xp or 0, match.code))
        results[name] = matches

    return results


def pick_level_zero(matches: list[CardMatch]) -> CardMatch | None:
    """Prefer the level 0 printing when multiple versions exist."""
    for match in matches:
        if match.xp == 0:
            return match
    return matches[0] if matches else None


def format_match(match: CardMatch) -> str:
    return (
        f"{match.code}: {match.name} | "
        f"{match.type_code} | {match.faction_code} | "
        f"xp={match.xp} | pack={match.pack_code}"
    )
