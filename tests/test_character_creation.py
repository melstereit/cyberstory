import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.terminal import TerminalUI
from character.manager import CharacterManager
from character.templates import TemplateManager
from character.creation import CharacterCreation
from character.gear_manager import GearManager
from ui.character_creation_ui import CharacterCreationUI

def test_character_creation():
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

if __name__ == "__main__":
    test_character_creation()