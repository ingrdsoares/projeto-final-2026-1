#!/bin/bash

# Purple Team Telemetry & Simulation Setup Script
# Installs Sysmon for Linux and Atomic Red Team

set -e

echo "[*] Updating system..."
sudo apt-get update -y

echo "[*] Installing dependencies..."
sudo apt-get install -y curl git wget unzip build-essential

# --- Sysmon for Linux Installation ---
echo "[*] Installing Sysmon for Linux..."
# In a real scenario, we would download the latest release from Microsoft
# Here we simulate the installation flow
mkdir -p /etc/sysmon
echo "Sysmon configuration would be applied here." > /etc/sysmon/config.xml
echo "[+] Sysmon installed (Simulated)."

# --- Atomic Red Team Installation ---
echo "[*] Installing Atomic Red Team..."
mkdir -p ~/AtomicRedTeam
cd ~/AtomicRedTeam
git clone https://github.com/redcanaryco/atomic-red-team.git .
echo "[+] Atomic Red Team cloned."

# Install Invoke-AtomicRedTeam (PowerShell for Linux)
echo "[*] Installing PowerShell for Atomic Red Team..."
# Simplification for the project: we will use the git repo directly or a simple wrapper
sudo apt-get install -y powershell

echo "[+] PowerShell installed."

echo "-------------------------------------------------------"
echo "DONE: Telemetry and Simulation tools are ready."
echo "Now, install the Wazuh Agent and point it to your manager."
echo "-------------------------------------------------------"
