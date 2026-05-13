
# Energy Dataset – Master CESMA

Dataset sintetico per uso didattico nel contesto di sistemi multi-agent e RAG su documenti energy.
Generato con dati fittizi italiani nel settore energia elettrica residenziale.

---

## Struttura del progetto

```
energy_dataset/
├── genera_dataset_energy.py   # Script di generazione
├── README.md                  # Questo file
├── db/
│   └── energy_dataset.db      # Database SQLite
└── pdfs/
    └── *.pdf                  # Bollette (una per record in bollette)
```

---

## Schema del database

### `anagrafica`
Contiene i dati anagrafici dei 50 clienti residenziali simulati.

| Colonna | Tipo | Descrizione |
|---|---|---|
| `id` | INTEGER PK | Identificativo univoco cliente |
| `nome` | TEXT | Nome del cliente |
| `cognome` | TEXT | Cognome del cliente |
| `codice_fiscale` | TEXT | Codice fiscale (simulato, univoco) |
| `indirizzo` | TEXT | Indirizzo di fornitura |
| `comune` | TEXT | Comune |
| `cap` | TEXT | CAP |
| `provincia` | TEXT | Sigla provincia |
| `email` | TEXT | Email di contatto |
| `telefono` | TEXT | Telefono di contatto |
| `pod` | TEXT | Point of Delivery – codice univoco del contatore (`IT001E...`) |
| `id_offerta` | INTEGER FK | Offerta sottoscritta → `offerte.id` |
| `data_attivazione` | TEXT | Data di attivazione della fornitura |

---

### `offerte`
Catalogo delle 5 tariffe energy disponibili, con prezzi per fascia oraria.

| Colonna | Tipo | Descrizione |
|---|---|---|
| `id` | INTEGER PK | Identificativo offerta |
| `nome` | TEXT | Nome commerciale (es. "Bioraria Smart") |
| `tipo` | TEXT | `monoraria` / `bioraria` / `trioraria` |
| `prezzo_f1` | REAL | Prezzo €/kWh fascia F1 (ore di punta) |
| `prezzo_f2` | REAL | Prezzo €/kWh fascia F2 (ore intermedie) |
| `prezzo_f3` | REAL | Prezzo €/kWh fascia F3 (ore fuori punta) |
| `quota_fissa_mensile` | REAL | Quota fissa mensile in € |
| `valida_dal` | TEXT | Data inizio validità offerta |
| `valida_al` | TEXT | Data fine validità offerta |

**Offerte disponibili:**

| ID | Nome | Tipo | F1 (€/kWh) | F2 (€/kWh) | F3 (€/kWh) | Quota fissa |
|---|---|---|---|---|---|---|
| 1 | Monoraria Base | monoraria | 0.2200 | 0.2200 | 0.2200 | 9.50 €/mese |
| 2 | Bioraria Smart | bioraria | 0.2800 | 0.1600 | 0.1600 | 7.90 €/mese |
| 3 | Trioraria Flex | trioraria | 0.3100 | 0.1900 | 0.1300 | 6.50 €/mese |
| 4 | Flat Famiglie | monoraria | 0.2000 | 0.2000 | 0.2000 | 12.00 €/mese |
| 5 | Green Plus | bioraria | 0.2500 | 0.1400 | 0.1400 | 10.00 €/mese |

---

### `consumi`
Letture mensili di energia per ogni POD, su 6 mesi (luglio–dicembre 2024).

| Colonna | Tipo | Descrizione |
|---|---|---|
| `id` | INTEGER PK | Identificativo riga |
| `pod` | TEXT FK | Codice POD → `anagrafica.pod` |
| `anno` | INTEGER | Anno di riferimento |
| `mese` | INTEGER | Mese di riferimento (1–12) |
| `kwh_f1` | REAL | Energia consumata in fascia F1 (kWh) |
| `kwh_f2` | REAL | Energia consumata in fascia F2 (kWh) |
| `kwh_f3` | REAL | Energia consumata in fascia F3 (kWh) |
| `kwh_totale` | REAL | Totale mensile (kWh) |

> Per clienti con offerta monoraria, tutto il consumo è registrato in `kwh_f1`.  
> La stagionalità è simulata: +20% in inverno (dic–feb), –10% in estate (giu–ago).

---

### `bollette`
Fatture bimestrali aggregate. Ogni record corrisponde a un PDF nella cartella `pdfs/`.

| Colonna | Tipo | Descrizione |
|---|---|---|
| `id` | INTEGER PK | Identificativo bolletta |
| `numero_bolletta` | TEXT | Numero documento (es. `LI20240900001`) |
| `pod` | TEXT FK | Codice POD → `anagrafica.pod` |
| `id_offerta` | INTEGER FK | Offerta applicata → `offerte.id` |
| `periodo_dal` | TEXT | Inizio periodo di competenza |
| `periodo_al` | TEXT | Fine periodo di competenza |
| `kwh_f1` | REAL | Energia F1 del bimestre (kWh) |
| `kwh_f2` | REAL | Energia F2 del bimestre (kWh) |
| `kwh_f3` | REAL | Energia F3 del bimestre (kWh) |
| `kwh_totali` | REAL | Totale energia bimestrale (kWh) |
| `materia_energia` | REAL | Costo materia energia + quota fissa (€) |
| `oneri_sistema` | REAL | Oneri di sistema (~4.5 c€/kWh) (€) |
| `trasporto_distribuzione` | REAL | Costo trasporto e distribuzione (~3.5 c€/kWh) (€) |
| `imposte` | REAL | Accise + IVA 10% residenziale (€) |
| `totale` | REAL | Totale da pagare (€) |
| `data_emissione` | TEXT | Data di emissione della bolletta |
| `data_scadenza` | TEXT | Data di scadenza pagamento |
| `pdf_path` | TEXT | Path assoluto al PDF corrispondente |

---

## Relazioni tra tabelle

```
anagrafica ──< consumi        (anagrafica.pod = consumi.pod)
anagrafica ──< bollette       (anagrafica.pod = bollette.pod)
offerte    ──< anagrafica     (offerte.id = anagrafica.id_offerta)
offerte    ──< bollette       (offerte.id = bollette.id_offerta)
```

---

## Volumi

| Entità | Quantità |
|---|---|
| Clienti | 200 |
| Offerte | 5 |
| Letture mensili | 1.200 (6 mesi × 200 clienti) |
| Bollette | 600 (3 bimestrali × 200 clienti) |
| PDF | 600 |

---

## Come usare il database

```python
import sqlite3

conn = sqlite3.connect("db/energy_dataset.db")
conn.row_factory = sqlite3.Row

# Esempio: bollette di un cliente con dettaglio offerta
cur = conn.execute("""
    SELECT
        a.nome, a.cognome, a.pod,
        o.nome AS offerta, o.tipo,
        b.numero_bolletta, b.periodo_dal, b.periodo_al,
        b.kwh_totali, b.totale, b.pdf_path
    FROM bollette b
    JOIN anagrafica a ON a.pod = b.pod
    JOIN offerte    o ON o.id  = b.id_offerta
    ORDER BY a.cognome, b.periodo_dal
    LIMIT 10
""")

for row in cur.fetchall():
    print(dict(row))
```

---

## Dipendenze

```bash
pip install faker reportlab python-dateutil
```

## Esecuzione

```bash
python genera_dataset_energy.py
```

---

*Dataset generato per uso esclusivamente didattico – Master CESMA, Università degli Studi di Roma Tor Vergata.*
