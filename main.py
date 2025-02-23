import json
import os
import random
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv('api_key.env')  # Lade die Umgebungsvariablen aus der api_key.env-Datei

# Gemini API Key aus der Umgebungsvariablen laden
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if GOOGLE_API_KEY is None:
    print("Fehler: Google API Key nicht in der api_key.env-Datei gefunden.")
    exit()

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def load_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def roll_dice(action_dice, danger_dice):
    """
    Würfelt Action und Danger Dice und gibt das Ergebnis zurück.
    """
    action_results = [random.randint(1, 6) for _ in range(action_dice)]
    danger_results = [random.randint(1, 6) for _ in range(danger_dice)]

    # Annulliere passende Action Dice
    action_results.sort()
    danger_results.sort()

    while action_results and danger_results:
        action_results.pop(0) # entferne kleinsten Wert
        danger_results.pop(0)

    if not action_results:
        return 0  # Misserfolg (keine Action Dice übrig)
    else:
        return max(action_results)

def get_gemini_response(prompt, data, history, user_input):
    """
    Sendet einen Prompt an Gemini und erhält die Antwort.
    """
    # Gemini API initialisieren
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    # Kontext zusammenstellen
    context = f"""
    # Spielleiter-Anweisungen:
    {prompt}

    # Spielwelt-Daten:
    {json.dumps(data, indent=2)}

    # Bisherige Geschichte:
    {history}
    """

    # Prompt für Gemini erstellen
    full_prompt = f"""
    {context}

    # Spieleraktion:
    {user_input}

    # Deine Antwort als Spielleiter (max. 200 Wörter):
    """

    # Anfrage an Gemini senden
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Fehler bei der Gemini-Anfrage: {e}"

def update_history(history_file, user_input, gemini_response):
    """
    Aktualisiert die history.md-Datei mit der Spieleraktion und der Gemini-Antwort.
    """
    with open(history_file, 'a', encoding='utf-8') as f:
        f.write(f"\n\n**Spieler:** {user_input}\n")
        f.write(f"**Spielleiter:** {gemini_response}\n")

def initialize_character(data_file):
    """
    Initialisiert den Charakter und speichert die Daten in data.json.
    (Hier müsste die Logik für die Charaktererstellung implementiert werden)
    """
    # Beispielhafte Initialisierung (muss angepasst werden!)
    character_data = {
        "name": "eXodus",
        "faction": "Anarchisten",
        "trademarks": {
            "Netrunner": [
                "Hacking",
                "Digital Systems",
                "Neural Interface"
            ],
            "Partisan": [
                "Guerilla Tactics",
                "Sabotage",
                "Stealth Operations"
            ]
        },
        "flaws": [
            "Family Ties",
            "Vendetta"
        ],
        "drive": {
            "description": "Revolution - Rache für die Kommune und Sturz der korrupten Machtstrukturen",
            "track": [False] * 10
        },
        "edges": [
            "Ghost in the Machine",
            "Shadow Walker",
            "Network",
            "Quick Hack"
        ],
        "stunt_points": 3,
        "inventory": [
            "Militärischer Cyberdeck",
            "Stealth-Suite",
            "EMP-Granaten",
            "Datensplitter mit Beweisen"
        ],
        "xp": 0,
        "current_quest": None,
        "locations": {
            "known": ["Anarchistische Kommune (zerstört)", "Neo-Berlin Untergrund"],
            "current_location": "Neo-Berlin Untergrund",
            "routes": {}
        },
        "contacts": {
            "allies": [],
            "factions_status": {},
            "current_intel": None
        },
        "enemies": {
            "known": [],
            "suspected": [],
            "status": {}
        },
        "quest_log": [],
        "status_effects": []
    }
    save_data(data_file, character_data)
    return character_data


def main():
    """
    Hauptfunktion des Programms.
    """
    # Pfade zu den Dateien
    prompt_file = 'prompt.md'
    data_file = 'data.json'
    history_file = 'history.md'

    # Daten und Prompt laden
    prompt = load_text(prompt_file)

    # Sicherstellen, dass history.md existiert, andernfalls initialisieren
    if not os.path.exists(history_file):
        with open(history_file, 'w', encoding='utf-8') as f:
            f.write("**Spielverlauf**\n\n")  # Initialer Inhalt für die History-Datei

    # Überprüfen, ob history.md leer ist
    if os.path.getsize(history_file) == 0:
        print("Charakter wird initialisiert...")
        data = initialize_character(data_file)
        history = ""  # Initialisiere history als leeren String
    else:
        data = load_data(data_file)
        history = load_text(history_file)
        print("Fortsetzung der Geschichte basierend auf history.md und data.json...")

    # Hauptschleife des Spiels
    while True:
        # Spieler-Input abfragen
        user_input = input("\nDeine Aktion: ")

        # Aktionen des Spielers parsen
        if user_input.startswith("würfel"):
            try:
                parts = user_input.split()
                action_dice = int(parts[1])
                danger_dice = int(parts[2])
                roll_result = roll_dice(action_dice, danger_dice)

                if roll_result == 0:
                     gemini_response = "Misserfolg!"
                elif roll_result == 6:
                    gemini_response = f"Voller Erfolg! Du hast eine {roll_result} gewürfelt."
                else:
                   gemini_response = f"Erfolg! Du hast eine {roll_result} gewürfelt."
                print(f"\nDu würfelst: {gemini_response}")

            except (IndexError, ValueError):
                print("Ungültige Würfelanweisung.  Nutze: würfel <action_dice> <danger_dice>")
                continue # Zurück zum Anfang der Schleife
        else:
            # Gemini um eine Antwort bitten
            gemini_response = get_gemini_response(prompt, data, history, user_input)

            # Antwort ausgeben
            print(f"\n{gemini_response}")

        # History aktualisieren
        update_history(history_file, user_input, gemini_response)

        # History neu laden
        history = load_text(history_file)

        # Optional: Spiel beenden, wenn der Spieler etwas Bestimmtes eingibt
        if user_input.lower() == "ende":
            print("Spiel beendet.")
            break

        # Daten aktualisieren (Beispiel - MUSS ANGEPASST WERDEN!)
        data = load_data(data_file) # Neuladen der Daten nach dem Updaten, falls Aktionen diese verändert haben
        data["locations"]["current_location"] = "Irgendein neuer Ort" # Beispiel-Änderung!
        save_data(data_file, data)

if __name__ == "__main__":
    main()