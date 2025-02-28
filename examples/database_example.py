# examples/database_example.py
from data.json_database import JSONDatabase
from data.game_state import GameState, GameStateManager
from data.session_handler import SessionHandler
from data.config_handler import ConfigHandler
import os

def main():
    print("=== DATENBANKBEISPIEL ===\n")
    
    # Konfigurations-Handler initialisieren
    config = ConfigHandler()
    print(f"Konfiguration geladen: terminal_width = {config.get('ui.terminal_width')}")
    
    # Config-Wert ändern
    config.set('ui.terminal_width', 100)
    print(f"Konfiguration geändert: terminal_width = {config.get('ui.terminal_width')}")
    
    # Sitzungs-Handler initialisieren
    session = SessionHandler()
    
    # Charakter erstellen (vereinfachtes Beispiel)
    char_db = JSONDatabase("data/characters")
    char_id = "test-char-1"
    
    character_data = {
        "id": char_id,
        "name": "Raven",
        "faction": "Anarchisten",
        "trademarks": {
            "Codeslinger": {
                "name": "Codeslinger",
                "triggers": ["Hacking", "Security systems", "Computers"]
            }
        }
    }
    
    print(f"\nCharakter speichern: {char_db.save(character_data)}")
    
    # Game-State-Manager initialisieren
    gsm = GameStateManager()
    
    # Neues Spiel erstellen
    game_state = gsm.new_game(char_id)
    print(f"\nNeues Spiel erstellt mit ID: {game_state.id}")
    
    # Game-State aktualisieren
    game_state.current_scene = {
        "name": "The Bar",
        "description": "Ein düsterer Ort mit vielen zwielichtigen Gestalten.",
        "npcs": ["Barkeeper", "Schmuggler"]
    }
    
    # Ereignis zur Historie hinzufügen
    gsm.add_event_to_history("Charakter betritt die Bar")
    
    # Spiel speichern
    print(f"Spiel speichern: {gsm.save_game()}")
    
    # Sitzungsdaten aktualisieren
    session.set_session_value("active_game_state_id", game_state.id)
    session.set_session_value("active_character_id", char_id)
    
    print(f"\nAktive Spiel-ID in Sitzung: {session.get_session_value('active_game_state_id')}")
    
    # Alle gespeicherten Spiele anzeigen
    saved_games = gsm.get_saved_games()
    print("\nGespeicherte Spiele:")
    for game in saved_games:
        print(f"  - {game['id']} (Charakter: {game['active_character_id']}, Szene: {game['last_scene']})")
    
    # Spiel unter neuem Namen speichern
    print(f"\nSpiel als 'mein-erstes-spiel' speichern: {gsm.save_game_as('mein-erstes-spiel')}")
    
    # Alle gespeicherten Spiele erneut anzeigen
    saved_games = gsm.get_saved_games()
    print("\nGespeicherte Spiele nach 'save as':")
    for game in saved_games:
        print(f"  - {game['id']} (Charakter: {game['active_character_id']}, Szene: {game['last_scene']})")
    
    # Aufräumen (für den Test)
    print("\nAufräumen...")
    for game in saved_games:
        gsm.delete_game(game['id'])
    
    char_db.delete(char_id)
    
    # Sitzung löschen
    session.clear_session()
    
    print("\nDatenbankbeispiel abgeschlossen.")

if __name__ == "__main__":
    main()