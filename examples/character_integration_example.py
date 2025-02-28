# main.py
import os

from cyberstory import LLMInterface

from cyberstory import CharacterCreation
from cyberstory import GearManager
from cyberstory import CharacterLLMIntegration
from cyberstory import CharacterManager
from cyberstory import TemplateManager
from cyberstory import CheckManager
from cyberstory import NCODiceSystem
from cyberstory import CharacterCreationUI
from cyberstory import CharacterDisplay
from cyberstory import TerminalUI


def main():
    # Terminal-UI erstellen
    ui = TerminalUI()
    
    # LLM-Interface initialisieren
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        ui.display_text("Kein API-Schlüssel gefunden. Bitte setze die Umgebungsvariable GOOGLE_API_KEY.")
        return
    
    llm = LLMInterface(api_key=api_key)
    
    # Charakterverwaltung erstellen
    character_manager = CharacterManager()
    template_manager = TemplateManager()
    gear_manager = GearManager()
    
    # LLM-Integration erstellen
    llm_integration = CharacterLLMIntegration(llm)
    
    # Charaktererstellung erstellen
    character_creation = CharacterCreation(character_manager, template_manager, gear_manager)
    
    # Würfelsystem erstellen
    dice_system = NCODiceSystem()
    check_manager = CheckManager(dice_system)
    
    # UIs erstellen
    character_creation_ui = CharacterCreationUI(ui, character_creation)
    character_display = CharacterDisplay(ui)
    
    # Hauptmenü
    while True:
        ui.clear_screen()
        ui.display_title("NEON CITY OVERDRIVE: TERMINAL EDITION")
        
        options = [
            "Neuen Charakter erstellen",
            "Charaktere anzeigen",
            "Spiel starten",
            "Beenden"
        ]
        
        choice = ui.get_choice("Hauptmenü:", options)
        
        if choice == 0:  # Neuen Charakter erstellen
            character_creation_ui.start_creation()
        
        elif choice == 1:  # Charaktere anzeigen
            characters = character_manager.get_all_characters()
            selected_id = character_display.display_character_list(characters)
            
            if selected_id:
                character_data = character_manager.get_character(selected_id)
                character_display.display_character_sheet(character_data)
        
        elif choice == 2:  # Spiel starten
            # Charakter auswählen
            characters = character_manager.get_all_characters()
            
            if not characters:
                ui.display_text("Keine Charaktere vorhanden. Bitte erstelle zuerst einen Charakter.")
                ui.display_text("\nDrücke Enter, um fortzufahren...")
                input()
                continue
            
            selected_id = character_display.display_character_list(characters)
            
            if selected_id:
                # Hier würde die Spielimplementierung beginnen
                # Dies ist für die nächste Phase vorgesehen
                ui.clear_screen()
                ui.display_title("SPIEL STARTEN")
                ui.display_text("Spielimplementierung noch nicht verfügbar in dieser Phase.")
                ui.display_text("\nDrücke Enter, um fortzufahren...")
                input()
        
        elif choice == 3:  # Beenden
            break

if __name__ == "__main__":
    main()