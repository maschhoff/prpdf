# ai.py suggestion of title and folder from ai

import os
from openai import OpenAI
import settings

# 🔑 Deinen OpenAI API-Key hier eintragen
config = settings.loadConfig()
API_KEY = config.get("openai_api_key","")

# Client initialisieren
client = OpenAI(api_key=API_KEY)

def categorize_document(file_path: str, ordner_liste: list[str]):
    """
    Analysiert ein PDF oder Textdokument und gibt den passenden Ordner + Dateinamen als JSON zurück.
    """

    # Lies den Dateiinhalt
    with open(file_path, "rb") as f:
        file_content = f.read()

    # Baue den System- und User-Prompt auf
    messages = [
        {
            "role": "system",
            "content": "Du bist ein intelligentes Dokumentenverwaltungssystem. "
                       "Lies den Inhalt der Datei, verstehe den Kontext (z. B. Rechnung, Versicherung, Steuer etc.) "
                       "und gib ausschließlich ein JSON-Objekt im Format "
                       "{\"Ordner\": \"<Ordnername>\", \"Datei\": \"<NeuerDateiname.pdf>\"} zurück."
        },
        {
            "role": "user",
            "content": f"Hier ist die Liste der möglichen Ordner:\n{chr(10).join(ordner_liste)}"
        },
        {
            "role": "user",
            "content": f"Analysiere die folgende Datei und bestimme den passenden Ordner und Dateinamen."
        }
    ]

    # Anfrage an ChatGPT senden
    response = client.chat.completions.create(
        model="gpt-5",  # Modellname entsprechend deiner API-Version
        messages=messages,
        files=[("file", (os.path.basename(file_path), file_content, "application/pdf"))],
        temperature=0.0
    )

    # JSON-Antwort ausgeben
    result = response.choices[0].message.content.strip()
    return result


   # ergebnis = categorize_document("Rechnung_AfB_NotebookX280_27-2024-191259_27_03_2024_2754.pdf", ordner)
    
