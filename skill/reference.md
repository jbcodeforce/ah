# Arkham Horror LCG — reference

## Card research template

Use this structure for deep card research responses:

```markdown
# [Card Name](https://arkhamdb.com/card/XXXXX)

## At a glance
- **Faction / type / cost / XP:** ...
- **Slots:** ...
- **Traits:** ...
- **Pack:** ...

## What it does
[Faithful summary from ArkhamDB text]

## Why play it
- [Role in deck: clue compression, evasion, economy, etc.]
- [Stat substitution or test modifier if applicable]

## Synergies and interactions
- [Investigators, assets, events, traits]
- [Timing: fast, reaction, end of turn]

## Downsides and counters
- [Resource cost, slot pressure, token risk, scenario weakness]

## Upgrade path
- [Level 0 → higher XP printings, when to buy]

## Community notes
- [Playing Board Games or other cited sources with links]
  - [Video title](https://www.youtube.com/...) — one-line takeaway

## Fit for [investigator or archetype]
[Short recommendation]
```

## ArkhamDB API fields (single card)

`GET https://arkhamdb.com/api/public/card/{code}.json`

| Field | Use |
|-------|-----|
| `name` | Display name and link text |
| `code` | Card URL segment |
| `text` | Rules text (may include HTML) |
| `type_code` | asset, event, skill, treachery, ... |
| `faction_code` | guardian, seeker, rogue, mystic, survivor, neutral |
| `cost` | Resource cost |
| `xp` | Experience level |
| `traits` | Trait string |
| `slot` | Body, hand, arcane, ally, ... |
| `skill_agility`, `skill_intellect`, `skill_combat`, `skill_willpower` | Committed icons |
| `pack_code` | Expansion pack |
| `deck_limit` | Taboo or limit notes |
| `flavor` | Flavor text (optional context) |

Full card list: `GET https://arkhamdb.com/api/public/cards/` (cached locally).

## Playing Board Games research

**Channel:** https://www.youtube.com/@PlayingBoardGames

**Hosts:** Justin, Travis (also referenced in `docs/index.md`).

**When to search:**

| Goal | Query pattern |
|------|----------------|
| Card in decks | `site:youtube.com PlayingBoardGames "<card name>" arkham deck` |
| Investigator guide | `site:youtube.com PlayingBoardGames "<investigator>" arkham` |
| Expansion overview | `site:youtube.com PlayingBoardGames "<expansion name>" arkham horror` |
| Mechanic explainers | `site:youtube.com PlayingBoardGames arkham "<mechanic>"` |

**How to use video results:**

- Prefer episodes that show the card in play or in a decklist.
- Extract practical tips (when to play, mulligan, upgrade priority), not generic rules.
- Link the video in "Community notes"; do not claim video content without finding it.
- If no relevant PBG video exists, say so and rely on ArkhamDB + ah docs.

## Doc link audit commands

```bash
# Count linked cards per file
rg -c "arkhamdb\.com/card/" docs/

# List unique card codes already in docs
rg -o "arkhamdb\.com/card/[0-9]+" docs/ | sort -u

# Find markdown bold/italic card names without links (manual pass)
rg -n "\*\*[A-Z][a-zA-Z' ]+\*\*" docs/investigators/
```

## XP level linking rules

| Doc text | Link target |
|----------|-------------|
| `Level 0 Event` | XP = 0 printing |
| `Level 0 / Level 3 Asset` | XP = 0 printing (mention upgrades in prose) |
| `upgrade to Lockpicks (1)` | XP = 1 printing `01687` or `03031` — confirm with CLI |
| Discussing a specific taboo or promo | Match that printing explicitly |

When documenting multiple versions in one bullet, optional format:

```markdown
[Lockpicks](https://arkhamdb.com/card/60305) (0) / [Lockpicks](https://arkhamdb.com/card/01687) (1)
```

## Investigator doc conventions

Files under `docs/investigators/` may include YAML frontmatter (`title`, `source`, `tags`). Preserve it.

Typical sections:

- Key cards and strategy (bullets with linked card names)
- Upgrade plans
- Archetype variants (e.g. Seeker vs Mystic)

Match existing link density in `agatha_crane.md` and `index.md`.
