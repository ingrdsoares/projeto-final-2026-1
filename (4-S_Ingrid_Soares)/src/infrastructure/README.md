# Infrastructure Deployment Guide

This directory contains the scripts and configurations necessary to set up the Purple Team Lab.

## 🚀 Components

1.  **Wazuh (SIEM/XDR):** Deployed via Docker Compose. Provides centralized log management, integrity monitoring, and alert generation.
2.  **Sysmon for Linux:** Installed on the target host. Provides deep visibility into process creation, network connections, and file changes.
3.  **Atomic Red Team:** Installed on the target host. Used to simulate TTPs.

## 🛠 Setup Process

### 1. Deploy Wazuh
```bash
cd src/infrastructure
docker-compose up -d
```
Wait for the containers to start and access the dashboard at `https://localhost:5608`.

### 2. Install Telemetry & Simulation Tools
Run the setup script on the machine you wish to monitor/attack:
```bash
chmod +x install_telemetry.sh
sudo ./install_telemetry.sh
```

### 3. Link Agent to Manager
Follow the Wazuh dashboard instructions to deploy the agent on the target machine and link it to the manager.
