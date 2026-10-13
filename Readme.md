<div align="center">

# 💧 HYDRAFLOW AI
### *Autonomous Hydration Agent & Real-Time Wellness Tracker*

[![Python](https://img.shields.io/badge/Python-3.10+-38BDF8?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Glassmorphic_UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google_GenAI-Agentic_AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![SQLite3](https://img.shields.io/badge/SQLite3-Database-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)

<p align="center">
  <b>HydraFlow AI</b> ek intelligent full-stack hydration management system hai jo har sip ko track karta hai, logs ko persistent SQLite database me store karta hai, aur Google Gemini AI ke through real-time personalized hydration coach feedback deliver karta hai.
</p>

[✨ Live Features](#-key-features) • [⚡ Quick Setup](#-quick-start) • [📡 API Docs](#-rest-api-endpoints) • [🛠️ Architecture](#-system-architecture)

---

</div>

## 🌌 System Architecture

HydraFlow AI ek decoupled **3-Tier Full-Stack Microservice** architecture follow karta hai:

```ascii
 ╔═══════════════════════════════════════════════════════════════════╗
 ║                     STREAMLIT DASHBOARD UI                        ║
 ║      (Glassmorphism • Fluid Animations • Interactive Charts)      ║
 ╚═════════════════════════════════╤═════════════════════════════════╝
                                   │ HTTP POST / GET (JSON)
                                   ▼
 ╔═══════════════════════════════════════════════════════════════════╗
 ║                      FASTAPI BACKEND ENGINE                       ║
 ║         (Endpoint Routing • Pydantic Schema Validation)           ║
 ╚═════════════════════════╤═════════════════════════╤═══════════════╝
                           │                         │
                           ▼                         ▼
            ┌─────────────────────────────┐   ┌─────────────────────────────┐
            │       SQLITE DATABASE       │   │       GOOGLE GEMINI AI      │
            │   (water_tracker.db Store)  │   │  (HydraFlow Coach Feedback) │
            └─────────────────────────────┘   └─────────────────────────────┘

Hydra flow water tracker/
├── 📁 src/
│   ├── 📄 __init__.py
│   ├── 📄 agent.py            # Gemini Client & WaterIntakeAgent Class
│   ├── 📄 api.py              # FastAPI Application & REST Routes
│   ├── 📄 database.py         # SQLite Tables & Data Insertion Methods
│   └── 📄 app_logging.py      # Structured Log Formatter
│
├── 📄 .env                    # Secret API Keys & Config
├── 📄 app.log                 # Automated System Run Logs
├── 📄 dashboard.py            # Streamlit Frontend Web App
├── 📄 requirement.txt         # Project Dependencies
├── 📄 water_tracker.db        # Production SQLite Database
└── 📄 README.md               # Project Documentation

Key Engineering Bugs Resolved During Development:

Google GenAI Deprecation & Model 404s:
Issue: Legacy models gemini-1.5-flash / gemini-2.0-flash par 404 Not Found error.
Fix: Latest Google GenAI SDK adopt kiya gaya aur dynamic fallback pool (gemma-4-26b-a4b-it aur gemini-3.8-flash) implement kiya.

Conda Missing CA Certificate Handshake:
Issue: Windows Conda me FileNotFoundError: cafile SSL failure.
Fix: Runtime par certifi.where() path ko SSL_CERT_FILE environment variable me inject kiya gaya.

HTTP Client Connection Timeout:
Issue: LLM processing ke dauran Read timed out (timeout=20) drop.
Fix: Client HTTP requests timeout ko badhakar 60 seconds kiya gaya aur server-side caching apply ki gayi.

👨‍💻 Author & Contributions
Built with ❤️ by Anuj Mishra.
Contributions, pull requests, and suggestions are welcome!