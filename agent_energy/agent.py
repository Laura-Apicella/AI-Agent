import sqlite3
from pathlib import Path
import matplotlib.pyplot as plt

from google.adk.agents.llm_agent import Agent
from .services.llm import MODEL



# =========================
# CONFIGURAZIONE
# =========================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "db" / "energy_dataset.db"


# =========================
# TOOLS
# =========================

def riconosci_cliente(codice_fiscale: str, email: str) -> dict:
    """
    Verifica l'identità del cliente tramite codice fiscale ed email.
    Restituisce i dati minimi del cliente solo se l'autenticazione va a buon fine.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT 
            id,
            nome,
            cognome,
            codice_fiscale,
            email,
            pod,
            id_offerta
        FROM anagrafica
        WHERE codice_fiscale = ?
        AND email = ?
    """

    cur = conn.execute(query, (codice_fiscale, email))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return {
            "status": "errore",
            "messaggio": "Cliente non riconosciuto. Verifica codice fiscale ed email."
        }

    return {
        "status": "successo",
        "messaggio": "Cliente riconosciuto correttamente.",
        "cliente": dict(row)
    }


def informazioni_contratto(codice_fiscale: str, email: str) -> dict:
    """
    Recupera le informazioni contrattuali del cliente autenticato.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT
            a.nome,
            a.cognome,
            a.pod,
            o.nome AS offerta,
            o.tipo,
            o.prezzo_f1,
            o.prezzo_f2,
            o.prezzo_f3,
            o.quota_fissa_mensile
        FROM anagrafica a
        JOIN offerte o
            ON a.id_offerta = o.id
        WHERE a.codice_fiscale = ?
        AND a.email = ?
    """

    cur = conn.execute(query, (codice_fiscale, email))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return {
            "status": "errore",
            "messaggio": "Cliente non riconosciuto. Verifica codice fiscale ed email."
        }

    return {
        "status": "successo",
        "contratto": dict(row)
    }


def recupera_ultima_bolletta(codice_fiscale: str, email: str) -> dict:
    """
    Recupera l'ultima bolletta disponibile del cliente autenticato.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT
            a.nome,
            a.cognome,
            a.pod,
            b.numero_bolletta,
            b.periodo_dal,
            b.periodo_al,
            b.kwh_totali,
            b.totale,
            b.data_emissione,
            b.data_scadenza,
            b.pdf_path
        FROM bollette b
        JOIN anagrafica a
            ON a.pod = b.pod
        WHERE a.codice_fiscale = ?
        AND a.email = ?
        ORDER BY b.periodo_al DESC
        LIMIT 1
    """

    cur = conn.execute(query, (codice_fiscale, email))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return {
            "status": "errore",
            "messaggio": "Cliente non riconosciuto oppure nessuna bolletta trovata."
        }

    return {
        "status": "successo",
        "bolletta": dict(row)
    }


def analizza_consumi(codice_fiscale: str, email: str) -> dict:
    """
    Recupera i consumi mensili del cliente e confronta l'ultimo mese con la media.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT
            c.anno,
            c.mese,
            c.kwh_f1,
            c.kwh_f2,
            c.kwh_f3,
            c.kwh_totale
        FROM consumi c
        JOIN anagrafica a
            ON a.pod = c.pod
        WHERE a.codice_fiscale = ?
        AND a.email = ?
        ORDER BY c.anno, c.mese
    """

    cur = conn.execute(query, (codice_fiscale, email))
    rows = cur.fetchall()
    conn.close()

    if len(rows) == 0:
        return {
            "status": "errore",
            "messaggio": "Cliente non riconosciuto oppure nessun consumo trovato."
        }

    consumi = [dict(r) for r in rows]
    media = sum(r["kwh_totale"] for r in consumi) / len(consumi)
    ultimo = consumi[-1]
    ultimo_consumo = ultimo["kwh_totale"]

    if ultimo_consumo > media:
        confronto = "superiore alla media"
    elif ultimo_consumo < media:
        confronto = "inferiore alla media"
    else:
        confronto = "in linea con la media"

    return {
        "status": "successo",
        "ultimo_mese": ultimo,
        "consumo_medio": round(media, 2),
        "confronto": confronto,
        "storico_consumi": consumi
    }


def riepilogo_contratto_completo(codice_fiscale: str, email: str) -> dict:
    """
    Recupera un riepilogo completo del contratto e dell'ultima bolletta del cliente.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT
            a.nome,
            a.cognome,
            a.pod,
            o.nome AS offerta_attiva,
            o.tipo AS tipo_tariffa,
            o.prezzo_f1,
            o.prezzo_f2,
            o.prezzo_f3,
            o.quota_fissa_mensile,
            b.numero_bolletta,
            b.periodo_dal,
            b.periodo_al,
            b.kwh_totali,
            b.materia_energia,
            b.oneri_sistema,
            b.trasporto_distribuzione,
            b.imposte,
            b.totale,
            b.data_emissione,
            b.data_scadenza,
            b.pdf_path
        FROM anagrafica a
        JOIN offerte o ON a.id_offerta = o.id
        LEFT JOIN bollette b ON a.pod = b.pod
        WHERE a.codice_fiscale = ?
        AND a.email = ?
        ORDER BY b.periodo_al DESC
        LIMIT 1
    """

    cur = conn.execute(query, (codice_fiscale, email))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return {
            "status": "errore",
            "messaggio": "Cliente non riconosciuto oppure nessun contratto trovato."
        }

    return {
        "status": "successo",
        "riepilogo_contratto": dict(row)
    }


def grafico_consumi(codice_fiscale: str, email: str) -> dict:
    """
    Genera un grafico PNG dell'andamento dei consumi mensili del cliente.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT
            c.anno,
            c.mese,
            c.kwh_totale
        FROM consumi c
        JOIN anagrafica a
            ON a.pod = c.pod
        WHERE a.codice_fiscale = ?
        AND a.email = ?
        ORDER BY c.anno, c.mese
    """

    cur = conn.execute(query, (codice_fiscale, email))
    rows = cur.fetchall()
    conn.close()

    if len(rows) == 0:
        return {
            "status": "errore",
            "messaggio": "Cliente non riconosciuto oppure nessun consumo trovato."
        }

    mesi = [f"{r['mese']}/{r['anno']}" for r in rows]
    consumi = [r["kwh_totale"] for r in rows]

    output_dir = BASE_DIR.parent / "output"
    output_dir.mkdir(exist_ok=True)

    nome_file = f"grafico_consumi_{codice_fiscale}.png"
    percorso_file = output_dir / nome_file

    plt.figure(figsize=(8, 4))
    plt.plot(mesi, consumi, marker="o")
    plt.title("Andamento consumi mensili")
    plt.xlabel("Mese")
    plt.ylabel("Consumo totale (kWh)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(percorso_file)
    plt.close()

    return {
        "status": "successo",
        "messaggio": "Grafico dei consumi generato correttamente.",
        "percorso_file": str(percorso_file),
        "mesi": mesi,
        "consumi_kwh": consumi
    }


# =========================
# ROOT AGENT
# =========================

root_agent = Agent(
    model=MODEL,
    name="root_agent",
    description="Assistente clienti per un fornitore di energia elettrica.",
    instruction="""
Sei un assistente clienti di un fornitore di energia elettrica.

Il tuo compito è aiutare il cliente a:
- riconoscersi;
- consultare il contratto;
- recuperare l'ultima bolletta;
- analizzare i consumi energetici;
- consultare offerta attiva, fasce orarie, importi e date di scadenza;
- generare grafici dei consumi.

REGOLE IMPORTANTI:
- Rispondi sempre in dialetto romano.
- Usa un tono da burino.
- Non mostrare mai dati personali, consumi, bollette o informazioni contrattuali se il cliente non è stato prima riconosciuto.
- Il cliente deve fornire sia codice fiscale sia email.
- Se l'utente non fornisce codice fiscale ed email, chiedili prima di procedere.
- Se il riconoscimento fallisce, non fornire altri dati.

FUNZIONALITÀ:
- Per riconoscere il cliente usa il tool riconosci_cliente.
- Per informazioni sul contratto usa informazioni_contratto.
- Per recuperare l'ultima bolletta usa recupera_ultima_bolletta.
- Per i consumi usa analizza_consumi.
- Per un riepilogo completo usa riepilogo_contratto_completo.
- Per creare grafici usa grafico_consumi.

INFORMAZIONI DA MOSTRARE:
- Per il contratto mostra:
    • nome offerta attiva
    • tipo tariffa
    • prezzo F1, F2, F3
    • quota fissa mensile

- Per la bolletta mostra:
    • numero bolletta
    • periodo
    • kWh totali
    • totale da pagare
    • data emissione
    • data scadenza
    • percorso PDF

- Per i consumi mostra:
    • consumo dell'ultimo mese
    • consumo medio
    • confronto rispetto alla media
    • se utile, lo storico mensile disponibile

- Per il riepilogo completo mostra:
    • offerta attiva
    • fasce orarie
    • importi principali dell'ultima bolletta
    • totale da pagare
    • data di scadenza

Quando generi un grafico:
- spiega cosa mostra il grafico;
- comunica il percorso del file PNG creato.
""",
    tools=[
        riconosci_cliente,
        informazioni_contratto,
        recupera_ultima_bolletta,
        analizza_consumi,
        riepilogo_contratto_completo,
        grafico_consumi,
    ],
)