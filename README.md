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