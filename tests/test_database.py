import sys
import os
import unittest
from pathlib import Path

# Füge das Projekt-Stammverzeichnis zum Python-Pfad hinzu
sys.path.insert(0, str(Path(__file__).parent.parent))

from cyberstory.data.json_database import JSONDatabase
from cyberstory.data.game_state import GameState, GameStateManager
from cyberstory.data.session_handler import SessionHandler
from cyberstory.data.config_handler import ConfigHandler
from cyberstory.character.manager import CharacterManager


class TestDatabase(unittest.TestCase):
    """Tests für die Datenbankfunktionalitäten."""
    
    def setUp(self):
        """Richtet die Testumgebung ein."""
        # Testverzeichnis für temporäre Dateien
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Initialisiere Testdaten
        self.test_data = {"id": "test1", "name": "Test Data", "value": 42}
    
    def tearDown(self):
        """Räumt die Testumgebung auf."""
        # Lösche Testdateien, wenn vorhanden
        if os.path.exists(f"{self.test_dir}/test1.json"):
            os.remove(f"{self.test_dir}/test1.json")
        
        # Verzeichnis löschen, wenn es leer ist
        try:
            os.rmdir(self.test_dir)
        except OSError:
            # Verzeichnis ist nicht leer, ignoriere den Fehler
            pass
    
    def test_json_database_save_load(self):
        """Testet das Speichern und Laden von JSON-Daten."""
        db = JSONDatabase(self.test_dir)
        
        # Speichern
        result = db.save(self.test_data)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(f"{self.test_dir}/test1.json"))
        
        # Laden
        loaded_data = db.load("test1")
        self.assertIsNotNone(loaded_data)
        self.assertEqual(loaded_data["id"], "test1")
        self.assertEqual(loaded_data["name"], "Test Data")
        self.assertEqual(loaded_data["value"], 42)
    
    def test_json_database_update(self):
        """Testet das Aktualisieren von JSON-Daten."""
        db = JSONDatabase(self.test_dir)
        
        # Zuerst speichern
        db.save(self.test_data)
        
        # Dann aktualisieren
        updates = {"value": 99, "new_field": "New Value"}
        result = db.update("test1", updates)
        self.assertTrue(result)
        
        # Überprüfen
        loaded_data = db.load("test1")
        self.assertEqual(loaded_data["value"], 99)
        self.assertEqual(loaded_data["new_field"], "New Value")
        self.assertEqual(loaded_data["name"], "Test Data")  # Unverändert
    
    def test_json_database_delete(self):
        """Testet das Löschen von JSON-Daten."""
        db = JSONDatabase(self.test_dir)
        
        # Zuerst speichern
        db.save(self.test_data)
        self.assertTrue(os.path.exists(f"{self.test_dir}/test1.json"))
        
        # Dann löschen
        result = db.delete("test1")
        self.assertTrue(result)
        self.assertFalse(os.path.exists(f"{self.test_dir}/test1.json"))
    
    def test_config_handler(self):
        """Testet den Konfigurations-Handler."""
        config_file = f"{self.test_dir}/config.json"
        config = ConfigHandler(config_file)
        
        # Standard-Wert auslesen
        width = config.get("ui.terminal_width")
        self.assertEqual(width, 80)
        
        # Wert ändern
        config.set("ui.terminal_width", 100)
        self.assertEqual(config.get("ui.terminal_width"), 100)
        
        # Datei sollte existieren
        self.assertTrue(os.path.exists(config_file))
    
    def test_session_handler(self):
        """Testet den Sitzungs-Handler."""
        session_file = f"{self.test_dir}/session.json"
        session = SessionHandler(session_file)
        
        # Wert setzen
        session.set_session_value("test_value", "Dies ist ein Test")
        self.assertEqual(session.get_session_value("test_value"), "Dies ist ein Test")
        
        # Datei sollte existieren
        self.assertTrue(os.path.exists(session_file))
    
    @unittest.skip("Erfordert vorhandene Charaktere in der Datenbank")
    def test_game_state_manager(self):
        """Testet den GameStateManager (wird übersprungen, wenn keine Charaktere vorhanden sind)."""
        # Verwende ein eigenes Verzeichnis für GameStates
        gsm = GameStateManager(f"{self.test_dir}/game_states")
        
        # Hole einen Charakter, falls vorhanden
        char_manager = CharacterManager()
        characters = char_manager.get_all_characters()
        
        if not characters:
            self.skipTest("Keine Charaktere gefunden. Führe zuerst test_character.py aus.")
        
        char_id = characters[0]["id"]
        
        # Spiel erstellen
        game_state = gsm.new_game(char_id)
        game_id = game_state.id
        self.assertIsNotNone(game_id)
        
        # Spielzustand ändern
        game_state.current_scene = {
            "name": "The Bar",
            "description": "Ein düsterer Ort mit vielen zwielichtigen Gestalten."
        }
        
        # Ereignisse zur Historie hinzufügen
        gsm.add_event_to_history("Charakter betritt die Bar")
        gsm.add_event_to_history("Charakter spricht mit dem Barkeeper")
        
        # Spielstand speichern
        result = gsm.save_game()
        self.assertTrue(result)
        
        # Gespeicherte Spiele auflisten
        saved_games = gsm.get_saved_games()
        self.assertGreater(len(saved_games), 0)
        
        # Spielstand laden
        loaded_game = gsm.load_game(game_id)
        self.assertIsNotNone(loaded_game)
        self.assertEqual(loaded_game.id, game_id)
        self.assertEqual(loaded_game.active_character_id, char_id)
        
        # Spielstand löschen
        result = gsm.delete_game(game_id)
        self.assertTrue(result)


def manual_test_database():
    """
    Manuelle Testfunktion für die Datenbankfunktionalitäten.
    Diese Funktion wird nicht automatisch ausgeführt, wenn die Datei als unittest ausgeführt wird,
    sondern muss explizit aufgerufen werden.
    """
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


# Diese Funktion wird aufgerufen, wenn die Datei direkt ausgeführt wird
if __name__ == "__main__":
    # Wenn die Datei direkt ausgeführt wird, führe entweder den manuellen Test aus...
    # manual_test_database()
    
    # ...oder führe die unittest-Tests aus
    unittest.main()