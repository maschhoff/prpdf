# ai_with_file_upload.py
import json
import os
from openai import OpenAI
import settings
from openai import error as openai_error

config = settings.loadConfig()
API_KEY = config.get("openai_api_key", "")
client = OpenAI(api_key=API_KEY)

def categorize_document_with_upload(file_path: str, ordner_liste: list[str]):
    # 1) Upload
    try:
        with open(file_path, "rb") as f:
            uploaded = client.files.create(file=f, purpose="assistants")
    except Exception as e:
        print("FEHLER beim Hochladen der Datei:", e)
        raise

    # Debug: inspect uploaded object
    print("Uploaded file object (für Debug):", uploaded)
    # Stelle sicher, dass id vorhanden ist
    file_id = getattr(uploaded, "id", None) or uploaded.get("id") if isinstance(uploaded, dict) else None
    if not file_id:
        raise RuntimeError("Upload hat keine 'id' zurückgegeben. Objekt: " + str(uploaded))

    # 2) Call responses.create mit input_file
    try:
        response = client.responses.create(
            model="gpt-5",
            input=[
                {"role": "system",
                 "content": (
                     "Du bist ein intelligentes Dokumentenverwaltungssystem. "
                     "Gib ausschließlich ein JSON-Objekt im Format "
                     "{\"Ordner\": \"<Ordnername>\", \"Datei\": \"<NeuerDateiname.pdf>\"} zurück."
                 )},
                {"role": "user",
                 "content": [
                     {"type": "text",
                      "text": f"Liste der Ordner:\n{chr(10).join(ordner_liste)}\n\nAnalysiere die Datei und nenne Ordner und Dateinamen."},
                     {"type": "input_file", "input_file_id": file_id}
                 ]}
            ],
            temperature=0.0,
        )
    except openai_error.BadRequestError as e:
        # Detailliertes Debugging-Output
        print("BadRequestError:", e)
        # Wenn möglich, zeige raw response
        try:
            print("Error response:", e.response.json())
        except Exception:
            pass
        raise
    except Exception as e:
        print("Allgemeiner Fehler bei responses.create:", e)
        raise

    # 3) Extrahiere textuelle Ausgabe robust
    # Manche SDK-Versionen haben response.output_text, manche liefern content im response.output
    output_text = None
    if hasattr(response, "output_text"):
        output_text = response.output_text
    else:
        # Versuche generischen Zugriff
        try:
            out = response.output
            # Suche rekursiv nach text-Strings
            fragments = []
            if isinstance(out, list):
                for item in out:
                    # Das Format kann versch. sein; handle common cases:
                    if isinstance(item, dict):
                        # item.get("content") kann Liste sein
                        content = item.get("content")
                        if isinstance(content, list):
                            for c in content:
                                if isinstance(c, dict) and c.get("type") == "output_text":
                                    fragments.append(c.get("text", ""))
                                elif isinstance(c, str):
                                    fragments.append(c)
                        elif isinstance(content, str):
                            fragments.append(content)
            output_text = "\n".join(fragments).strip()
        except Exception:
            output_text = None

    if not output_text:
        # fallback to raw repr
        output_text = str(response)

    # Versuch JSON zu parsen
    try:
        parsed = json.loads(output_text.strip())
        return parsed
    except Exception:
        return {"raw": output_text}

# Beispiel
# ordner = ["Rechnungen", "Versicherung", "Steuer", "Privat"]
# print(categorize_document_with_upload("rechnung.pdf", ordner))
