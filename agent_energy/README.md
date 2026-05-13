# sequential_agent — Pipeline sequenziale in Google ADK

## Avvio

```bash
uv run adk web
```

## Come funziona

Pipeline in due step:

1. **`estrattore`** — classifica la richiesta in JSON: `categoria`, `urgenza`, `sintesi`. Salva in `state["analisi_richiesta"]`.
2. **`gestore`** — legge `{analisi_richiesta}` dallo State e genera una risposta professionale.

Il secondo agente non può partire finché il primo non ha scritto nello State. Questo è il valore di `SequentialAgent`.

Nel pannello **State** vedrai `analisi_richiesta` aggiornarsi ad ogni turn.
Nel pannello **Trace** vedrai i due agenti eseguiti in sequenza.

---

## Domande di test

### 1. Problema tecnico urgente
> "Il mio router non si connette a Internet da stamattina, ho un meeting importante tra un'ora."

`estrattore` classifica: `categoria: "tecnico"`, `urgenza: "alta"`.
`gestore` risponde sottolineando la gestione prioritaria.

### 2. Domanda su fatturazione
> "Ho ricevuto una fattura più alta del solito, non capisco le voci extra."

`categoria: "fatturazione"`, `urgenza: "media"`.
`gestore` spiega le possibili voci e come contestarle.

### 3. Richiesta commerciale
> "Vorrei capire se conviene passare a un piano con più Giga per tutta la famiglia."

`categoria: "commerciale"`, `urgenza: "bassa"`.
`gestore` suggerisce opzioni senza pressione.

### 4. Richiesta generica
> "Quali sono gli orari del vostro servizio clienti?"

`categoria: "altro"`, `urgenza: "bassa"`.
Dimostra che la pipeline funziona anche su richieste semplici.

### 5. Verifica dello State
Dopo più domande: apri il pannello **State** e verifica che `analisi_richiesta` contenga l'analisi dell'ultimo turn. Dimostra che ogni step scrive nello State e il successivo lo legge.
