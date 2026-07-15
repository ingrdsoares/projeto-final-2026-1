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
Refer to [mission-brief.md](docs/mission-brief.md) for full scope and objectives.
