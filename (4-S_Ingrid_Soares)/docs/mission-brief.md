# Mission Brief: Purple Team AI Orchestrator

## 1. Problem Definition
Modern Linux environments often suffer from a gap between the known threats (TTPs) and the actual detection capabilities of the installed security tools. Manual validation of security controls is time-consuming and often inconsistent.

**The Goal:** Build an AI-driven orchestrator that automates the "Attack -> Detect -> Remediate" cycle, using a feedback loop to improve security posture based on real-world simulations.

### Stakeholders
- **Security Engineers:** Need to validate that their detection rules actually work.
- **SOC Analysts:** Need clear alerts and a way to understand the "why" behind an attack.
- **System Administrators:** Need to apply mitigations without breaking production services.

### Metrics of Success
- **Business Metric:** Percentage of the selected MITRE ATT&CK matrix covered by validated detections.
- **Technical Metric:** Accuracy of the AI Agent in identifying the gap between a simulated attack and its corresponding alert in the SIEM.

---

## 2. Scope & Technical Approach

### The Cycle: Agent -> API -> Product

#### A. The Agent (The Brain)
An AI Agent (built with LangChain/Python) that orchestrates the following tools:
- **Atomic Red Team:** To execute specific TTPs.
- **Wazuh API:** To query alerts and logs.
- **Sigma Converter:** To propose new detection rules.

#### B. The API (The Contract)
A FastAPI layer that abstracts the complexity of the tools:
- `POST /simulate`: Triggers an attack.
- `GET /status`: Checks if an attack was detected.
- `POST /remediate`: Deploys a new rule to the SIEM.

#### C. The Product (The Interface)
A Streamlit Dashboard providing:
- **MITRE Heatmap:** Visual representation of security coverage (Green = Detected, Red = Blind spot).
- **Execution Log:** Real-time trace of the Agent's reasoning.
- **One-Click Hardening:** Button to trigger the Agent's remediation flow.

---

## 3. Selected TTPs (Linux focus)
| ID | Tactic | Technique | Goal |
| :--- | :--- | :--- | :--- |
| T1543.002 | Persistence | Systemd Service | Create a persistent backdoor via systemd. |
| T1548.001 | Privilege Escalation | Sudo Abuse | Gain root access via sudo misconfiguration. |
| T1070.004 | Defense Evasion | Log File Deletion | Clear `/var/log` to hide tracks. |
| T1082 | Discovery | System Info Discovery | Reconnaissance of OS and kernel versions. |
| T1041 | Exfiltration | Exfiltration Over C2 | Send data to an external server via HTTP. |

---

## 4. Tech Stack
- **Simulations:** Atomic Red Team.
- **Detection/SIEM:** Wazuh + Sysmon for Linux.
- **Intelligence:** Python, LangChain, OpenAI/Gemini API.
- **Interface:** FastAPI + Streamlit.
- **Infrastructure:** Docker / Ansible.
