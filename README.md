# [Arkham Horror LCG personal notes](https://jbcodeforce.github.io/ah)

Agentic based knowledge management about Arkham Horror.

## Documentation

[Read book view](https://jbcodeforce.github.io/ah)

## Research

* Research content on the web - summarize 

## Indexing

* Add frontmatter to raw files:
    ```sh
    under km-agent
    uv run python scripts/add_raw_frontmatter.py ../ah/docs --source ah
    ```

## Searching

seed the cache with:
```sh
curl -sS "https://arkhamdb.com/api/public/cards/" -o ~/.cache/arkhamdb/cards.json
```

Usage (from the ah repo root):
```sh
# All printings for one or more cards
PYTHONPATH=src python3 -m arkhamdb "Lockpicks" "Pilfer" "Rite of Seeking"

# Level 0 markdown link (what we used for docs/cards/index.md)
PYTHONPATH=src python3 -m arkhamdb "Lockpicks" "Read the Signs" --markdown

# Every printing as markdown links
PYTHONPATH=src python3 -m arkhamdb "Lockpicks" --markdown --all-versions

# Partial name search
PYTHONPATH=src python3 -m arkhamdb "rite" --partial

# Force refresh from ArkhamDB
PYTHONPATH=src python3 -m arkhamdb "Curiosity" --refresh
```
