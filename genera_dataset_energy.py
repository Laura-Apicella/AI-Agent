"""
genera_dataset_energy.py
========================
Genera un dataset simulato settore energy per uso didattico (Master CESMA).

Output:
  - db/energy_dataset.db  → SQLite con 4 tabelle (anagrafica, offerte, consumi, bollette)
  - pdfs/                 → un PDF per ogni bolletta
  - docs/                 → manuali PDF scaricati da Enel

Dipendenze:
  pip install faker reportlab python-dateutil
"""

import sqlite3
import os
import random
import urllib.request
from datetime import date
from dateutil.relativedelta import relativedelta
from faker import Faker

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT

# ─────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────
random.seed(42)
fake = Faker("it_IT")
Faker.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR   = os.path.join(BASE_DIR, "db")
PDF_DIR  = os.path.join(BASE_DIR, "pdfs")
DB_PATH  = os.path.join(DB_DIR, "energy_dataset.db")
DOCS_DIR = os.path.join(BASE_DIR, "docs")

N_CLIENTI   = 200
MESI_STORIA = 6

FORNITORE_NOME = "LuceItalia S.p.A."
FORNITORE_CF   = "IT09876543210"
FORNITORE_IND  = "Via dell'Energia, 12 – 00144 Roma (RM)"

os.makedirs(DB_DIR,   exist_ok=True)
os.makedirs(PDF_DIR,  exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────
# SAMPLE DATA
# ─────────────────────────────────────────────────────────
NOMI = [
    "Marco","Luca","Giovanni","Francesco","Antonio","Matteo","Lorenzo","Andrea",
    "Davide","Alessandro","Sara","Giulia","Martina","Francesca","Elena","Valentina",
    "Federica","Chiara","Laura","Silvia","Roberto","Stefano","Paolo","Carlo","Angelo",
    "Giuseppina","Maria","Rosa","Anna","Carla","Emanuele","Fabio","Giorgio","Nicola",
    "Claudio","Simone","Riccardo","Daniele","Michele","Salvatore","Teresa","Patrizia",
    "Monica","Roberta","Cristina","Paola","Lucia","Raffaella","Cinzia","Antonella",
    "Sergio","Bruno","Aldo","Renato","Massimo","Gianluca","Vincenzo","Domenico",
    "Carmela","Concetta","Immacolata","Filomena","Assunta","Pasquale","Gennaro",
    "Umberto","Silvio","Augusto","Cesare","Ottavio","Mirko","Kevin","Alessio",
    "Samuele","Edoardo","Filippo","Tommaso","Pietro","Leonardo","Giacomo","Enrico",
    "Beatrice","Ilaria","Giorgia","Alessia","Elisa","Eleonora","Marta","Serena",
    "Veronica","Sabrina","Nadia","Tiziana","Manuela","Daniela","Annalisa","Rossella"
]
COGNOMI = [
    "Rossi","Ferrari","Russo","Esposito","Bianchi","Romano","Colombo","Ricci",
    "Marino","Greco","Bruno","Gallo","Conti","De Luca","Mancini","Costa","Giordano",
    "Rizzo","Lombardi","Moretti","Barbieri","Fontana","Santoro","Marini","Rinaldi",
    "Caruso","Ferrara","Galli","Montanari","Leone","Longo","Gentile","Martinelli",
    "Vitale","Pellegrini","Palumbo","Sanna","Farina","Coppola","Testa","Villa",
    "Ferretti","Orlando","Serra","De Angelis","Fabbri","Marchetti","Amato","Neri",
    "Cattaneo","Ferraro","Silvestri","Mazza","Caputo","Benedetti","Barone","Donati",
    "Riccardi","Parisi","Poli","D'Amico","Riva","Vitali","Battaglia","Catalano",
    "Grasso","Monti","Martini","Pagano","Ruggiero","Grassi","Valentini","Sala",
    "Bianco","Milani","Piccolo","Sartori","Rizzi","Taddei","Ferri","Sorrentino",
    "Fiore","Scarpa","Negri","Pellegrino","Carbone","Guerra","Piras","Melis",
    "Cherchi","Floris","Careddu","Serpi","Mura","Lai","Pinna","Garau","Cadeddu"
]
COMUNI = [
    ("Roma","00100","RM"), ("Milano","20100","MI"), ("Napoli","80100","NA"),
    ("Torino","10100","TO"), ("Palermo","90100","PA"), ("Genova","16100","GE"),
    ("Bologna","40100","BO"), ("Firenze","50100","FI"), ("Bari","70100","BA"),
    ("Catania","95100","CT"), ("Venezia","30100","VE"), ("Verona","37100","VR"),
    ("Messina","98100","ME"), ("Padova","35100","PD"), ("Trieste","34100","TS"),
    ("Taranto","74100","TA"), ("Brescia","25100","BS"), ("Parma","43100","PR"),
    ("Modena","41100","MO"), ("Reggio Calabria","89100","RC"),
    ("Perugia","06100","PG"), ("Cagliari","09100","CA"), ("Sassari","07100","SS"),
    ("Salerno","84100","SA"), ("Ferrara","44100","FE"), ("Pisa","56100","PI"),
    ("Ancona","60100","AN"), ("Foggia","71100","FG"), ("Reggio Emilia","42100","RE"),
    ("Ravenna","48100","RA"), ("Rimini","47900","RN"), ("Bergamo","24100","BG"),
    ("Lecce","73100","LE"), ("Trento","38100","TN"), ("Udine","33100","UD"),
    ("Pescara","65100","PE"), ("Livorno","57100","LI"), ("Siracusa","96100","SR"),
    ("Cosenza","87100","CS"), ("Latina","04100","LT"),
]

OFFERTE_DATA = [
    {
        "id": 1, "nome": "Monoraria Base", "tipo": "monoraria",
        "prezzo_f1": 0.22, "prezzo_f2": 0.22, "prezzo_f3": 0.22,
        "quota_fissa_mensile": 9.50,
        "valida_dal": "2023-01-01", "valida_al": "2025-12-31"
    },
    {
        "id": 2, "nome": "Bioraria Smart", "tipo": "bioraria",
        "prezzo_f1": 0.28, "prezzo_f2": 0.16, "prezzo_f3": 0.16,
        "quota_fissa_mensile": 7.90,
        "valida_dal": "2023-01-01", "valida_al": "2025-12-31"
    },
    {
        "id": 3, "nome": "Trioraria Flex", "tipo": "trioraria",
        "prezzo_f1": 0.31, "prezzo_f2": 0.19, "prezzo_f3": 0.13,
        "quota_fissa_mensile": 6.50,
        "valida_dal": "2023-06-01", "valida_al": "2025-12-31"
    },
    {
        "id": 4, "nome": "Flat Famiglie", "tipo": "monoraria",
        "prezzo_f1": 0.20, "prezzo_f2": 0.20, "prezzo_f3": 0.20,
        "quota_fissa_mensile": 12.00,
        "valida_dal": "2022-01-01", "valida_al": "2025-12-31"
    },
    {
        "id": 5, "nome": "Green Plus", "tipo": "bioraria",
        "prezzo_f1": 0.25, "prezzo_f2": 0.14, "prezzo_f3": 0.14,
        "quota_fissa_mensile": 10.00,
        "valida_dal": "2024-01-01", "valida_al": "2025-12-31"
    },
]

# ─────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────
def genera_pod():
    return "IT001E" + "".join([str(random.randint(0, 9)) for _ in range(15)])


def genera_codice_fiscale(nome, cognome):
    anni      = random.randint(1955, 2000)
    mesi_cod  = "ABCDEHLMPRST"
    mese      = mesi_cod[random.randint(0, 11)]
    giorno    = str(random.randint(1, 28)).zfill(2)
    comune_cod = "H501"
    ctrl      = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    cf        = f"{cognome[:3].upper()}{nome[:3].upper()}{str(anni)[2:]}{mese}{giorno}{comune_cod}{ctrl}"
    return cf[:16]


def calcola_importo(kwh_f1, kwh_f2, kwh_f3, offerta, n_mesi=2):
    materia_energia = (
        kwh_f1 * offerta["prezzo_f1"] +
        kwh_f2 * offerta["prezzo_f2"] +
        kwh_f3 * offerta["prezzo_f3"]
    )
    quota_fissa = offerta["quota_fissa_mensile"] * n_mesi
    kwh_tot     = kwh_f1 + kwh_f2 + kwh_f3
    oneri       = round(kwh_tot * 0.045, 2)
    trasporto   = round(kwh_tot * 0.035, 2)
    accisa      = round(kwh_tot * 0.0227, 2)
    imponibile  = round(materia_energia + quota_fissa + oneri + trasporto + accisa, 2)
    iva         = round(imponibile * 0.10, 2)
    totale      = round(imponibile + iva, 2)
    return {
        "materia_energia":         round(materia_energia + quota_fissa, 2),
        "oneri_sistema":           oneri,
        "trasporto_distribuzione": trasporto,
        "imposte":                 round(accisa + iva, 2),
        "totale":                  totale,
    }

# ─────────────────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────────────────
def crea_db(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS anagrafica (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            nome             TEXT NOT NULL,
            cognome          TEXT NOT NULL,
            codice_fiscale   TEXT NOT NULL UNIQUE,
            indirizzo        TEXT NOT NULL,
            comune           TEXT NOT NULL,
            cap              TEXT NOT NULL,
            provincia        TEXT NOT NULL,
            email            TEXT NOT NULL,
            telefono         TEXT NOT NULL,
            pod              TEXT NOT NULL UNIQUE,
            id_offerta       INTEGER NOT NULL,
            data_attivazione TEXT NOT NULL,
            FOREIGN KEY (id_offerta) REFERENCES offerte(id)
        );
        CREATE TABLE IF NOT EXISTS offerte (
            id                  INTEGER PRIMARY KEY,
            nome                TEXT NOT NULL,
            tipo                TEXT NOT NULL,
            prezzo_f1           REAL NOT NULL,
            prezzo_f2           REAL NOT NULL,
            prezzo_f3           REAL NOT NULL,
            quota_fissa_mensile REAL NOT NULL,
            valida_dal          TEXT NOT NULL,
            valida_al           TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS consumi (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            pod        TEXT NOT NULL,
            anno       INTEGER NOT NULL,
            mese       INTEGER NOT NULL,
            kwh_f1     REAL NOT NULL,
            kwh_f2     REAL NOT NULL,
            kwh_f3     REAL NOT NULL,
            kwh_totale REAL NOT NULL,
            FOREIGN KEY (pod) REFERENCES anagrafica(pod)
        );
        CREATE TABLE IF NOT EXISTS bollette (
            id                      INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_bolletta         TEXT NOT NULL UNIQUE,
            pod                     TEXT NOT NULL,
            id_offerta              INTEGER NOT NULL,
            periodo_dal             TEXT NOT NULL,
            periodo_al              TEXT NOT NULL,
            kwh_f1                  REAL NOT NULL,
            kwh_f2                  REAL NOT NULL,
            kwh_f3                  REAL NOT NULL,
            kwh_totali              REAL NOT NULL,
            materia_energia         REAL NOT NULL,
            oneri_sistema           REAL NOT NULL,
            trasporto_distribuzione REAL NOT NULL,
            imposte                 REAL NOT NULL,
            totale                  REAL NOT NULL,
            data_emissione          TEXT NOT NULL,
            data_scadenza           TEXT NOT NULL,
            pdf_path                TEXT,
            FOREIGN KEY (pod)        REFERENCES anagrafica(pod),
            FOREIGN KEY (id_offerta) REFERENCES offerte(id)
        );
    """)
    conn.commit()

# ─────────────────────────────────────────────────────────
# PDF BOLLETTA
# ─────────────────────────────────────────────────────────
def genera_pdf_bolletta(bolletta, cliente, offerta, output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm,  bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    BLUE   = colors.HexColor("#1a5276")
    LGREY  = colors.HexColor("#f2f3f4")
    MGREY  = colors.HexColor("#aab7b8")

    s_body  = ParagraphStyle("body",   fontSize=9,  leading=13)
    s_h2    = ParagraphStyle("h2",     fontSize=10, leading=14, spaceAfter=2, fontName="Helvetica-Bold")
    s_right = ParagraphStyle("right",  fontSize=9,  leading=12, alignment=TA_RIGHT)
    s_small = ParagraphStyle("small",  fontSize=8,  leading=11, textColor=colors.grey)
    s_tot   = ParagraphStyle("totale", fontSize=13, leading=18, fontName="Helvetica-Bold", textColor=BLUE)

    story = []

    # HEADER
    header = Table([[
        Paragraph(
            f"<font size=16><b>{FORNITORE_NOME}</b></font><br/>"
            f"<font size=8 color='grey'>{FORNITORE_IND}<br/>{FORNITORE_CF}</font>",
            styles["Normal"]
        ),
        Paragraph(
            f"<b>BOLLETTA N.</b> {bolletta['numero_bolletta']}<br/>"
            f"<font size=8>Emissione: {bolletta['data_emissione']}<br/>"
            f"Scadenza: <b>{bolletta['data_scadenza']}</b></font>",
            s_right
        )
    ]], colWidths=[10*cm, 7*cm])
    header.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(header)
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=10))

    # CLIENTE + FORNITURA
    info = Table([
        [Paragraph("<b>INTESTATARIO</b>", s_h2), Paragraph("<b>FORNITURA</b>", s_h2)],
        [
            Paragraph(
                f"{cliente['nome']} {cliente['cognome']}<br/>"
                f"{cliente['indirizzo']}<br/>"
                f"{cliente['cap']} {cliente['comune']} ({cliente['provincia']})<br/>"
                f"C.F.: {cliente['codice_fiscale']}<br/>"
                f"Email: {cliente['email']}",
                s_body
            ),
            Paragraph(
                f"<b>POD:</b> {bolletta['pod']}<br/>"
                f"<b>Offerta:</b> {offerta['nome']} ({offerta['tipo']})<br/>"
                f"<b>Periodo:</b> {bolletta['periodo_dal']} – {bolletta['periodo_al']}<br/>"
                f"<b>Energia prelevata:</b> {bolletta['kwh_totali']:.1f} kWh",
                s_body
            ),
        ]
    ], colWidths=[8.5*cm, 8.5*cm])
    info.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), LGREY),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("GRID",          (0,0), (-1,-1), 0.5, MGREY),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ]))
    story.append(info)
    story.append(Spacer(1, 16))

    # CONSUMI PER FASCIA
    story.append(Paragraph("DETTAGLIO CONSUMI PER FASCIA ORARIA", s_h2))
    story.append(Spacer(1, 4))

    tipo = offerta["tipo"]
    if tipo == "monoraria":
        righe_consumi = [
            ["Fascia", "Energia (kWh)", "Prezzo (€/kWh)", "Importo (€)"],
            ["F1 (unica fascia)",
             f"{bolletta['kwh_f1']:.1f}",
             f"{offerta['prezzo_f1']:.4f}",
             f"{bolletta['kwh_f1'] * offerta['prezzo_f1']:.2f}"],
        ]
    elif tipo == "bioraria":
        righe_consumi = [
            ["Fascia", "Energia (kWh)", "Prezzo (€/kWh)", "Importo (€)"],
            ["F1 – Picco (lun-ven 8-19)",
             f"{bolletta['kwh_f1']:.1f}",
             f"{offerta['prezzo_f1']:.4f}",
             f"{bolletta['kwh_f1'] * offerta['prezzo_f1']:.2f}"],
            ["F2/F3 – Fuori picco",
             f"{bolletta['kwh_f2'] + bolletta['kwh_f3']:.1f}",
             f"{offerta['prezzo_f2']:.4f}",
             f"{(bolletta['kwh_f2'] + bolletta['kwh_f3']) * offerta['prezzo_f2']:.2f}"],
        ]
    else:
        righe_consumi = [
            ["Fascia", "Energia (kWh)", "Prezzo (€/kWh)", "Importo (€)"],
            ["F1 – Punta (lun-ven 8-19)",
             f"{bolletta['kwh_f1']:.1f}",
             f"{offerta['prezzo_f1']:.4f}",
             f"{bolletta['kwh_f1'] * offerta['prezzo_f1']:.2f}"],
            ["F2 – Intermedia",
             f"{bolletta['kwh_f2']:.1f}",
             f"{offerta['prezzo_f2']:.4f}",
             f"{bolletta['kwh_f2'] * offerta['prezzo_f2']:.2f}"],
            ["F3 – Fuori punta (notti e festivi)",
             f"{bolletta['kwh_f3']:.1f}",
             f"{offerta['prezzo_f3']:.4f}",
             f"{bolletta['kwh_f3'] * offerta['prezzo_f3']:.2f}"],
        ]

    t_consumi = Table(righe_consumi, colWidths=[5.5*cm, 3.5*cm, 4.5*cm, 3.5*cm])
    t_consumi.setStyle(TableStyle([
        ("BACKGROUND",     (0,0), (-1,0), BLUE),
        ("TEXTCOLOR",      (0,0), (-1,0), colors.white),
        ("FONTNAME",       (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",       (0,0), (-1,-1), 8),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LGREY]),
        ("GRID",           (0,0), (-1,-1), 0.4, MGREY),
        ("ALIGN",          (1,0), (-1,-1), "CENTER"),
        ("TOPPADDING",     (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 5),
        ("LEFTPADDING",    (0,0), (-1,-1), 6),
    ]))
    story.append(t_consumi)
    story.append(Spacer(1, 16))

    # RIEPILOGO IMPORTI
    story.append(Paragraph("RIEPILOGO IMPORTI", s_h2))
    story.append(Spacer(1, 4))

    t_riepilogo = Table([
        ["Voce", "Importo (€)"],
        ["Materia energia + Quota fissa",      f"{bolletta['materia_energia']:.2f}"],
        ["Oneri di sistema",                    f"{bolletta['oneri_sistema']:.2f}"],
        ["Trasporto e distribuzione",           f"{bolletta['trasporto_distribuzione']:.2f}"],
        ["Imposte e accise (IVA 10% inclusa)", f"{bolletta['imposte']:.2f}"],
        ["TOTALE DA PAGARE",                    f"{bolletta['totale']:.2f}"],
    ], colWidths=[13*cm, 4*cm])
    t_riepilogo.setStyle(TableStyle([
        ("BACKGROUND",     (0,0),  (-1,0),  BLUE),
        ("TEXTCOLOR",      (0,0),  (-1,0),  colors.white),
        ("FONTNAME",       (0,0),  (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0,0),  (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1),  (-1,-2), [colors.white, LGREY]),
        ("BACKGROUND",     (0,-1), (-1,-1), colors.HexColor("#d5e8f5")),
        ("FONTNAME",       (0,-1), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE",       (0,-1), (-1,-1), 10),
        ("GRID",           (0,0),  (-1,-1), 0.4, MGREY),
        ("ALIGN",          (1,0),  (-1,-1), "RIGHT"),
        ("TOPPADDING",     (0,0),  (-1,-1), 6),
        ("BOTTOMPADDING",  (0,0),  (-1,-1), 6),
        ("LEFTPADDING",    (0,0),  (-1,-1), 8),
        ("RIGHTPADDING",   (0,0),  (-1,-1), 8),
    ]))
    story.append(t_riepilogo)
    story.append(Spacer(1, 20))

    # TOTALE EVIDENZIATO
    story.append(Paragraph(
        f"Importo totale da pagare entro il <b>{bolletta['data_scadenza']}</b>: "
        f"<b>€ {bolletta['totale']:.2f}</b>",
        s_tot
    ))
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=1, color=MGREY, spaceAfter=8))

    # MODALITÀ DI PAGAMENTO
    story.append(Paragraph("MODALITÀ DI PAGAMENTO", s_h2))
    story.append(Paragraph(
        "Bonifico bancario: IBAN IT60X0542811101000000123456 – causale: numero bolletta<br/>"
        "Addebito diretto (SDD): attivo se autorizzato in fase di contratto<br/>"
        "Pagamento online: area clienti su <u>www.luceitalia.it</u>",
        s_body
    ))
    story.append(Spacer(1, 12))

    # FOOTER
    story.append(HRFlowable(width="100%", thickness=0.5, color=MGREY, spaceAfter=4))
    story.append(Paragraph(
        f"{FORNITORE_NOME} – {FORNITORE_CF} – "
        f"Documento generato per uso didattico (Master CESMA, Università di Roma Tor Vergata)",
        s_small
    ))

    doc.build(story)

# ─────────────────────────────────────────────────────────
# DOWNLOAD DOCUMENTI
# ─────────────────────────────────────────────────────────
def scarica_docs():
    documenti = [
        (
            "Manuale_utente_Gest_Ambientale_IMPRESA.pdf",
            "https://scm.enel.it/Scm/mol/doc/Manuale_utente_Gest_Ambientale_IMPRESA.pdf"
        ),
        (
            "manuale-utente-waybox-start-e-pro.pdf",
            "https://www.enel.it/content/dam/asset/documenti/waybox/manuale-utente-waybox-start-e-pro.pdf"
        ),
        (
            "MLM_CMD_Manuale_Utente_Fornitore_V3.pdf",
            "https://globalprocurement.enel.com/content/dam/enel-gp/documents/manuals/other-procurement-systems/it/MLM%20CMD%20Manuale%20Utente%20Fornitore%20(IT)%20V3.pdf"
        ),
    ]

    print("\n── Download documenti in docs/ ──")
    for nome_file, url in documenti:
        dest = os.path.join(DOCS_DIR, nome_file)
        try:
            print(f"  Scaricando {nome_file}...")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                with open(dest, "wb") as f:
                    f.write(response.read())
            size_kb = os.path.getsize(dest) // 1024
            print(f"  OK – {size_kb} KB")
        except Exception as e:
            print(f"  ERRORE su {nome_file}: {e}")

# ─────────────────────────────────────────────────────────
# GENERAZIONE DATI
# ─────────────────────────────────────────────────────────
def genera_clienti(conn):
    cur       = conn.cursor()
    clienti   = []
    pod_usati = set()
    cf_usati  = set()

    for i in range(N_CLIENTI):
        nome    = NOMI[i % len(NOMI)]
        cognome = COGNOMI[i % len(COGNOMI)]
        comune, cap, prov = random.choice(COMUNI)

        pod = genera_pod()
        while pod in pod_usati:
            pod = genera_pod()
        pod_usati.add(pod)

        cf = genera_codice_fiscale(nome, cognome)
        while cf in cf_usati:
            cf = cf[:-1] + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        cf_usati.add(cf)

        indirizzo  = fake.street_address()
        email      = (f"{nome.lower()}.{cognome.lower().replace(' ', '')}"
                      f"@{random.choice(['gmail.com','libero.it','virgilio.it','yahoo.it'])}")
        telefono   = fake.phone_number()
        id_offerta = random.randint(1, 5)
        data_att   = date(random.randint(2020, 2023), random.randint(1, 12), 1).isoformat()

        cur.execute("""
            INSERT INTO anagrafica
            (nome, cognome, codice_fiscale, indirizzo, comune, cap, provincia,
             email, telefono, pod, id_offerta, data_attivazione)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (nome, cognome, cf, indirizzo, comune, cap, prov,
              email, telefono, pod, id_offerta, data_att))

        clienti.append({
            "id": cur.lastrowid, "nome": nome, "cognome": cognome,
            "codice_fiscale": cf, "indirizzo": indirizzo,
            "comune": comune, "cap": cap, "provincia": prov,
            "email": email, "telefono": telefono,
            "pod": pod, "id_offerta": id_offerta
        })

    conn.commit()
    return clienti


def genera_consumi(conn, clienti):
    cur    = conn.cursor()
    inizio = date(2024, 7, 1)

    for cliente in clienti:
        base_kwh = random.randint(80, 350)

        for m in range(MESI_STORIA):
            d    = inizio + relativedelta(months=m)
            anno, mese = d.year, d.month

            stagione = 1.0
            if mese in [12, 1, 2]:
                stagione = 1.20
            elif mese in [6, 7, 8]:
                stagione = 0.90

            kwh_tot = round(base_kwh * stagione * random.uniform(0.85, 1.15), 1)

            tipo = next(o["tipo"] for o in OFFERTE_DATA if o["id"] == cliente["id_offerta"])
            if tipo == "monoraria":
                f1 = kwh_tot; f2 = 0.0; f3 = 0.0
            elif tipo == "bioraria":
                f1 = round(kwh_tot * random.uniform(0.55, 0.65), 1)
                f2 = round(kwh_tot - f1, 1); f3 = 0.0
            else:
                f1 = round(kwh_tot * random.uniform(0.45, 0.55), 1)
                f2 = round(kwh_tot * random.uniform(0.25, 0.35), 1)
                f3 = round(kwh_tot - f1 - f2, 1)

            cur.execute("""
                INSERT INTO consumi (pod, anno, mese, kwh_f1, kwh_f2, kwh_f3, kwh_totale)
                VALUES (?,?,?,?,?,?,?)
            """, (cliente["pod"], anno, mese, f1, f2, f3, kwh_tot))

    conn.commit()


def genera_bollette(conn, clienti, offerte_map):
    cur      = conn.cursor()
    bollette = []
    counter  = 1

    bimestri = [
        (date(2024,7,1),  date(2024,8,31),  date(2024,9,10),  date(2024,9,30)),
        (date(2024,9,1),  date(2024,10,31), date(2024,11,10), date(2024,11,30)),
        (date(2024,11,1), date(2024,12,31), date(2025,1,10),  date(2025,1,31)),
    ]

    for cliente in clienti:
        for (dal, al, emissione, scadenza) in bimestri:
            kwh_f1 = kwh_f2 = kwh_f3 = 0.0
            d = dal
            while d <= al:
                row = cur.execute("""
                    SELECT kwh_f1, kwh_f2, kwh_f3 FROM consumi
                    WHERE pod=? AND anno=? AND mese=?
                """, (cliente["pod"], d.year, d.month)).fetchone()
                if row:
                    kwh_f1 += row[0]; kwh_f2 += row[1]; kwh_f3 += row[2]
                d += relativedelta(months=1)

            kwh_tot = round(kwh_f1 + kwh_f2 + kwh_f3, 1)
            offerta = offerte_map[cliente["id_offerta"]]
            importi = calcola_importo(kwh_f1, kwh_f2, kwh_f3, offerta, n_mesi=2)

            numero       = f"LI{emissione.year}{str(emissione.month).zfill(2)}{str(counter).zfill(6)}"
            pdf_filename = f"{numero}_{cliente['pod'][-6:]}.pdf"
            pdf_path     = os.path.join(PDF_DIR, pdf_filename)

            cur.execute("""
                INSERT INTO bollette
                (numero_bolletta, pod, id_offerta, periodo_dal, periodo_al,
                 kwh_f1, kwh_f2, kwh_f3, kwh_totali,
                 materia_energia, oneri_sistema, trasporto_distribuzione, imposte, totale,
                 data_emissione, data_scadenza, pdf_path)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                numero, cliente["pod"], cliente["id_offerta"],
                dal.isoformat(), al.isoformat(),
                round(kwh_f1,1), round(kwh_f2,1), round(kwh_f3,1), kwh_tot,
                importi["materia_energia"], importi["oneri_sistema"],
                importi["trasporto_distribuzione"], importi["imposte"], importi["totale"],
                emissione.isoformat(), scadenza.isoformat(), pdf_path
            ))

            bollette.append({
                "numero_bolletta": numero,
                "pod":             cliente["pod"],
                "id_offerta":      cliente["id_offerta"],
                "periodo_dal":     dal.isoformat(),
                "periodo_al":      al.isoformat(),
                "kwh_f1":          round(kwh_f1,1),
                "kwh_f2":          round(kwh_f2,1),
                "kwh_f3":          round(kwh_f3,1),
                "kwh_totali":      kwh_tot,
                **importi,
                "data_emissione":  emissione.isoformat(),
                "data_scadenza":   scadenza.isoformat(),
                "pdf_path":        pdf_path,
                "_cliente":        cliente,
                "_offerta":        offerta,
            })
            counter += 1

    conn.commit()
    return bollette

# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────
def main():
    print("=" * 55)
    print("  GENERATORE DATASET ENERGY – Master CESMA")
    print("=" * 55)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)

    print("\n[1/6] Creazione schema database...")
    crea_db(conn)

    print("[2/6] Inserimento offerte energy...")
    cur = conn.cursor()
    for o in OFFERTE_DATA:
        cur.execute("""
            INSERT INTO offerte
            (id, nome, tipo, prezzo_f1, prezzo_f2, prezzo_f3, quota_fissa_mensile, valida_dal, valida_al)
            VALUES (:id, :nome, :tipo, :prezzo_f1, :prezzo_f2, :prezzo_f3,
                    :quota_fissa_mensile, :valida_dal, :valida_al)
        """, o)
    conn.commit()
    offerte_map = {o["id"]: o for o in OFFERTE_DATA}

    print(f"[3/6] Generazione {N_CLIENTI} clienti...")
    clienti = genera_clienti(conn)

    print("[4/6] Generazione consumi mensili...")
    genera_consumi(conn, clienti)

    print("[5/6] Generazione bollette e PDF...")
    bollette = genera_bollette(conn, clienti, offerte_map)
    totale   = len(bollette)
    for i, b in enumerate(bollette, 1):
        genera_pdf_bolletta(b, b["_cliente"], b["_offerta"], b["pdf_path"])
        if i % 50 == 0 or i == totale:
            print(f"  PDF generati: {i}/{totale}")

    conn.close()

    print("[6/6] Download documenti Enel...")
    scarica_docs()

    print("\n" + "=" * 55)
    print("  COMPLETATO")
    print("=" * 55)
    print(f"  Database  → {DB_PATH}")
    print(f"  PDF       → {PDF_DIR}/  ({len(bollette)} file)")
    print(f"  Docs      → {DOCS_DIR}/")
    print(f"\n  Riepilogo:")
    print(f"    Clienti   → {N_CLIENTI}")
    print(f"    Offerte   → {len(OFFERTE_DATA)}")
    print(f"    Consumi   → {N_CLIENTI * MESI_STORIA} righe mensili")
    print(f"    Bollette  → {len(bollette)}")
    print("=" * 55)


if __name__ == "__main__":
    main()