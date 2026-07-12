# Radar 📡

An automated web monitoring system that tracks pages for changes, extracts structured information, stores historical observations, and sends notifications when important updates are detected.

Radar is designed as a lightweight, configurable monitoring pipeline that can be adapted to different websites and information sources.

## Features

* 🔎 **Automatic page discovery**

  * Locates the current page or article to monitor using configurable discovery rules.

* 🧩 **Pluggable extractors**

  * Extracts structured data from HTML pages.
  * Supports different extraction strategies depending on the monitored source.

* 📸 **Change detection**

  * Compares newly extracted information against previously stored snapshots.
  * Identifies meaningful changes without requiring manual checking.

* 📚 **Historical tracking**

  * Records every monitoring run as timestamped JSON Lines (`.jsonl`) data.
  * Maintains a history of observations for future analysis.

* 🔔 **Notifications**

  * Sends alerts when monitored content changes.
  * Supports recurring notifications for selected conditions, such as active promotions or announcements.

* ⚙️ **Automated execution**

  * Runs on a scheduled GitHub Actions workflow.
  * Supports manual execution for testing and debugging.

## Architecture

The project separates responsibilities into independent modules:

```text
radar/
│
├── alerts/
│   ├── formatter.py       # Creates notification messages
│   └── pushover.py        # Sends notifications
│
├── discoverers/
│   └── link_text.py       # Discovers current pages to monitor
│
├── extractors/
│   └── ...                # Source-specific HTML extraction logic
│
├── monitors/
│   └── page_monitor.py    # Fetches pages and runs extractors
│
├── trackers/
│   ├── change_detector.py # Detects changes against snapshots
│   └── history.py         # Stores historical observations
│
├── storage/
│   ├── snapshots.json     # Latest known state
│   └── history/           # Historical monitoring data
│
├── tests/                 # Automated tests
│
├── config.py              # Monitor configuration
└── main.py                # Workflow orchestration
```

## How it works

For each configured monitor:

1. Discover the current page URL.
2. Retrieve and parse the page content.
3. Run configured extractors.
4. Store the latest observation in history.
5. Compare against the previous snapshot.
6. Send notifications when configured conditions are met.
7. Update stored state.

## Configuration

Monitors are defined through configuration rather than hard-coded workflows.

Each monitor specifies:

* a name and identifier
* how to locate the page
* which extractors to run
* how extracted information should be tracked

This allows new monitoring targets to be added without changing the core workflow.

## Running locally

### Install dependencies

Radar uses `uv` for dependency management.

```bash
uv sync
```

### Run the monitor

```bash
uv run python main.py
```

### Run tests

```bash
uv run pytest
```

## GitHub Actions

Two workflows are included.

### CI

Runs automatically on:

* pushes to `main`
* pull requests
* manual workflow runs

The CI workflow installs dependencies and runs the test suite.

### Radar

Runs automatically on a scheduled basis and can also be triggered manually.

The workflow:

* installs dependencies
* executes the monitoring pipeline
* updates stored tracking data
* commits updated state

## Environment variables

Notification credentials are loaded from environment variables:

```text
PUSHOVER_USER_KEY
PUSHOVER_API_TOKEN
```

Secrets should be stored securely using GitHub Actions secrets or a local environment file.

## Testing

The project includes automated tests covering:

* HTML extraction logic
* change detection behaviour
* notification formatting
* edge cases where expected information is missing

The test suite helps prevent changes to extraction logic from silently breaking monitoring.

## Future ideas

Potential improvements:

* Add dashboards for historical trends.
* Support additional notification providers.
* Add monitoring failure alerts.
* Introduce configurable alert rules.
* Store larger datasets in a database.
* Expand support for different page structures.

## Why "Radar"?

Radar is designed to quietly monitor information in the background and surface changes that matter, rather than requiring repeated manual checks.
