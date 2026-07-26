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

Results are stored in: storage/history/dog_food_prices.jsonl

### Scrumbles price monitor

Runs daily and stores historical price observations.

Output:

storage/history/dog_food_prices.jsonl

Each row contains:
- retailer
- regular price
- promotional price
- effective price
- loyalty pricing
- availability
- source quality
- timestamp