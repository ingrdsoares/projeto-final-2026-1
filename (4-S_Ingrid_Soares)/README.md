# Purple Team AI Orchestrator

An AI-driven system to automate the simulation and detection of Linux TTPs, bridging the gap between Red and Blue teams.

## 🚀 Architecture: Agent -> API -> Product

- **Agent:** AI core using LangChain to orchestrate attacks (Atomic Red Team) and detections (Wazuh).
- **API:** FastAPI backend for controlling simulations and monitoring alerts.
- **Product:** Streamlit dashboard with a MITRE ATT&CK heatmap.

## 🛠 Tech Stack
- **Red Team:** Atomic Red Team.
- **Blue Team:** Wazuh, Sysmon for Linux, Sigma Rules.
- **Orchestration:** Python, FastAPI, LangChain.
- **UI:** Streamlit.

## 📂 Project Structure
- `/src/agent`: AI reasoning and tool integration.
- `/src/api`: API endpoints.
- `/src/product`: Dashboard implementation.
- `/src/infrastructure`: Deployment scripts for Wazuh/Sysmon.
- `/attacks`: Custom attack configurations.
- `/detections`: Sigma and Wazuh rules.
- `/docs`: Architecture and Mission Brief.

## 📈 TTPs Covered
- Persistence (Systemd)
- Privilege Escalation (Sudo)
- Defense Evasion (Log deletion)
- Discovery (System info)
- Exfiltration (C2 Channel)

---

## 🌐 Live Demo & Video
- **API URL:** [https://fastapi-backend-production-7a41.up.railway.app](https://fastapi-backend-production-7a41.up.railway.app)
- **Dashboard URL:** [https://streamlit-dashboard-production-f577.up.railway.app](https://streamlit-dashboard-production-f577.up.railway.app)
- **Demo Video:** [Assista ao vídeo de demonstração](https://mega.nz/folder/Gqw0DTZQ#UmqMmBx3jEpW2x2dKOA1Vw)

## 🛠 Tech Stack
- **Red Team:** Atomic Red Team.
- **Blue Team:** Wazuh, Sysmon for Linux, Sigma Rules.
- **Orchestration:** Python, FastAPI, LangChain.
- **UI:** Streamlit.
- **CI/CD & Deploy:** GitHub Actions, Docker, Railway.

## 🚀 How to Run (Local)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/seu-usuario/projeto-final-2026-1.git
   cd projeto-final-2026-1/(4-S_Ingrid_Soares)
   ```

2. **Setup Infrastructure (Wazuh):**
   ```bash
   cd src/infrastructure
   docker compose up -d
   ```

3. **Run API and Dashboard:**
   Use the provided Dockerfiles or run directly:
   ```bash
   # API
   python -m uvicorn src.api.main:app --port 8000
   # Dashboard
   streamlit run src/product/app.py
   ```

## 🛤️ Railway Setup Guide (Fulfilling Point 1)

To get your public URL, follow these steps:

1. **Create a New Project** on [Railway.app](https://railway.app).
2. **Add Two Web Services:**
   - **Service 1 (API):**
     - Source: This repository.
     - Root Directory: `(4-S_Ingrid_Soares)`
     - Dockerfile: `src/infrastructure/Dockerfile.api`
   - **Service 2 (Dashboard):**
     - Source: This repository.
     - Root Directory: `(4-S_Ingrid_Soares)`
     - Dockerfile: `src/infrastructure/Dockerfile.dashboard`
3. **Configure Domains:** Railway will provide a public URL for each service (e.g., `purple-team-api.up.railway.app`).
4. **Update README:** Replace the placeholder URLs with your actual Railway domains.

## ⚙️ CI/CD Configuration
This project uses **GitHub Actions** for automated:
- **Linting:** Using `Ruff`.
- **Docker Build:** Images for API and Dashboard.
- **Deployment:** Automatic push to **Railway**.

*Note: To enable deployment, configure the following secrets in your GitHub repository:*
- `RAILWAY_TOKEN`
- `RAILWAY_PROJECT_ID`
- `RAILWAY_API_SERVICE_ID`
- `RAILWAY_DASHBOARD_SERVICE_ID`
