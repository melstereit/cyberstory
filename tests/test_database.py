import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.json_database import JSONDatabase
from data.game_state import GameState, GameStateManager
from data.session_handler import SessionHandler
from data.config_handler import ConfigHandler
from character.manager import CharacterManager

def test_database():
    print("\n=== Datenbank-Test ===")
    
    # 1. Konfigurations-Handler testen
    print("\n1. Konfigurations-Handler:")
    config = ConfigHandler()
    
    print(f"Terminal-Breite: {config.get('ui.terminal_width')}")
    print(f"Animation Speed: {config.get('ui.animation_speed')}")
    
    # Konfiguration ändern
    config.set("ui.terminal_width", 100)
    print(f"Neue Terminal-Breite: {config.get('ui.terminal_width')}")
    
    # 2. Sitzungs-Handler testen
    print("\n2. Sitzungs-Handler:")
    session = SessionHandler()
    
    session.set_session_value("test_value", "Dies ist ein Test")
    print(f"Sitzungswert: {session.get_session_value('test_value')}")
    
    # 3. GameStateManager testen
    print("\n3. GameStateManager:")
    gsm = GameStateManager()
    
    # Verwende die Charakter-ID von test_character.py, falls verfügbar
    char_manager = CharacterManager()
    characters = char_manager.get_all_characters()
    
    if characters:
        char_id = characters[0]["id"]
        
        # Spiel erstellen
        game_state = gsm.new_game(char_id)
        game_id = game_state.id
        print(f"Neues Spiel erstellt: {game_id}")
        
        # Spielzustand ändern
        game_state.current_scene = {
            "name": "The Bar",
            "description": "Ein düsterer Ort mit vielen zwielichtigen Gestalten."
        }
        
        # Ereignisse zur Historie hinzufügen
        gsm.add_event_to_history("Charakter betritt die Bar")
        gsm.add_event_to_history("Charakter spricht mit dem Barkeeper")
        
        # Spielstand speichern
        gsm.save_game()
        print("Spielstand gespeichert")
        
        # Gespeicherte Spiele auflisten
        saved_games = gsm.get_saved_games()
        print(f"Gespeicherte Spiele: {len(saved_games)}")
        
        for game in saved_games:
            print(f"- {game['id']} (Charakter: {game['active_character_id']})")
    else:
        print("Keine Charaktere gefunden. Führe zuerst test_character.py aus.")
    
    print("\nTest abgeschlossen.")

if __name__ == "__main__":
    test_database()