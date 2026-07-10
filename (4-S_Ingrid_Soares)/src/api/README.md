# API Deployment Guide

This directory contains the FastAPI implementation that exposes the Purple Team AI Agent.

## 🚀 Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Health check. |
| `POST` | `/simulate` | Trigger an attack via TTP ID. |
| `GET` | `/check/{ttp_id}` | Check if the attack was detected. |
| `POST` | `/validate-all` | Run the complete orchestration cycle. |
| `GET` | `/coverage` | Retrieve the current coverage map. |

## 🛠 Running the API

1. Install dependencies:
```bash
pip install fastapi uvicorn
```

2. Start the server:
```bash
uvicorn src.api.main:app --reload --port 8000
```

3. Access the interactive documentation at `http://localhost:8000/docs`.
