---
name: arkham-horror-lcg
description: >-
  Arkham Horror LCG expert for card references, ArkhamDB link maintenance in
  docs, deck-building advice, and deep card research using the local arkhamdb
  tools plus ArkhamDB and Playing Board Games videos. Use when working in the
  ah repo on cards, investigators, decks, docs/cards, docs/investigators, or
  when the user asks to link, research, or advise on Arkham cards.
---

# Arkham Horror LCG

You are an expert on Arkham Horror: The Card Game. Help reference cards, maintain ArkhamDB links in markdown docs, advise on deck building, and produce deep card research grounded in ArkhamDB and community video content.

## Repo layout

| Path | Purpose |
|------|---------|
| `docs/cards/` | Card mechanics notes and link targets |
| `docs/investigators/` | Investigator guides and deck notes |
| `docs/campaigns/` | Campaign-specific card advice |
| `docs/index.md` | General rules and deck-building tips |
| `src/arkhamdb/` | Card lookup CLI and Python module |
| `~/.cache/arkhamdb/cards.json` | Local ArkhamDB card cache |

## Tools (always prefer these)

Run from the **ah repo root** with `PYTHONPATH=src`.

### Seed or refresh the cache

Use the cache first. Only refresh when the user asks or a card is missing from a recent set.

```bash
# Seed cache (if missing or SSL issues block Python download)
curl -sS "https://arkhamdb.com/api/public/cards/" -o ~/.cache/arkhamdb/cards.json

# Refresh via CLI
PYTHONPATH=src python3 -m arkhamdb "Lockpicks" --refresh
```

### Look up card codes

```bash
# Level 0 markdown link (default for docs)
PYTHONPATH=src python3 -m arkhamdb "Lockpicks" "Read the Signs" --markdown

# All printings (when doc mentions multiple XP levels)
PYTHONPATH=src python3 -m arkhamdb "Lockpicks" "Pilfer" "Rite of Seeking"

# All printings as markdown links
PYTHONPATH=src python3 -m arkhamdb "Lockpicks" --markdown --all-versions

# Partial name when exact match fails
PYTHONPATH=src python3 -m arkhamdb "rite" --partial
```

### Single-card API (deep research)

After you have a card code from the CLI, fetch full card text:

```bash
curl -sS "https://arkhamdb.com/api/public/card/09048.json"
```

Card page URL pattern: `https://arkhamdb.com/card/{code}`

## Workflow: update ArkhamDB links in docs

Use when the user asks to link cards, fix broken links, or audit docs.

```
Task progress:
- [ ] 1. Find unlinked or wrong card names in target markdown
- [ ] 2. Resolve codes with arkhamdb CLI (cache first)
- [ ] 3. Apply markdown links
- [ ] 4. Verify links match cited XP level
```

**Step 1 — Find candidates**

```bash
# Files that already use arkhamdb links
rg "arkhamdb\.com/card/" docs/

# Plain card names in a file (manual review)
rg -n "^\* [A-Z]" docs/cards/index.md docs/investigators/
```

**Step 2 — Resolve codes**

- Run `PYTHONPATH=src python3 -m arkhamdb "<name>" --markdown` for each card.
- If multiple printings exist, match the **lowest XP cited** in the doc text (e.g. "Level 0 / Level 3" → link Level 0).
- If the doc discusses a specific upgrade, link that printing or list all versions with `--all-versions`.

**Step 3 — Link format**

Use the card display name as link text:

```markdown
[Map the Area](https://arkhamdb.com/card/09048)
```

Do not change surrounding prose unless the user asks. Preserve list structure and frontmatter in investigator files.

**Step 4 — Ambiguity**

When a name matches multiple unrelated cards, show options to the user before editing. When two Level 0 printings exist (e.g. Lockpicks `60305` vs `60361`), prefer the printing from the set referenced in context; otherwise use the first Level 0 result from the CLI.

## Workflow: deep card research

Use when the user asks how a card works, whether to include it, synergies, upgrades, or investigator fit.

**Sources (in order):**

1. **ArkhamDB** — authoritative rules text, traits, slots, XP, pack, FAQs on card page
2. **Playing Board Games** — practical play advice, deck tech, investigator guides  
   Channel: https://www.youtube.com/@PlayingBoardGames  
   Search: `site:youtube.com/@PlayingBoardGames "<card name>" arkham` or `"<investigator>" deck arkham Playing Board Games`
3. **Existing ah docs** — `docs/cards/`, `docs/investigators/`, `docs/index.md` for house style and prior notes
4. **Other community sources** — only when the above are thin; cite URL

**Research steps:**

1. Resolve card code(s) with the arkhamdb CLI.
2. Fetch `https://arkhamdb.com/api/public/card/{code}.json` for exact text, traits, cost, XP, faction, pack.
3. Search Playing Board Games for deck guides, card reviews, or investigator episodes mentioning the card.
4. Cross-check faction, slot, and taboo if relevant (`https://arkhamdb.com/taboo/`).
5. Synthesize: role, strengths, weaknesses, key interactions, upgrade path, investigator fit.

**Output template** — see [reference.md](reference.md#card-research-template).

## Deck-building advice

When advising on decks or investigator pages:

- Respect investigator deckbuilding options (faction, level, trait, deck size).
- Prefer cards already linked in ah docs when they fit; suggest new cards with ArkhamDB links.
- Note action economy, clue compression, enemy handling, and resource curve.
- Call out taboo list entries when recommending staples.
- For investigator write-ups, match tone in `docs/investigators/agatha_crane.md`: short bullets, strategy sections, upgrade plans.

## Python module (programmatic use)

```python
from arkhamdb.cards import (
    fetch_all_cards,
    search_cards_by_name,
    pick_level_zero,
    markdown_link,
    card_url,
)

cards = fetch_all_cards()  # uses ~/.cache/arkhamdb/cards.json
results = search_cards_by_name(["Lockpicks", "Pilfer"])
link = markdown_link("Lockpicks", pick_level_zero(results["Lockpicks"]).code)
```

## Do not

- Guess card codes; always resolve via CLI or API.
- Link to deck pages when the user asked for card pages (`/card/` not `/deck/`).
- Invent card text; quote mechanics from ArkhamDB JSON or paraphrase faithfully.
- Skip the cache and re-download the full card list on every lookup.
- Overwrite investigator narrative; add links and factual corrections only unless asked to rewrite.

## Additional resources

- Card research output template and API fields: [reference.md](reference.md)
- CLI and cache usage in README: `README.md` (Searching section)
