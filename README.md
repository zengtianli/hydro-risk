# ⚠️ Hydro Risk -- Risk Map Data Processing

[![GitHub stars](https://img.shields.io/github/stars/zengtianli/hydro-risk)](https://github.com/zengtianli/hydro-risk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-FF4B4B.svg)](https://streamlit.io)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-hydro--risk.tianlizeng.cloud-brightgreen)](https://hydro-risk.tianlizeng.cloud)

Risk map data table auto-filling ETL pipeline -- GeoJSON to Excel in 3 phases.

![screenshot](docs/screenshot.png)

## Features

- **3-phase ETL pipeline** -- database building → forecast → risk analysis
- **14 processing scripts** -- each handles a specific data table
- **GeoJSON → Excel** -- automatic spatial data extraction and table filling
- **Code normalization** -- automatic encoding, river/basin code generation
- **Web + CLI** -- Streamlit interface for interactive use, CLI for scripted execution
- **Processing reports** -- detailed logs with statistics and validation results

## Quick Start

```bash
git clone https://github.com/zengtianli/hydro-risk.git
cd hydro-risk
pip install -r requirements.txt
streamlit run app.py
```

## Pipeline

| Phase | Scripts | Input | Output |
|-------|---------|-------|--------|
| Database Building | 1.1-1.4 | GeoJSON (protection areas, dikes, rivers) + CSV mappings | database_sx.xlsx |
| Forecast | 2.1 | GeoJSON (cross-sections with mileage) | forecast_sx.xlsx |
| Risk Analysis | 3.01-3.09 | GeoJSON + CSV + database_sx.xlsx | risk_sx.xlsx (18+ sheets) |

## CLI Usage

```bash
# Phase 1: Build database
python 1.1_database_protection_area.py
python 1.2_database_dike_section.py
python 1.3_database_dike.py
python 1.4_database_river_centerline.py

# Phase 2: Forecast
python 2.1_forecast_cross_section.py

# Phase 3: Risk analysis (with arguments)
python 3.01_risk_protection_info.py -g input/env.geojson -e output/risk_sx.xlsx
```

## Deploy (VPS)

```bash
git clone https://github.com/zengtianli/hydro-risk.git
cd hydro-risk
pip install -r requirements.txt
nohup streamlit run app.py --server.port 8519 --server.headless true &
```

## Hydro Toolkit Plugin

This project is a plugin for [Hydro Toolkit](https://github.com/zengtianli/hydro-toolkit) and can also run standalone. Install it in the Toolkit by pasting this repo URL in the Plugin Manager. You can also **[try it online](https://hydro-risk.tianlizeng.cloud)** -- no install needed.

## License

MIT
