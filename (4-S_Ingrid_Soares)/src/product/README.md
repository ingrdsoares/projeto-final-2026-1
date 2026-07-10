# Dashboard Deployment Guide

This directory contains the Streamlit frontend for the Purple Team AI Orchestrator.

## 🚀 How to Run

1. Ensure the API is running:
```bash
uvicorn src.api.main:app --reload --port 8000
```

2. Install requirements:
```bash
pip install streamlit requests pandas
```

3. Start the dashboard:
```bash
streamlit run src/product/app.py
```

## 🛠 Features
- **MITRE Heatmap:** Real-time visualization of security coverage.
- **Orchestration Trigger:** One-click execution of the full validation cycle.
- **Manual Simulation:** Trigger specific TTPs and verify their detection status.
