# Radar

Radar is a lightweight web monitoring tool that detects changes on selected web pages, extracts structured information, and sends notifications when meaningful updates occur.

It is designed to automate the repetitive task of checking websites for changes, while keeping the monitoring logic modular and easy to extend.

## Features

* 🔎 Discover relevant pages from configured sources
* 🧩 Extract structured information from web content
* 🔄 Detect changes against previous results
* 🔔 Send notifications when updates are detected
* ⏰ Run automatically on a schedule using GitHub Actions
* 💾 Persist state between runs using version-controlled snapshots

## How It Works

Radar follows a simple pipeline:

```
Website
   |
   v
Discover page
   |
   v
Extract information
   |
   v
Compare with previous snapshot
   |
   +---- No change
   |
   +---- Change detected
             |
             v
       Send notification
```

Each monitored source is configured with:

* How to find the relevant page
* Which extractors should run
* Where historical state should be stored

## Project Structure

```
radar/
│
├── alerts/          # Notification formatting and delivery
├── discoverers/     # Finding relevant pages
├── extractors/      # Extracting structured data
├── monitors/        # Monitoring logic
├── trackers/        # Change detection and history management
├── storage/         # Persisted snapshots and history
├── tests/           # Automated tests
│
├── main.py
├── config.py
├── pyproject.toml
└── README.md
```

## Running Locally

Install dependencies:

```bash
uv sync
```

Create a `.env` file containing required environment variables:

```
PUSHOVER_API_TOKEN=your_token
PUSHOVER_USER_KEY=your_user_key
```

Run Radar:

```bash
uv run python main.py
```

## Testing

Tests are written using `pytest`.

Run the test suite:

```bash
uv run pytest
```

The tests cover individual components such as:

* Data extraction
* Change detection
* Notification formatting

## Automation

Radar runs automatically through GitHub Actions.

The workflow:

1. Starts on a scheduled basis
2. Installs dependencies
3. Runs the monitoring process
4. Updates stored snapshots
5. Commits changes back to the repository

This allows Radar to operate continuously without requiring a local machine to be running.

## Design Approach

Radar separates responsibilities into small, independent components:

* **Discoverers** find pages
* **Extractors** convert HTML into structured data
* **Trackers** determine whether information has changed
* **Alerts** handle notification delivery

This makes it possible to add new monitors without changing the core application logic.

## Future Improvements

Potential future enhancements include:

* Adding more notification channels
* Improving configuration management
* Adding richer historical reporting
* Expanding automated testing coverage
* Supporting additional data sources
