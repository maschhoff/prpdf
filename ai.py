# ai.py – Vorschlag von Titel und Ordner durch KI

import os
from openai import OpenAI
import settings

# 🔑 OpenAI API-Key laden
config = settings.loadConfig()
API_KEY = config.get("openai_api_key", "")

# Client initialisieren
client = OpenAI(api_key=API_KEY)

def categorize_document(file_path: str, ordner_liste: list[str]):
    """
    Analysiert ein PDF oder Textdokument und gibt den passenden Ordner + Dateinamen als JSON zurück.
    """

    # 1️⃣ Datei hochladen
    with open(file_path, "rb") as f:
        uploaded_file = client.files.create(
            file=f,
            purpose="assistants"
        )

    # 2️⃣ Nachrichten im alten (Chat Completions) Format
    messages = [
        {
            "role": "system",
            "content": (
                "Du bist ein intelligentes Dokumentenverwaltungssystem. "
                "Lies den Inhalt der Datei, verstehe den Kontext (z. B. Rechnung, Versicherung, Steuer etc.) "
                "und gib ausschließlich ein JSON-Objekt im Format "
                "{\"Ordner\": \"<Ordnername>\", \"Datei\": \"<NeuerDateiname.pdf>\"} zurück."
            )
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        f"Hier ist die Liste der möglichen Ordner:\n{chr(10).join(ordner_liste)}\n\n"
                        "Analysiere die folgende Datei und bestimme den passenden Ordner und Dateinamen."
                    )
                },
                {
                    # ✅ korrekt für chat.completions
                    "type": "file",
                    "file_id": uploaded_file.id
                }
            ]
        }
    ]

    # 3️⃣ Anfrage an ChatGPT senden
    response = client.chat.completions.create(
        model="gpt-5",
        messages=messages,
        temperature=0.0
    )

    # 4️⃣ Ergebnis extrahieren
    result = response.choices[0].message.content.strip()
    return result


# Beispielaufruf:
# ordner = ["Rechnungen", "Versicherung", "Steuer", "Privat"]
# ergebnis = categorize_document("Rechnung_AfB_NotebookX280_27-2024-191259_27_03_2024_2754.pdf", ordner)
# print(ergebnis)
