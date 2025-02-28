import json
import os

import google.generativeai as genai

from dotenv import load_dotenv

# .env-Datei laden
load_dotenv()  # Lade die Umgebungsvariablen aus der api_key.env-Datei

# Gemini API Key aus der Umgebungsvariablen laden
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if GOOGLE_API_KEY is None:
    print("Fehler: Google API Key nicht in der api_key.env-Datei gefunden.")
    exit()

def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Fehler: Die Datei {filepath} wurde nicht gefunden.")
        return {}
    except json.JSONDecodeError:
        print(f"Fehler: Die Datei {filepath} konnte nicht gelesen werden. Möglicherweise ist sie beschädigt.")
        return {}

def load_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def get_gemini_response(prompt, user_input, data, history, current_phase):
    """
    Sendet einen strukturierten Input an Gemini und erhält die strukturierte Antwort.
    """
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    # Input-Template erstellen
    input_template = {
        "prompt": prompt,
        "user_input": user_input,
        "data": data,
        "history": history
    }

    try:
        response = model.generate_content(json.dumps(input_template))

        # Überprüfen, ob die Antwort leer ist
        if not response.text.strip():
            raise ValueError("Die Antwort von Gemini ist leer.")

        # Sicherstellen, dass die Antwort als UTF-8 kodiert ist
        clean_response = response.text.strip()

        # Entferne Markdown-Code-Block-Markierungen
        if clean_response.startswith("```json"):
            clean_response = clean_response[7:]  # Entferne ```json
        if clean_response.endswith("```"):
            clean_response = clean_response[:-3]  # Entferne ```
        clean_response = clean_response.strip()  # Entferne zusätzliche Leerzeichen

        # Versuchen, die bereinigte Antwort als JSON zu parsen
        try:
            parsed_response = json.loads(clean_response)
        except json.JSONDecodeError as e:
            print("Fehler beim Parsen der Antwort als JSON:", e)
            print("Bereinigte Antwort:", clean_response)
            return {"error": "Die Antwort von Gemini konnte nicht als JSON interpretiert werden."}

        if "response" not in parsed_response:
            raise ValueError("Die Antwort enthält kein 'response'-Feld.")

        return parsed_response

    except json.JSONDecodeError as e:
        print("Fehler: Die Antwort von Gemini konnte nicht als JSON interpretiert werden.")
        return {"error": "Die Antwort von Gemini konnte nicht als JSON interpretiert werden."}
    except ValueError as ve:
        print(f"Wertfehler: {ve}")
        return {"error": str(ve)}
    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")
        return {"error": f"Fehler bei der Gemini-Anfrage: {e}"}

def main():
    """
    Hauptfunktion des Programms.
    """
    prompt_file = 'prompt.md'
    data_file = 'data.json'
    history_file = 'history.md'

    # Daten und Prompt laden
    prompt = load_text(prompt_file)

    # Überprüfen, ob history.md existiert und initialisieren, wenn nicht
    if not os.path.exists(history_file):
        with open(history_file, 'w', encoding='utf-8') as f:
            f.write("**Spielverlauf**\n\n")  # Initialer Inhalt für die History-Datei

    # Überprüfen, ob data.json existiert und initialisieren, wenn nicht
    if not os.path.exists(data_file):
        data = {
            "name": "",
            "faction": "",
            "trademarks": {},
            "flaws": [],
            "drive": {
                "description": "",
                "track": [False] * 10
            },
            "edges": [],
            "stunt_points": 0,
            "inventory": [],
            "xp": 0,
            "current_quest": None,
            "locations": {
                "known": [],
                "current_location": None,
                "routes": {}
            },
            "contacts": {
                "allies": [],
                "factions_status": {},
                "current_intel": ""
            },
            "enemies": {
                "known": [],
                "suspected": [],
                "status": {}
            },
            "quest_log": [],
            "status_effects": []
        }
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    else:
        data = load_data(data_file)

    # Initialisieren der Geschichte
    history = "Die Charaktererstellung muss gestartet werden."  # Nachricht für leere Geschichte

    current_phase = "Spielphase"  # Setzen Sie die Phase auf "Spielphase"

    print("Wenn die Charaktererstellung erforderlich ist, antworte mit Charakter erstellen.")

    # Hauptschleife des Spiels
    while True:
        user_input = input("\nDeine Aktion: ")
        print(f"Benutzereingabe: {user_input}")  # Debug-Ausgabe

        # Kontext für Gemini erstellen
        gemini_response = get_gemini_response(prompt, user_input, data, history, current_phase)

        # Überprüfen, ob die Antwort einen Fehler enthält
        if "error" in gemini_response:
            print(gemini_response["error"])
            continue

        # Antwort des Spielleiters
        game_master_response = gemini_response.get("response", "")
        data_update = gemini_response.get("data_update", {})
        history_update = gemini_response.get("history_update", "")

        # Antwort ausgeben
        print(f"\n{game_master_response}")

        # Selektives Aktualisieren der Datenstruktur
        if isinstance(data_update, dict):
            for key, value in data_update.items():
                data[key] = value  # Aktualisiere nur vorhandene Schlüssel
        else:
            print("Warnung: data_update ist kein Dictionary.  Wird ignoriert.")

        # History aktualisieren
        with open(history_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n**Spieler:** {user_input}\n")
            f.write(f"**Spielleiter:** {game_master_response}\n")
            f.write(f"**Aktualisierte Geschichte:** {history_update}\n")

        # Aktualisieren der data.json
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        # History neu laden
        history = load_text(history_file)

        # Optional: Spiel beenden, wenn der Spieler etwas Bestimmtes eingibt
        if user_input.lower() == "ende":
            print("Spiel beendet.")
            break

if __name__ == "__main__":
    main()