# ui/character_creation_ui.py
from typing import Dict, Any, Optional

from cyberstory.character.creation import CharacterCreation
from cyberstory.ui.terminal import TerminalUI


class CharacterCreationUI:
    """UI für den Charaktererstellungsprozess."""
    
    def __init__(self, terminal_ui: TerminalUI, character_creation: CharacterCreation):
        """
        Initialisiert die Charaktererstellungs-UI.
        
        Args:
            terminal_ui: Instanz der Terminal-UI
            character_creation: Instanz des CharacterCreation-Managers
        """
        self.ui = terminal_ui
        self.creation = character_creation
    
    def start_creation(self) -> Optional[Dict[str, Any]]:
        """
        Startet den Charaktererstellungsprozess.
        
        Returns:
            Dict mit den Charakterdaten oder None bei Abbruch
        """
        self.ui.clear_screen()
        self.ui.display_title("CHARAKTERERSTELLUNG")
        
        # Name und Fraktion
        name = self.ui.get_input("Wie lautet dein Name?")
        if not name:
            self.ui.display_text("Charaktererstellung abgebrochen.")
            return None
        
        factions = ["Corpos", "Anarchisten", "Staatsmacht"]
        faction = self.ui.get_choice("Wähle deine Fraktion:", factions)
        
        # Charakter erstellen
        character = self.creation.start_creation(name, faction)
        
        # Hintergrundgeschichte
        self.ui.display_text("\nErzähle mir etwas über deine Hintergrundgeschichte:")
        background = self.ui.get_multiline_input()
        
        # Trademarks
        self.ui.display_text("\n=== TRADEMARKS ===")
        self.ui.display_text("Trademarks definieren die Vergangenheit, den Beruf, die einzigartigen Talente oder die spezielle Ausrüstung deines Charakters.")
        
        trademark_suggestions = self.creation.suggest_trademarks(background)
        
        # Ersten zwei Trademarks auswählen
        for i in range(2):
            self.ui.display_text(f"\nWähle dein {i+1}. Trademark:")
            options = [f"{tm['name']}: {', '.join(tm['triggers'][:3])}..." for tm in trademark_suggestions]
            choice = self.ui.get_choice("", options)
            
            selected_tm = trademark_suggestions[choice]
            self.ui.display_text(f"\nDu hast {selected_tm['name']} gewählt.")
            
            # Triggers anzeigen und bis zu 3 auswählen
            self.ui.display_text("\nWähle bis zu 3 Trigger für dieses Trademark:")
            trigger_options = selected_tm['triggers']
            selected_triggers = []
            
            for j in range(3):
                options = [t for t in trigger_options if t not in selected_triggers]
                if not options:
                    break
                
                choice = self.ui.get_choice(f"Trigger {j+1}:", options)
                selected_triggers.append(options[choice])
            
            # Trademark hinzufügen
            self.creation.add_trademark_to_character(selected_tm['name'], selected_triggers)
            
            # Edge hinzufügen
            self.ui.display_text(f"\nWähle einen Edge für das Trademark {selected_tm['name']}:")
            edge_options = self.creation.suggest_edges(selected_tm['name'])
            edge_choice = self.ui.get_choice("", edge_options)
            self.creation.add_edge_to_character(edge_options[edge_choice], selected_tm['name'])
        
        # Flaws
        self.ui.display_text("\n=== FLAWS ===")
        self.ui.display_text("Flaws sind Nachteile, Probleme oder Schwierigkeiten, mit denen der Charakter zu kämpfen hat.")
        
        flaw_suggestions = self.creation.suggest_flaws()
        
        # Zwei Flaws auswählen
        for i in range(2):
            self.ui.display_text(f"\nWähle deinen {i+1}. Flaw:")
            options = [f"{flaw['name']}: {flaw['description']}" for flaw in flaw_suggestions]
            choice = self.ui.get_choice("", options)
            
            selected_flaw = flaw_suggestions[choice]
            self.creation.add_flaw_to_character(selected_flaw['name'], selected_flaw['description'])
        
        # Drive
        self.ui.display_text("\n=== DRIVE ===")
        self.ui.display_text("Der Drive ist das, was deinen Charakter antreibt, gefährliche Jobs anzunehmen.")
        
        drive_suggestions = self.creation.suggest_drives()
        options = [drive for drive in drive_suggestions]
        choice = self.ui.get_choice("Wähle deinen Drive:", options)
        
        self.creation.set_drive_for_character(options[choice])
        
        # Ausrüstung
        self.ui.display_text("\n=== AUSRÜSTUNG ===")
        self.ui.display_text("Jeder Charakter kann bis zu vier Gegenstände spezieller Ausrüstung besitzen.")
        
        # Für jedes Trademark Ausrüstung vorschlagen
        character_data = self.creation.character_manager.get_character(self.creation.current_character_id)
        trademarks = character_data.get("trademarks", {})
        
        for tm_name in trademarks:
            gear_suggestions = self.creation.suggest_gear(tm_name)
            
            self.ui.display_text(f"\nWähle Ausrüstung basierend auf deinem Trademark '{tm_name}':")
            options = [f"{gear['name']}: {', '.join(gear['tags'])}" for gear in gear_suggestions]
            
            # Optional weitere Ausrüstung hinzufügen
            if self.ui.get_yes_no("Möchtest du spezielle Ausrüstung für dieses Trademark?"):
                choice = self.ui.get_choice("", options)
                selected_gear = gear_suggestions[choice]
                
                # Würfelwurf für das Gear
                self.ui.display_text(f"\nWürfelwurf für {selected_gear['name']} mit {len(selected_gear['tags'])} Tags...")
                success = self.creation.roll_for_gear(selected_gear['name'], "", selected_gear['tags'])
                
                if success:
                    self.ui.display_text(f"Erfolg! Du erhältst {selected_gear['name']}.")
                else:
                    self.ui.display_text(f"Misserfolg! Du erhältst {selected_gear['name']} nicht.")
        
        # Abschluss
        character_data = self.creation.complete_creation()
        
        self.ui.clear_screen()
        self.ui.display_title("CHARAKTERERSTELLUNG ABGESCHLOSSEN")
        self.display_character_summary(character_data)
        
        return character_data
    
    def display_character_summary(self, character_data: Dict[str, Any]) -> None:
        """
        Zeigt eine Zusammenfassung des erstellten Charakters an.
        
        Args:
            character_data: Die Charakterdaten
        """
        self.ui.display_text(f"Name: {character_data.get('name')}")
        self.ui.display_text(f"Fraktion: {character_data.get('faction')}")
        
        # Trademarks
        self.ui.display_text("\n=== TRADEMARKS ===")
        for name, tm in character_data.get("trademarks", {}).items():
            self.ui.display_text(f"{name}: {', '.join(tm.get('triggers', []))}")
        
        # Edges
        self.ui.display_text("\n=== EDGES ===")
        for edge in character_data.get("edges", []):
            self.ui.display_text(f"{edge.get('name')} ({edge.get('trademark')})")
        
        # Flaws
        self.ui.display_text("\n=== FLAWS ===")
        for flaw in character_data.get("flaws", []):
            self.ui.display_text(f"{flaw.get('name')}: {flaw.get('description')}")
        
        # Drive
        self.ui.display_text("\n=== DRIVE ===")
        drive = character_data.get("drive", {})
        if drive:
            self.ui.display_text(drive.get("description", ""))
        
        # Ausrüstung
        self.ui.display_text("\n=== AUSRÜSTUNG ===")
        for item in character_data.get("inventory", []):
            if item.get("is_special"):
                self.ui.display_text(f"{item.get('name')}: {', '.join(item.get('tags', []))}")
            else:
                self.ui.display_text(item.get("name", ""))
        
        # Stunt Points und Hits
        self.ui.display_text(f"\nStunt Points: {character_data.get('stunt_points', 0)}/{character_data.get('max_stunt_points', 3)}")
        hit_track = character_data.get("hit_track", [])
        hits = sum(1 for hit in hit_track if hit)
        self.ui.display_text(f"Hits: {hits}/{len(hit_track)}")
        
        self.ui.display_text("\nDrücke Enter, um fortzufahren...")
        input()