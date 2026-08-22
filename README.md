# Radar 📡

An automated web monitoring system that tracks pages for changes, extracts structured information, stores historical observations, and sends notifications when important updates are detected.

Radar is designed as a lightweight, configurable monitoring pipeline that can be adapted to different websites and information sources.

## Live Dashboard

🐕 **[Scrumbles Turkey 2kg Price Monitor](https://scrumblesturkey2kg.streamlit.app/)**

A live Streamlit dashboard visualising historical price data collected by Radar for Scrumbles Turkey Adult & Senior Dry Dog Food 2kg across selected UK retailers.

The dashboard includes:

* Current retailer prices
* Historical price trends
* Promotion and availability information
* Retailer data-quality and monitoring health
* Price competitiveness analysis
* Date-range filtering

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

  * Records monitoring observations as timestamped JSON Lines (`.jsonl`) data.
  * Maintains a history of observations for future analysis and visualisation.

* 🔔 **Notifications**

  * Sends alerts when monitored content changes.
  * Supports recurring notifications for selected conditions, such as active promotions or announcements.

* 📊 **Data visualisation**

  * Historical monitoring data can be visualised through dashboards built on top of the stored observations.
  * The current Scrumbles dashboard uses Streamlit and Plotly.

* ⚙️ **Automated execution**

  * Runs on scheduled GitHub Actions workflows.
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
├── scrumbles/
│   └── ...                # Scrumbles price monitoring
│
├── storage/
│   ├── snapshots.json     # Latest known state
│   └── history/           # Historical monitoring data
│
├── tests/                 # Automated tests
│
├── dashboard.py           # Streamlit data visualisation
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
8. Where appropriate, expose historical observations for analysis and visualisation.

## Example: Scrumbles Price Monitoring

Radar currently includes a daily price-monitoring workflow for Scrumbles Turkey Adult & Senior Dry Dog Food 2kg.

The monitor collects structured price observations from selected UK retailers and stores them as JSON Lines data. The historical dataset is then used by the Streamlit dashboard to analyse price movements, promotions, availability, data quality, and retailer competitiveness over time.

This provides an example of how Radar can be used not only to detect changes, but also to build a historical dataset from repeated observations.

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

### Run the dashboard

```bash
uv run streamlit run dashboard.py
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

* Add monitoring failure alerts.
* Introduce configurable alert rules.
* Support additional notification providers.
* Store larger datasets in a database.
* Expand support for different page structures.
* Add additional dashboards and analytical views for monitored datasets.

## Why "Radar"?

Radar is designed to quietly monitor information in the background and surface changes that matter, rather than requiring repeated manual checks.
