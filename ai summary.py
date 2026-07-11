
""""
-------------
Liest die Churn-Findings direkt aus der SQLite-Datenbank, schickt sie an die
Anthropic-API(Claude) und laesst daraus automatisch eine Executive Summary schreiben.

Zeigt: LLM-API, strukturiertes Prompt-Design, SQL -> LLM Workflow-Automatisierung.

Vor dem Ausfuehren:
  churn_env\\Scripts\\python.exe -m pip install anthropic
  API-Key setzen (einmalig im Terminal):   set ANTHROPIC_API_KEY=sk-ant-dein-key
Ausfuehren:
  churn_env\\Scripts\\python.exe ai_summary.py
"""

import sqlite3
import pandas as pd
from anthropic import Anthropic

# --- 1. Daten aus der Datenbank holen ( nicht hartkodiert) ---
con = sqlite3.connect(r"C:\Users\irina\Downloads\churn.db")


def quote(sql: str) -> pd.DataFrame:
    return pd.read_sql_query(sql, con)


land = quote("""
    SELECT Geography,
           COUNT(*) AS Kunden,
           ROUND(AVG(Exited)*100, 1) AS Quote
    FROM Churn_Modelling GROUP BY Geography
""")

alter = quote("""
    SELECT CASE WHEN Age < 40 THEN 'unter 40' ELSE '40 und aelter' END AS Gruppe,
           COUNT(*) AS Kunden,
           ROUND(AVG(Exited)*100, 1) AS Quote
    FROM Churn_Modelling GROUP BY Gruppe
""")

produkte = quote("""
    SELECT NumOfProducts,
           COUNT(*) AS Kunden,
           ROUND(AVG(Exited)*100, 1) AS Quote
    FROM Churn_Modelling GROUP BY NumOfProducts ORDER BY NumOfProducts
""")

segment = quote("""
    SELECT COUNT(*) AS Kunden,
           ROUND(AVG(Exited)*100, 1) AS Quote
    FROM Churn_Modelling
    WHERE Geography='Germany' AND Age>=40 AND IsActiveMember=0
""")

gesamt = quote("SELECT ROUND(AVG(Exited)*100,1) AS Quote FROM Churn_Modelling")

# --- 2. Findings als Text fuer das Modell aufbereiten ---
findings = f"""
Gesamt-Churn: {gesamt['Quote'][0]} %
 
Nach Land:
{land.to_string(index=False)}
 
Nach Altersgruppe:
{alter.to_string(index=False)}
 
Nach Anzahl Produkte:
{produkte.to_string(index=False)}
 
Hochrisiko-Segment (Deutschland, 40+, inaktiv):
{segment.to_string(index=False)}
"""

# --- 3. Prompt-Design: klare Rolle, klare Aufgabe, klares Format ---
system_prompt = (
    "Du bist Data Analyst und schreibst praezise Executive Summaries fuer "
    "Entscheider ohne Datenhintergrund. Nutze nur die gelieferten Zahlen, "
    "erfinde nichts dazu."
)

user_prompt = f"""Hier sind die Ergebnisse einer Churn-Analyse einer Retail-Bank
(10.000 Kunden). Schreibe daraus eine Executive Summary fuer den Vorstand.
 
Anforderungen:
- Maximal 200 Woerter, sachlich, auf Deutsch.
- Beginne mit dem wichtigsten Befund (dem Hochrisiko-Segment).
- Nenne konkrete Zahlen.
- Schliesse mit 3 priorisierten Handlungsempfehlungen als Aufzaehlung.
 
Ergebnisse:
{findings}
"""

# 4. Anthropic-API aufrufen
client = Anthropic()  # liest den Key Y

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1000,
    temperature=0.3,           # niedrig = faktentreu, wenig "Fantasie"
    system=system_prompt,
    messages=[
        {"role": "user", "content": user_prompt},
    ],
)

summary = message.content[0].text

# --- 5. Ausgeben und speichern ---
print(summary)

with open("executive_summary.md", "w", encoding="utf-8") as f:
    f.write("# Executive Summary (KI-generiert)\n\n")
    f.write(summary)

print("\n\nGespeichert als executive_summary.md")
