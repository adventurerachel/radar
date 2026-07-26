# Scrumbles Price Monitor

## Purpose

Daily monitoring of:

**Scrumbles Turkey Adult & Senior Dry Dog Food 2kg**

across:

- Waitrose
- Tesco
- Sainsbury's
- Asda
- Pets at Home


## How it works

The monitor:

1. Uses OpenAI web search to locate current retailer pricing.
2. Extracts prices into a standard JSON structure.
3. Appends results to JSONL storage.
4. Prevents duplicate entries if a workflow is rerun.


## Data storage

Results are stored in:
