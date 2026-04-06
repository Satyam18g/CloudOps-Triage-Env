# CloudOps Triage Simulator 🚀

An agentic Reinforcement Learning (RL) environment built for the Scaler OpenEnv Hackathon.

## Overview
This project simulates a real-world CloudOps triage scenario. It provides a headless, API-driven environment where an LLM agent must act as an AI Site Reliability Engineer (SRE). The agent connects to the environment, reads real-time server logs and metrics, and must deduce the correct action to resolve the incident.

## Environment Tasks
The environment features three distinct difficulty levels with an automated grading and reward system:
* **Level 1 (Easy):** The agent must identify a deadlocked service and issue a `RESTART` command.
* **Level 2 (Medium):** The agent must identify severe resource exhaustion (99.9% CPU) and issue a `SCALE_UP` command.
* **Level 3 (Hard):** The agent must identify a crash loop caused by a bad code deployment and issue a `ROLLBACK` command.

## Tech Stack
* **Framework:** Python, FastAPI
* **Data Validation:** Pydantic
* **Containerization:** Docker
* **Hosting:** Hugging Face Spaces
* **Agent Testing:** OpenAI Python SDK

## How to Test Locally
If you want to run this environment on your own machine:
1. Clone the repository.
2. Build the Docker container: `docker build -t cloudops-env .`
3. Run the container: `docker run -p 7860:7860 cloudops-env`
4. Access the Swagger UI at: `http://localhost:7860/docs`
