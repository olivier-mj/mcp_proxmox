---
layout: default
title: Home
---

# Proxmox MCP Server 🤖

[![Docker Image CI](https://github.com/olivier-mj/mcp_proxmox/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/olivier-mj/mcp_proxmox/actions/workflows/docker-publish.yml)

**Manage your Proxmox VE infrastructure using AI.**
*Pilotez votre infrastructure Proxmox VE grâce à l'IA.*

This MCP (Model Context Protocol) server allows LLMs (like Claude, Gemini, etc.) to securely monitor and control your Proxmox nodes, VMs, and containers.

## 🌟 Key Features

- 📊 **Advanced Monitoring**: View CPU/RAM, storage, and internal IPs.
- ⚡ **Infrastructure Control**: Start, Stop, Reboot, and **Clone** machines.
- 🛡️ **Data Protection**: Manage **Snapshots** and **Backups** (vzdump).
- 🔗 **Direct Access**: Generate **NoVNC Console** links.
- 🔒 **Safe & Secure**: API Token auth, isolated Docker environment, no destructive delete.

## 📚 Documentation

Please select your language / Veuillez choisir votre langue :

*   👉 [**Documentation en Français**](./README_fr.html)
*   👉 [**English Documentation**](./README_en.html)

---

## 🚀 Quick Start

```bash
docker run -d \
  -e PROXMOX_URL=https://your-ip:8006 \
  -e PROXMOX_USER=root@pam \
  -e PROXMOX_TOKEN_ID=mcp \
  -e PROXMOX_TOKEN_SECRET=your-secret \
  oliviermj/mcp_proxmox:latest
```

[View on GitHub](https://github.com/olivier-mj/mcp_proxmox)