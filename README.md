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
