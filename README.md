# Hybrid Support Ticket Triage System

An intelligent support system that uses a **Hybrid Architecture**:

- A generative LLM (Nemotron free model) writes a draft reply
- **Jev** (TypeSafe System One model) evaluates the draft for tone, risk, policy compliance, and safety
- The system decides whether to **Auto-Send**, **Escalate**, or **Send for Human Review**

Built as a learning + portfolio project focused on real-world AI decision systems.

---

## Features

- Hybrid LLM + Decision Model architecture
- Confidence-based routing
- Structured logging of every decision
- Evaluation framework with test tickets
- Clean Streamlit web interface
- Free models only (no cost during development)

---

## Tech Stack

- **Decision Model**: Jev (via OpenRouter)
- **Generative Model**: `nvidia/nemotron-3-super-120b-a12b:free`
- **Backend**: Python
- **UI**: Streamlit
- **Logging**: JSON
- **Evaluation**: Custom test suite

---

## How it works

1. User pastes a customer ticket
2. LLM generates a professional draft reply
3. Jev evaluates the draft on 4 criteria:
   - Tone quality
   - Safety to send
   - Risk of making the customer more upset
   - Policy safety
4. System applies thresholds and decides the action
5. Everything is logged for later analysis

---

## Project Structure
```
jev-ticket-triage/
├── triage.py              # Core logic (LLM + Jev + decision)
├── app.py                 # Streamlit web interface
├── evaluate.py            # Evaluation script
├── logs.json              # Decision logs
├── evaluation_results.json
├── .env                   # API key (not committed)
└── README.md

```
---

## Setup

1. Clone the repository
2. Create virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install typesafe-sdk openai python-dotenv streamlit
