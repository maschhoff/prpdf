# ai.py – Vorschlag von Titel und Ordner durch KI

import os
from openai import OpenAI
import settings

# 🔑 OpenAI API-Key laden
config = settings.loadConfig()
API_KEY = config.get("openai_api_key", "")

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

    # 2️⃣ Anfrage an das Modell über responses.create (neuer Endpoint)
    response = client.responses.create(
        model="gpt-5",
        input=[
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
                        # ✅ Das ist jetzt korrekt im responses-API
                        "type": "input_file",
                        "input_file_id": uploaded_file.id
                    }
                ]
            }
        ],
        temperature=0.0,
    )

    # 3️⃣ Antworttext extrahieren
    result = response.output_text.strip()
    return result


# Beispielaufruf:
# ordner = ["Rechnungen", "Versicherung", "Steuer", "Privat"]
# ergebnis = categorize_document("Rechnung_AfB_NotebookX280_27-2024-191259_27_03_2024_2754.pdf", ordner)
# print(ergebnis)
