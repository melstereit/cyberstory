# main.py (überarbeitete Version mit Datenbankintegration)
import os

from cyberstory import *


def main():
    # Konfigurations-Handler initialisieren
    config = ConfigHandler()
    
    # Sitzungs-Handler initialisieren
    session = SessionHandler()
    
    # Terminal-UI erstellen
    terminal_width = config.get("ui.terminal_width", 80)
    ui = TerminalUI(width=terminal_width)
    
    # LLM-Interface initialisieren
    api_key = config.get("api_key") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        ui.display_text("Kein API-Schlüssel gefunden. Bitte setze die Umgebungsvariable GOOGLE_API_KEY.")
        return
    
    model = config.get("model", "gemini-2.0-flash")
    llm = LLMInterface(api_key=api_key, model=model)
    
    # Datenverzeichnisse aus der Konfiguration
    char_dir = config.get("data_dirs.characters", "data/characters")
    template_dir = config.get("data_dirs.templates", "data/templates")
    
    # Charakterverwaltung erstellen
    character_manager = CharacterManager(char_dir)
    template_manager = TemplateManager(template_dir)
    gear_manager = GearManager(f"{template_dir}/gear.json")
    
    # LLM-Integration erstellen
    llm_integration = CharacterLLMIntegration(llm)
    
    # Charaktererstellung erstellen
    character_creation = CharacterCreation(character_manager, template_manager, gear_manager)
    
    # Würfelsystem erstellen
    dice_system = NCODiceSystem()
    check_manager = CheckManager(dice_system)
    
    # Game-State-Manager erstellen
    game_state_manager = GameStateManager(config.get("data_dirs.game_states", "data/game_states"))
    
    # UIs erstellen
    character_creation_ui = CharacterCreationUI(ui, character_creation)
    character_display = CharacterDisplay(ui)
    
    # Lade aktiven Spielzustand, falls vorhanden
    active_game_id = session.get_session_value("active_game_state_id")
    if active_game_id:
        game_state_manager.load_game(active_game_id)
    
    # Hauptmenü
    while True:
        ui.clear_screen()
        ui.display_title("NEON CITY OVERDRIVE: TERMINAL EDITION")
        
        options = [
            "Neuen Charakter erstellen",
            "Charaktere anzeigen",
            "Spiel starten",
            "Spielstand laden",
            "Spielstand speichern",
            "Einstellungen",
            "Beenden"
        ]
        
        choice = ui.get_choice("Hauptmenü:", options)
        
        if choice == 0:  # Neuen Charakter erstellen
            character_data = character_creation_ui.start_creation()
            
            if character_data:
                # Aktiven Charakter in der Sitzung speichern
                session.set_session_value("active_character_id", character_data.get("id"))
                
                # Neues Spiel starten
                if ui.get_yes_no("Möchtest du mit diesem Charakter ein neues Spiel starten?"):
                    game_state = game_state_manager.new_game(character_data.get("id"))
                    session.set_session_value("active_game_state_id", game_state.id)
        
        elif choice == 1:  # Charaktere anzeigen
            characters = character_manager.get_all_characters()
            selected_id = character_display.display_character_list(characters)
            
            if selected_id:
                character_data = character_manager.get_character(selected_id)
                character_display.display_character_sheet(character_data)
                
                # Charakter als aktiv setzen
                if ui.get_yes_no("Möchtest du diesen Charakter verwenden?"):
                    session.set_session_value("active_character_id", selected_id)
        
        elif choice == 2:  # Spiel starten
            # Aktiven Charakter prüfen
            char_id = session.get_session_value("active_character_id")
            if not char_id:
                # Charakter auswählen
                characters = character_manager.get_all_characters()
                
                if not characters:
                    ui.display_text("Keine Charaktere vorhanden. Bitte erstelle zuerst einen Charakter.")
                    ui.display_text("\nDrücke Enter, um fortzufahren...")
                    input()
                    continue
                
                selected_id = character_display.display_character_list(characters)
                
                if selected_id:
                    char_id = selected_id
                    session.set_session_value("active_character_id", char_id)
                else:
                    continue
            
            # Aktiven Spielzustand prüfen
            game_id = session.get_session_value("active_game_state_id")
            if not game_id:
                # Neues Spiel erstellen
                game_state = game_state_manager.new_game(char_id)
                session.set_session_value("active_game_state_id", game_state.id)
            
            # Hier würde die Spielimplementierung beginnen
            # Dies ist für die nächste Phase vorgesehen
            ui.clear_screen()
            ui.display_title("SPIEL STARTEN")
            ui.display_text("Spielimplementierung noch nicht verfügbar in dieser Phase.")
            ui.display_text("\nDrücke Enter, um fortzufahren...")
            input()
        
        elif choice == 3:  # Spielstand laden
            saved_games = game_state_manager.get_saved_games()
            
            if not saved_games:
                ui.display_text("Keine Spielstände vorhanden.")
                ui.display_text("\nDrücke Enter, um fortzufahren...")
                input()
                continue
            
            options = [f"{game['id']} - Charakter: {game['active_character_id']}" for game in saved_games]
            game_choice = ui.get_choice("Wähle einen Spielstand:", options)
            
            if 0 <= game_choice < len(saved_games):
                game_id = saved_games[game_choice]["id"]
                game_state = game_state_manager.load_game(game_id)
                
                if game_state:
                    ui.display_text(f"Spielstand '{game_id}' geladen.")
                    session.set_session_value("active_game_state_id", game_id)
                    session.set_session_value("active_character_id", game_state.active_character_id)
                else:
                    ui.display_text(f"Fehler beim Laden des Spielstands '{game_id}'.")
                
                ui.display_text("\nDrücke Enter, um fortzufahren...")
                input()
        
        elif choice == 4:  # Spielstand speichern
            game_id = session.get_session_value("active_game_state_id")
            
            if not game_id or not game_state_manager.active_game_state:
                ui.display_text("Kein aktives Spiel vorhanden.")
                ui.display_text("\nDrücke Enter, um fortzufahren...")
                input()
                continue
            
            save_name = ui.get_input("Gib einen Namen für den Spielstand ein (leer für aktuellen Namen):")
            
            if save_name:
                success = game_state_manager.save_game_as(save_name)
                if success:
                    ui.display_text(f"Spielstand als '{save_name}' gespeichert.")
                    session.set_session_value("active_game_state_id", save_name)
                else:
                    ui.display_text(f"Fehler beim Speichern des Spielstands als '{save_name}'.")
            else:
                success = game_state_manager.save_game()
                if success:
                    ui.display_text(f"Spielstand '{game_id}' gespeichert.")
                else:
                    ui.display_text(f"Fehler beim Speichern des Spielstands '{game_id}'.")
            
            ui.display_text("\nDrücke Enter, um fortzufahren...")
            input()
        
        elif choice == 5:  # Einstellungen
            ui.clear_screen()
            ui.display_title("EINSTELLUNGEN")
            
            options = [
                f"Terminalbreite: {config.get('ui.terminal_width')}",
                f"Animationsgeschwindigkeit: {config.get('ui.animation_speed')}",
                f"API-Schlüssel: {'*****' + api_key[-4:] if api_key else 'Nicht gesetzt'}",
                f"Modell: {config.get('model')}"
            ]
            
            setting_choice = ui.get_choice("Wähle eine Einstellung zum Ändern:", options)
            
            if setting_choice == 0:  # Terminalbreite
                width = ui.get_input("Neue Terminalbreite (60-120):")
                try:
                    width = int(width)
                    if 60 <= width <= 120:
                        config.set("ui.terminal_width", width)
                        ui.width = width
                except ValueError:
                    ui.display_text("Ungültige Eingabe.")
            
            elif setting_choice == 1:  # Animationsgeschwindigkeit
                speed = ui.get_input("Neue Animationsgeschwindigkeit (0.001-0.1):")
                try:
                    speed = float(speed)
                    if 0.001 <= speed <= 0.1:
                        config.set("ui.animation_speed", speed)
                except ValueError:
                    ui.display_text("Ungültige Eingabe.")
            
            elif setting_choice == 2:  # API-Schlüssel
                key = ui.get_input("Neuer API-Schlüssel (leer für unverändert):")
                if key:
                    config.set("api_key", key)
                    api_key = key
                    llm = LLMInterface(api_key=api_key, model=model)
            
            elif setting_choice == 3:  # Modell
                options = ["gemini-2.0-flash", "gemini-2.0-pro", "gemini-1.5-flash"]
                model_choice = ui.get_choice("Wähle ein Modell:", options)
                model = options[model_choice]
                config.set("model", model)
                llm = LLMInterface(api_key=api_key, model=model)
            
            ui.display_text("Einstellungen gespeichert.")
            ui.display_text("\nDrücke Enter, um fortzufahren...")
            input()
        
        elif choice == 6:  # Beenden
            # Letzten Zustand speichern
            if game_state_manager.active_game_state:
                game_state_manager.save_game()
            
            break

if __name__ == "__main__":
    main()