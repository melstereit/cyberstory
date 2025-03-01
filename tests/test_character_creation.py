import sys
import os
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Füge das Projekt-Stammverzeichnis zum Python-Pfad hinzu
sys.path.insert(0, str(Path(__file__).parent.parent))

from cyberstory.ui.terminal import TerminalUI
from cyberstory.character.manager import CharacterManager
from cyberstory.character.templates import TemplateManager
from cyberstory.character.creation import CharacterCreation
from cyberstory.character.gear_manager import GearManager
from cyberstory.ui.character_creation_ui import CharacterCreationUI


class TestCharacterCreation(unittest.TestCase):
    """Tests für die Charaktererstellungsfunktionalität."""
    
    def setUp(self):
        """Richtet die Testumgebung ein."""
        self.ui = MagicMock(spec=TerminalUI)
        self.char_manager = CharacterManager()
        self.template_manager = TemplateManager()
        self.gear_manager = GearManager()
        
        # Erstelle den CharacterCreation-Manager
        self.creation = CharacterCreation(
            self.char_manager, 
            self.template_manager, 
            self.gear_manager
        )
        
        # Erstelle die UI für die Charaktererstellung
        self.creation_ui = CharacterCreationUI(self.ui, self.creation)
    
    def test_creation_start(self):
        """Testet, ob ein Charakter erstellt werden kann."""
        # Mocke die UI-Interaktionen
        self.ui.get_input.return_value = "Test Character"
        self.ui.get_choice.return_value = 0  # Wähle immer die erste Option
        self.ui.get_multiline_input.return_value = "This is a test character background."
        self.ui.get_yes_no.return_value = False  # Keine zusätzliche Ausrüstung
        
        # Rufe das zu testende Modul auf - aber mit patch, um die Eingabeaufforderung zu unterdrücken
        with patch('builtins.input', return_value=''):
            character_data = self.creation.start_creation("Test Character", "Anarchisten")
        
        # Überprüfungen
        self.assertIsNotNone(character_data)
        self.assertEqual(character_data.get("name"), "Test Character")
        self.assertEqual(character_data.get("faction"), "Anarchisten")
    
    def test_trademark_suggestions(self):
        """Testet, ob Trademark-Vorschläge generiert werden können."""
        background = "I was a hacker in the corporate world before going rogue."
        suggestions = self.creation.suggest_trademarks(background, count=3)
        
        # Überprüfungen
        self.assertIsNotNone(suggestions)
        self.assertIsInstance(suggestions, list)
        self.assertTrue(len(suggestions) <= 3)
        
        # Prüfe Struktur des ersten Vorschlags, falls vorhanden
        if suggestions:
            first_suggestion = suggestions[0]
            self.assertIn("name", first_suggestion)
            self.assertIn("triggers", first_suggestion)
    
    def test_add_trademark_to_character(self):
        """Testet, ob ein Trademark einem Charakter hinzugefügt werden kann."""
        # Erstelle zuerst einen Charakter
        char_data = self.creation.start_creation("Test Character", "Anarchisten")
        
        # Füge ein Trademark hinzu
        trademark_name = "Codeslinger"
        triggers = ["Hacking", "Security systems", "Computers"]
        result = self.creation.add_trademark_to_character(trademark_name, triggers)
        
        # Überprüfungen
        self.assertTrue(result)
        char_data = self.char_manager.get_character(self.creation.current_character_id)
        trademarks = char_data.get("trademarks", {})
        self.assertIn(trademark_name, trademarks)
        trademark = trademarks[trademark_name]
        self.assertEqual(trademark.get("name"), trademark_name)
        self.assertEqual(trademark.get("triggers"), triggers)
    
    # Weitere Test-Methoden könnten hier hinzugefügt werden...


def manual_test_character_creation():
    """
    Manuelle Testfunktion für die interaktive Charaktererstellung.
    Diese Funktion wird nicht automatisch ausgeführt, wenn die Datei als unittest ausgeführt wird,
    sondern muss explizit aufgerufen werden.
    """
    # UI initialisieren
    ui = TerminalUI()
    
    # Manager initialisieren
    char_manager = CharacterManager()
    template_manager = TemplateManager()
    gear_manager = GearManager()
    
    # Charaktererstellung initialisieren
    creation = CharacterCreation(char_manager, template_manager, gear_manager)
    
    # UI für die Charaktererstellung
    creation_ui = CharacterCreationUI(ui, creation)
    
    # Charaktererstellungsprozess starten
    creation_ui.start_creation()


# Diese Funktion wird aufgerufen, wenn die Datei direkt ausgeführt wird
if __name__ == "__main__":
    # Wenn die Datei direkt ausgeführt wird, führe entweder den manuellen Test aus...
    # manual_test_character_creation()
    
    # ...oder führe die unittest-Tests aus
    unittest.main()