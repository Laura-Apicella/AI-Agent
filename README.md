---
marp: true
theme: default
paginate: true
backgroundColor: white
style: |
  /* ── Base ───────────────────────────────────────── */
  section {
    font-family: 'Segoe UI', 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif;
    padding: 2em 3em;
  }

  /* ── Cover ─────────────────────────────────────── */
  section.cover {
    text-align: center;
  }

  /* ── Divider slide ──────────────────────────────── */
  section.divider {
    background: #006699;
    text-align: center;
  }
  section.divider h3 { color: rgba(255,255,255,0.5); font-size: 0.95em; font-weight: 400; letter-spacing: 0.25em; text-transform: uppercase; }
  section.divider h1 { color: white; font-size: 2.6em; }
  section.divider h2 { color: rgba(255,255,255,0.75); font-size: 1.2em; font-weight: 300; }

  /* ── Demo slide ─────────────────────────────────── */
  section.demo {
    background: #0d3349;
    text-align: center;
  }
  section.demo h3 { color: rgba(255,255,255,0.5); font-size: 0.95em; font-weight: 400; letter-spacing: 0.25em; text-transform: uppercase; }
  section.demo h1 { color: #64d2ff; font-size: 2.2em; }
  section.demo h2 { color: rgba(255,255,255,0.7); font-size: 1.1em; font-weight: 300; }
  section.demo pre { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); }

  /* ── Typography ─────────────────────────────────── */
  h1 { color: #006699; font-size: 1.9em; margin-bottom: 0.3em; text-align: center; }
  h2 { color: #2e7d32; font-size: 1.2em; font-weight: 400; margin-top: 0; margin-bottom: 0.8em; text-align: center; }
  h3 { color: #444; font-size: 1.05em; margin-bottom: 0.5em; margin-top: 1.4em; text-align: center; }
  p  { margin: 0.4em 0; text-align: center; }
  ul { margin-top: 0.4em; line-height: 1.85; }
  li { margin-bottom: 0.15em; text-align: left; }
  li p { text-align: left; }

  /* ── Code ───────────────────────────────────────── */
  code { background: #f0f4f8; color: #c0392b; padding: 0.1em 0.4em; border-radius: 4px; font-size: 0.88em; }
  pre  { background: #f6f8fa; color: #24292e; border: 1px solid #d0d7de; border-radius: 10px; padding: 0.85em 1.2em; font-size: 0.8em; line-height: 1.55; }
  pre code { background: none; color: inherit; padding: 0; }
  img { display: block; margin: 0 auto; max-width: 100%; }
  li img, h1 img, h2 img, h3 img, td img, th img, p img:not(:only-child) { display: inline; margin: 0; vertical-align: middle; }

  /* ── Tables ─────────────────────────────────────── */
  table { border-collapse: collapse; font-size: 0.88em; margin: 0.6em auto; }
  th { background: #006699; color: white; padding: 0.45em 0.9em; text-align: center; }
  td { border: 1px solid #ddd; padding: 0.45em 0.9em; text-align: center; }
  tr:nth-child(even) td { background: #f5f9fc; }

  /* ── Callout boxes ──────────────────────────────── */
  .highlight-box { background: #e8f5e9; border-left: 4px solid #2e7d32; padding: 0.7em 1.1em; border-radius: 0 8px 8px 0; margin-top: 0.9em; font-size: 0.97em; }
  .warning-box   { background: #fff8e1; border-left: 4px solid #f9a825; padding: 0.7em 1.1em; border-radius: 0 8px 8px 0; margin-top: 0.9em; font-size: 0.93em; }
  .demo-box      { background: #e3f2fd; border-left: 4px solid #1565c0; padding: 0.7em 1.1em; border-radius: 0 8px 8px 0; margin-top: 0.9em; font-size: 0.93em; }

  /* ── Two-column layout ──────────────────────────── */
  .two-col { display: flex; gap: 2em; width: 100%; align-items: flex-start; margin-top: 0.5em; }
  .col { flex: 1; }

  /* ── Logos ──────────────────────────────────────── */
  .logos-bottom { position: absolute; bottom: 1.2em; left: 0; width: 100%; display: flex; justify-content: space-between; padding: 0 2em; box-sizing: border-box; }
  .logos-bottom img { height: 55px; }
---

<!-- _class: cover -->
<!-- _paginate: false -->

# Use Case
## Assistente Clienti Energy

<br>

**Master CESMA · Pomeriggio**

Università degli Studi di Roma Tor Vergata · *12 Maggio 2026*

<div class="logos-bottom">
  <img src="https://www.cybertrends.it/wp-content/uploads/2021/01/wYS3XoJ1_400x400.jpg" />
  <img src="https://master-cesma.it/layout/economia/img/ateneo-logo/logo-tor-vergata-en.svg" />
</div>

---

# Lo scenario

Siete un team di consulenti AI assunti da un fornitore di energia elettrica.

Il cliente — il **direttore operations** — non conosce l'AI e vuole capire se vale l'investimento.

<br>

<div class="highlight-box">
Il vostro compito: costruire un prototipo funzionante e presentarlo al cliente in modo che lo capisca. Niente gergo tecnico nella demo — parlate di funzionalità, non di codice.
</div>

---

# Regole del pomeriggio

<br>

- 👥 **2 team** — formate da soli, equilibrate le competenze
- ⏱️ **1 ora e mezza** per costruire il prototipo
- 🎤 **Demo al cliente** — ~20/30 minuti per team

<br>

<div class="demo-box">
Nella demo fate vedere il sistema in azione, spiegate cosa fa in parole semplici e presentate tutto quello che avete costruito. Io farò domande come farebbe un cliente vero.
</div>

---

# Scaricate la repo

<br>

1. Vai su [gitlab.com/cesma/2026/cesma-use-case-2026](https://gitlab.com/cesma/2026/cesma-use-case-2026)
2. Click su **Code → Download ZIP**
3. Estrai lo ZIP in una cartella
4. Apri la cartella con VSCode

---

# Setup — Ambiente e dati

**1.** Crea il file `.env` nella root con la chiave fornita dal docente

**2.** Genera il dataset (DB + PDF bollette):

```bash
uv venv
.venv\Scripts\activate         # Windows
uv sync
uv run python genera_dataset_energy.py
```

<div class="warning-box">
⚠️ Su Windows, se il terminale blocca l'attivazione: <code>Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process</code>
</div>

---

# Setup — Avvio

```bash
uv run adk web
```

Apri `http://localhost:8000` → seleziona **`agent_energy`**

<div class="highlight-box">
Il comando ricarica automaticamente ad ogni modifica salvata.
</div>

---

# Cosa avete a disposizione

```
backend/
├── agent_energy/
│   ├── agent.py        ← punto di partenza, modificate questo
│   └── services/
│       └── llm.py      ← modello già configurato
├── db/
│   └── energy_dataset.db   ← 200 clienti, 600 bollette, 1.200 letture
├── pdfs/
│   └── *.pdf               ← bollette reali in PDF
├── docs/
│   └── *.pdf               ← manuali tecnici
└── README.md               ← schema completo del database
```

---

# Il database

| Tabella | Contenuto |
|---|---|
| `anagrafica` | Dati cliente: nome, CF, email, indirizzo, offerta |
| `offerte` | 5 tariffe con prezzi per fascia oraria (F1/F2/F3) |
| `consumi` | Letture mensili di energia per ogni contatore |
| `bollette` | Fatture bimestrali + percorso al PDF corrispondente |

<br>

Schema completo con esempi di query in `README.md`.

---

# Cosa deve saper fare (minimo)

### 🔐 Riconoscere il cliente
Verificare identità tramite codice fiscale ed email. Nessun dato senza autenticazione.

### 📄 Recuperare una bolletta
Trovare e restituire il PDF dell'ultima bolletta (o di un periodo specifico).

### 📊 Rispondere sui consumi
*"Quanto ho consumato questo bimestre?" · "Sto consumando più del solito?"*

### ℹ️ Informazioni sul contratto
Offerta attiva, fasce orarie, importi, date di scadenza.

---

# Cosa potete aggiungere — parte 1

### 📚 Risposte dalla documentazione (RAG)
L'assistente risponde a domande tecniche attingendo ai manuali in `docs/`.
Provate a usare un **modello di embedding in locale** (es. `nomic-embed-text` via Ollama).

### 📈 Grafici dei consumi
Andamento mese per mese direttamente in chat.
→ [Riferimento ADK + matplotlib](https://github.com/google/adk-python/issues/2283)

### 🎫 Segnalazione guasto
Il cliente apre un ticket in chat — salvato su DB con timestamp e stato.

---

# Cosa potete aggiungere — parte 2

### 📧 Conferma via email
Email automatica dopo ticket aperto o bolletta inviata.

### 🔌 Integrazioni esterne (MCP)
Connessione a strumenti e API tramite protocollo MCP.
→ [MCP Toolbox for Databases](https://github.com/googleapis/mcp-toolbox)

### ✨ Qualsiasi altra cosa
Carta bianca — se ha senso per il cliente, fatelo.

---

# Consigli pratici

<br>

- 🤝 **Dividetevi le funzionalità** — non lavorate tutti sullo stesso file
- 🤖 **Usate l'AI anche per leggere** — fatevi spiegare la documentazione, analizzare il codice, proporre architetture
- ✅ **Meglio poco e funzionante** — una funzionalità che funziona vale più di tre che si rompono nella demo

<div class="highlight-box">
Il cliente non sa cosa è un agent. Sa se il sistema funziona o no.
</div>

---

<!-- _class: cover -->
<!-- _paginate: false -->

# Via 🚀

<br>

**1 ora e mezza. Nessun limite.**

Il materiale della mattina è il vostro riferimento.

*Buona fortuna.*

<div class="logos-bottom">
  <img src="https://www.cybertrends.it/wp-content/uploads/2021/01/wYS3XoJ1_400x400.jpg" />
  <img src="https://master-cesma.it/layout/economia/img/ateneo-logo/logo-tor-vergata-en.svg" />
</div>
