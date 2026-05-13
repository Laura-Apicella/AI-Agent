# ⚡ Energy Assistant Agent

An AI-powered customer service assistant for an electricity provider, built with **Google ADK** and **Gemini**. The agent authenticates customers and helps them consult contracts, bills, and energy consumption data.

---

## 🎯 Project Overview

This project was developed as part of the **CESMA Master** at Università degli Studi di Roma Tor Vergata (May 2026), simulating a real-world AI consulting scenario.

The goal was to build a working prototype of a conversational AI assistant for an energy provider's customer service, presenting it to a non-technical client (the operations director) in a live demo.

---

## 🤖 What the Agent Can Do

| Feature | Description |
|---|---|
| 🔐 **Customer Authentication** | Verifies identity via tax code and email before exposing any data |
| 📄 **Bill Retrieval** | Fetches the latest bill with all details (period, kWh, amount, due date) |
| 📊 **Consumption Analysis** | Monthly breakdown, average consumption, comparison vs. historical data |
| ℹ️ **Contract Info** | Active offer, time-of-use pricing (F1/F2/F3), fixed monthly fee |
| 📋 **Full Contract Summary** | Complete overview of contract + latest bill in one call |
| 📈 **Consumption Chart** | Generates a PNG chart of monthly consumption trends |

---

## 🗂️ Repository Structure

```
AI-Agent/
├── README.md                  ← you are here
├── .gitignore
└── agent_energy/
    └── agent.py               ← core agent implementation
```

### 👉 Core Implementation → [`agent_energy/agent.py`](agent_energy/agent.py)

The agent is built as a single-file implementation with:
- **6 tools** connected to a SQLite database (200 customers, 600 bills, 1200 meter readings)
- **Authentication gate** — no data is returned without prior identity verification
- **Matplotlib integration** for chart generation
- **Prompt instructions** in Italian (the agent's target language)

---

## 🛠️ Tech Stack

- **Python 3.12**
- **Google ADK** — agent framework
- **Gemini** — underlying LLM
- **SQLite** — customer database
- **Matplotlib** — consumption charts

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/Laura-Apicella/AI-Agent.git
cd AI-Agent

# 2. Create virtual environment and install dependencies
uv venv
.venv\Scripts\activate      # Windows
uv sync

# 3. Add your API key
# Create a .env file in the root with your Gemini API key

# 4. Generate the dataset
uv run python genera_dataset_energy.py

# 5. Start the agent
uv run adk web
```

Open `http://localhost:8000` and select **`agent_energy`**.

---

## 💬 Example Interaction

```
User:   Hi, I'd like to check my latest bill.
Agent:  Sure! Please provide your tax code and email to proceed.

User:   Tax code: RSSMRA80A01H501Z — Email: mario.rossi@email.it
Agent:  Identity verified. ✅

        Here is your latest bill:
        • Bill number: 2024-0042
        • Period: 01/11/2024 – 31/12/2024
        • Total kWh: 312
        • Amount due: €87.40
        • Due date: 31/01/2025
```

---

## 📌 Notes

- The agent always responds in **Italian** (target user language)
- No personal data is ever returned before successful authentication
- The `.env` file and database are excluded from this repository for privacy reasons