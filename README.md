# System Resource Dashboard 🖥️

A simple Python-based system monitoring tool with a web interface.
This project is a mini-project that will be further developed into a comprehensive system administration portfolio.

## Features (Pages)
1. **Overview:** Real-time monitoring of CPU and RAM usage.
2. **Processes:** View the top running processes sorted by memory consumption.
3. **Disk & Network:** Track storage capacity and network I/O statistics.

## How to Run

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit application:
   ```bash
   streamlit run dashboard.py
   ```

## Live Demos

![System Monitor Overview](docs/_static/demo_screenshot.png)

> Open the Streamlit dashboard and use the Flask API to manage processes while monitoring system health.

## Features

- **Real-time system monitoring**: CPU, RAM, boot time, disk usage, and network I/O.
- **Process management**: Terminate processes via an authenticated backend endpoint.
- **Swagger API docs**: Interactive OpenAPI explorer for the Flask API using Flasgger.
- **Sphinx-generated docs**: HTML documentation generated from Python docstrings.

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the backend server:
   ```bash
   python run.py
   ```
4. In a second terminal, start the dashboard:
   ```bash
   streamlit run dashboard.py
   ```

## API Documentation

- Swagger UI: `http://127.0.0.1:5000/apidocs/`

Available API endpoints:

- `GET /api/cpu`
- `GET /api/ram`
- `GET /api/boot-time`
- `GET /api/disk?path=/`
- `GET /api/network`
- `GET /api/processes?limit=20`
- `POST /api/process/kill`

## Generate Documentation

Create or refresh the API docs from the `app/` package:

```bash
cd docs
sphinx-apidoc -o source ../app
```

Build the HTML docs:

```bash
cd docs
make html
```

Then open `docs/_build/html/index.html` in your browser.

## Project Structure

- `app/` — Flask package containing backend initialization and API routes.
- `dashboard.py` — Streamlit UI and dashboard presentation.
- `run.py` — Flask app entrypoint.
- `server.py` — Compatibility wrapper for the Flask package.
- `system_monitor.py` — Compatibility wrapper importing `app.models`.
- `docs/` — Sphinx documentation configuration and source.

## Notes for GitHub Pages

This repository can publish the generated documentation via GitHub Pages from the `docs/_build/html` folder or the `docs/` source directory.

## Development

This portfolio-ready project now includes source-level documentation comments and a Swagger-enabled backend, making it easy to extend and showcase to employers or contributors.
