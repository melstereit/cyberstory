# cyberstory/gameplay/manager.py
from typing import Dict, Any, List, Optional

from cyberstory.character.manager import CharacterManager
from cyberstory.data.game_state import GameStateManager
from cyberstory.mechanics.check_manager import CheckManager
from cyberstory.ai.gameplay_integration import LLMGameplayIntegration
from cyberstory.ui.terminal import TerminalUI
from cyberstory.ui.character_display import CharacterDisplay


class GameplayManager:
    """Verwaltet den Spielablauf."""
    
    def __init__(self, 
                 character_manager: CharacterManager, 
                 game_state_manager: GameStateManager, 
                 check_manager: CheckManager, 
                 llm_integration: LLMGameplayIntegration, 
                 ui: TerminalUI):
        """
        Initialisiert den GameplayManager.
        
        Args:
            character_manager: Instanz des CharacterManagers
            game_state_manager: Instanz des GameStateManagers
            check_manager: Instanz des CheckManagers
            llm_integration: Instanz der LLMGameplayIntegration
            ui: Instanz der UI
        """
        self.character_manager = character_manager
        self.game_state_manager = game_state_manager
        self.check_manager = check_manager
        self.llm_integration = llm_integration
        self.ui = ui
        
        # Aktueller Spielzustand
        self.current_game_state = None
        self.current_character_data = None
        
        # Anzeigen für den Charakterstatus
        self.character_display = CharacterDisplay(ui)
    
    def start_game(self, game_state_id: Optional[str], character_id: str) -> bool:
        """
        Startet ein Spiel.
        
        Args:
            game_state_id: ID des Spielzustands oder None für ein neues Spiel
            character_id: ID des zu verwendenden Charakters
        
        Returns:
            bool: True, wenn das Spiel erfolgreich gestartet wurde, sonst False
        """
        # Lade den Charakter
        self.current_character_data = self.character_manager.get_character(character_id)
        if not self.current_character_data:
            self.ui.display_text("Fehler: Charakter konnte nicht geladen werden.")
            return False
        
        # Lade oder erstelle den Spielzustand
        if game_state_id:
            self.current_game_state = self.game_state_manager.load_game(game_state_id)
            if not self.current_game_state:
                self.ui.display_text(f"Fehler: Spielzustand {game_state_id} konnte nicht geladen werden.")
                return False
        else:
            self.current_game_state = self.game_state_manager.new_game(character_id)
        
        # Starte den Game Loop
        return self.game_loop()
    
    def game_loop(self) -> bool:
        """
        Hauptschleife des Spiels.
        
        Returns:
            bool: True, wenn das Spiel erfolgreich beendet wurde, sonst False
        """
        self.ui.clear_screen()
        self.ui.display_title("NEON CITY OVERDRIVE")
        
        # Kurzübersicht des Charakters anzeigen
        self.character_display.display_character_summary(self.current_character_data)
        self.ui.display_text("\nDrücke Enter, um zu beginnen...")
        input()
        
        # Überprüfe, ob eine aktuelle Szene existiert, sonst generiere eine neue
        if not self.current_game_state.current_scene:
            self.ui.display_text("Generiere neue Szene...")
            scene = self.llm_integration.generate_scene(
                self.current_game_state.to_dict(), 
                self.current_character_data
            )
            self.current_game_state.current_scene = scene
            self.game_state_manager.save_game()
        
        # Überprüfe, ob eine aktuelle Quest existiert, sonst generiere eine neue
        if not self.current_game_state.quest_data:
            self.ui.display_text("Generiere neue Quest...")
            quest = self.llm_integration.generate_quest(
                self.current_game_state.to_dict(), 
                self.current_character_data
            )
            self.current_game_state.quest_data = quest
            self.game_state_manager.save_game()
        
        # Hauptspielschleife
        while True:
            # Zeige die aktuelle Szene an
            self._display_current_scene()
            
            # Zeige den Charakterstatus an
            self.character_display.display_character_summary(self.current_character_data)
            
            # Hole die Spieleraktion
            action_text = self.ui.get_input("Was möchtest du tun?")
            
            # Beenden-Option
            if action_text.lower() in ["beenden", "quit", "exit"]:
                if self.ui.get_yes_no("Möchtest du das Spiel wirklich beenden?"):
                    self.game_state_manager.save_game()
                    return True
                else:
                    continue
            
            # Charakterblatt-Option
            if action_text.lower() in ["character", "charakter", "stats", "blatt"]:
                self.character_display.display_character_sheet(self.current_character_data)
                continue
            
            # Quest-Option
            if action_text.lower() in ["quest", "auftrag", "mission"]:
                self._display_current_quest()
                continue
            
            # Hilfe-Option
            if action_text.lower() in ["hilfe", "help", "?"]:
                self._display_help()
                continue
            
            # Verarbeite die Aktion
            self.ui.display_text("\nVerarbeite deine Aktion...")
            action_result = self.llm_integration.process_player_action(
                self.current_game_state.to_dict(),
                self.current_character_data,
                action_text
            )
            
            # Dieser Flag wird gesetzt, wenn wir die Szene aktualisieren, um anzuzeigen, 
            # dass wir beim nächsten Schleifendurchlauf nicht neu anzeigen müssen
            scene_updated = False
            
            # Führe einen Würfelwurf durch, falls erforderlich
            if action_result.get("requires_check", False):
                check_context = action_result.get("check_context", {})
                
                self.ui.display_text(f"\nDu versuchst: {check_context.get('action', 'eine Aktion')}")
                
                # Führe den Check durch
                check_result = self.check_manager.perform_check(
                    self.current_character_data,
                    check_context
                )
                
                # Zeige das Würfelergebnis an
                self._display_check_result(check_result)
                
                # Generiere Konsequenzen
                self.ui.display_text("\nGeneriere Konsequenzen...")
                consequences = self.llm_integration.generate_consequences(
                    self.current_game_state.to_dict(),
                    self.current_character_data,
                    check_result,
                    action_text
                )
                
                # Zeige die Konsequenzen an
                self.ui.display_subtitle("Konsequenzen")
                self.ui.display_text(consequences.get("description", ""))
                
                # Aktualisiere den Spielzustand und Charakter
                self._update_game_state(consequences)
                self._update_character(consequences)
                
                # Speichern nach der Aktualisierung
                self.game_state_manager.save_game()
                
                # Aktualisiere die Daten
                self.current_character_data = self.character_manager.get_character(self.current_character_data["id"])
                
                # Markiere die Szene als aktualisiert
                scene_updated = True
                
            else:
                # Direkte Antwort ohne Würfelwurf
                response = action_result.get("response", "")
                self.ui.display_text("\n" + response)
                
                # Aktualisiere den Spielzustand, falls notwendig
                if "state_update" in action_result:
                    self._update_direct(action_result["state_update"])
                    
                    # Speichern nach der Aktualisierung
                    self.game_state_manager.save_game()
                    
                    # Aktualisiere die Daten
                    self.current_character_data = self.character_manager.get_character(self.current_character_data["id"])
                    
                    # Markiere die Szene als aktualisiert
                    scene_updated = True
                
                # Wenn es keine state_update gibt, füge die Antwort als letztes Ereignis hinzu
                else:
                    self.current_game_state.current_scene["letztes_ereignis"] = response
                    self.current_game_state.add_to_history(response[:100] + "..." if len(response) > 100 else response)
                    self.game_state_manager.save_game()
                    scene_updated = True
            
            # Warte auf Benutzereingabe, bevor fortfahren
            self.ui.display_text("\nDrücke Enter, um fortzufahren...")
            input()
            
            # Prüfe, ob die Szene abgeschlossen ist
            scene_completed = self.current_game_state.current_scene.get("completed", False)
            
            if scene_completed:
                self.ui.display_text("\nDie Szene ist abgeschlossen.")
                self.ui.display_text("Drücke Enter, um fortzufahren...")
                input()
                
                if self._is_game_completed():
                    self._end_game()
                    return True
                else:
                    # Generiere die nächste Szene
                    self.ui.display_text("Generiere neue Szene...")
                    scene = self.llm_integration.generate_scene(
                        self.current_game_state.to_dict(), 
                        self.current_character_data
                    )
                    self.current_game_state.current_scene = scene
                    self.game_state_manager.save_game()
                    scene_updated = False  # Neue Szene muss angezeigt werden
            
            # Optional: Wenn die Szene aktualisiert wurde, zeige sie sofort an,
            # anstatt auf den nächsten Schleifendurchlauf zu warten
            if scene_updated:
                self._display_current_scene()
                self.character_display.display_character_summary(self.current_character_data)
    
    def _display_current_scene(self) -> None:
        """Zeigt die aktuelle Szene an."""
        self.ui.clear_screen()
        
        scene = self.current_game_state.current_scene
        
        # Sicherstellen, dass die Szene existiert
        if not scene:
            self.ui.display_title("KEINE SZENE VERFÜGBAR")
            self.ui.display_text("Es ist keine aktive Szene vorhanden.")
            return
        
        self.ui.display_title(scene.get("name", "Aktuelle Szene"))
        self.ui.display_text(scene.get("description", ""))
        
        # Zeige zusätzliche Informationen an
        # Prüfen, ob der Wert ein Wörterbuch oder eine Liste ist
        characters = scene.get("characters", [])
        if isinstance(characters, list) and characters:
            self.ui.display_subtitle("Personen")
            for char in characters:
                if isinstance(char, dict):
                    self.ui.display_text(f"- {char.get('name', '')}: {char.get('description', '')}")
                else:
                    self.ui.display_text(f"- {char}")
        
        objects = scene.get("objects", [])
        if isinstance(objects, list) and objects:
            self.ui.display_subtitle("Objekte")
            for obj in objects:
                if isinstance(obj, dict):
                    self.ui.display_text(f"- {obj.get('name', '')}: {obj.get('description', '')}")
                else:
                    self.ui.display_text(f"- {obj}")
        
        threats = scene.get("threats", [])
        if isinstance(threats, list) and threats:
            self.ui.display_subtitle("Bedrohungen")
            for threat in threats:
                if isinstance(threat, dict):
                    self.ui.display_text(f"- {threat.get('name', '')}: {threat.get('description', '')}")
                else:
                    self.ui.display_text(f"- {threat}")
        
        # Zusätzliche dynamische Elemente der Szene anzeigen
        for key, value in scene.items():
            # Ignoriere bereits verarbeitete Standard-Schlüssel
            if key in ["name", "description", "characters", "objects", "threats", "objectives", "suggested_actions", "completed"]:
                continue
            
            # Wenn es ein String ist, könnte es ein dynamisches Element wie eine Notiz oder ein Zustand sein
            if isinstance(value, str):
                self.ui.display_text(f"{key}: {value}")
        
        objectives = scene.get("objectives", [])
        if isinstance(objectives, list) and objectives:
            self.ui.display_subtitle("Ziele")
            for objective in objectives:
                if isinstance(objective, dict):
                    status = "[X]" if objective.get("completed", False) else "[ ]"
                    self.ui.display_text(f"{status} {objective.get('description', '')}")
                else:
                    self.ui.display_text(f"- {objective}")
        
        suggested_actions = scene.get("suggested_actions", [])
        if isinstance(suggested_actions, list) and suggested_actions:
            self.ui.display_subtitle("Mögliche Aktionen")
            for action in suggested_actions:
                self.ui.display_text(f"- {action}")
    
    def _display_current_quest(self) -> None:
        """Zeigt die aktuelle Quest an."""
        quest = self.current_game_state.quest_data
        
        self.ui.clear_screen()
        self.ui.display_title("Aktuelle Quest")
        
        if not quest:
            self.ui.display_text("Keine aktive Quest.")
            self.ui.display_text("\nDrücke Enter, um fortzufahren...")
            input()
            return
        
        self.ui.display_text(quest.get("name", "Unbenannte Quest"))
        self.ui.display_text("\n" + quest.get("description", ""))
        
        if "client" in quest:
            client = quest["client"]
            self.ui.display_subtitle("Auftraggeber")
            self.ui.display_text(f"{client.get('name', '')}: {client.get('description', '')}")
        
        if "objectives" in quest:
            self.ui.display_subtitle("Ziele")
            for objective in quest["objectives"]:
                status = "[X]" if objective.get("completed", False) else "[ ]"
                self.ui.display_text(f"{status} {objective.get('description', '')}")
        
        if "rewards" in quest:
            rewards = quest["rewards"]
            self.ui.display_subtitle("Belohnungen")
            
            if "credits" in rewards:
                self.ui.display_text(f"Credits: {rewards['credits']}")
            
            if "xp" in rewards:
                self.ui.display_text(f"Erfahrungspunkte: {rewards['xp']}")
            
            if "items" in rewards and rewards["items"]:
                self.ui.display_text("Items:")
                for item in rewards["items"]:
                    self.ui.display_text(f"- {item.get('name', '')}")
        
        if "locations" in quest and quest["locations"]:
            self.ui.display_subtitle("Orte")
            for location in quest["locations"]:
                visited = " (besucht)" if location.get("visited", False) else ""
                self.ui.display_text(f"{location.get('name', '')}{visited}: {location.get('description', '')}")
        
        if "npcs" in quest and quest["npcs"]:
            self.ui.display_subtitle("Personen")
            for npc in quest["npcs"]:
                self.ui.display_text(f"{npc.get('name', '')}: {npc.get('description', '')}")
        
        self.ui.display_text("\nDrücke Enter, um fortzufahren...")
        input()
    
    def _display_help(self) -> None:
        """Zeigt die Hilfe an."""
        self.ui.clear_screen()
        self.ui.display_title("HILFE")
        
        self.ui.display_text("Befehle:")
        self.ui.display_text("- charakter, character, stats, blatt: Zeigt das Charakterblatt an")
        self.ui.display_text("- quest, auftrag, mission: Zeigt die aktuelle Quest an")
        self.ui.display_text("- beenden, quit, exit: Beendet das Spiel")
        self.ui.display_text("- hilfe, help, ?: Zeigt diese Hilfe an")
        
        self.ui.display_text("\nSpieltipps:")
        self.ui.display_text("- Beschreibe deine Aktionen detailliert")
        self.ui.display_text("- Nutze deine Trademarks und Edges")
        self.ui.display_text("- Achte auf die Umgebung und nutze sie zu deinem Vorteil")
        self.ui.display_text("- Stunt Points können eingesetzt werden, um:")
        self.ui.display_text("  * Ein zweites Trademark zu nutzen")
        self.ui.display_text("  * Treffer abzuwehren")
        self.ui.display_text("  * Ein Würfelergebnis zu verbessern")
        self.ui.display_text("  * Ein nützliches Detail zur Szene hinzuzufügen")
        
        self.ui.display_text("\nDrücke Enter, um fortzufahren...")
        input()
    
    def _display_check_result(self, check_result: Dict[str, Any]) -> None:
        """
        Zeigt das Ergebnis eines Würfelwurfs an.
        
        Args:
            check_result: Das Ergebnis des Würfelwurfs
        """
        result = check_result["result"]
        pool_details = check_result["pool_details"]
        
        self.ui.display_subtitle("Würfelwurf")
        self.ui.display_text(self.check_manager.get_check_description(pool_details))
        
        # Würfelergebnis
        self.ui.display_text(f"Gewürfelt: {result.action_dice} vs. {result.danger_dice}")
        self.ui.display_text(f"Verbleibende Würfel: {result.remaining_dice}")
        
        # Erfolgsgrad
        success_levels = {
            "success": "Erfolg",
            "partial": "Teilerfolg",
            "failure": "Misserfolg",
            "botch": "Kritischer Misserfolg"
        }
        level = success_levels.get(result.success_level, result.success_level)
        self.ui.display_text(f"\nErgebnis: {level} (Wert: {result.value})")
        
        if result.boons > 0:
            self.ui.display_text(f"Boons: {result.boons}")
        
        if result.is_botch:
            self.ui.display_text("BOTCH! Ein kritischer Misserfolg!")
    
    def _display_consequences(self, consequences: Dict[str, Any]) -> None:
        """
        Zeigt die Konsequenzen eines Würfelwurfs an.
        
        Args:
            consequences: Die Konsequenzdaten
        """
        self.ui.display_subtitle("Konsequenzen")
        self.ui.display_text(consequences.get("description", ""))
    
    def _update_game_state(self, consequences: Dict[str, Any]) -> None:
        """
        Aktualisiert den Spielzustand basierend auf den Konsequenzen.
        
        Args:
            consequences: Die Konsequenzdaten
        """
        updates = consequences.get("game_state_updates", {})
        
        # Füge Ereignis zur Historie hinzu
        if "history_event" in updates:
            self.current_game_state.add_to_history(updates["history_event"])
        
        # Aktualisiere die aktuelle Szene
        if "scene_updates" in updates:
            for key, value in updates["scene_updates"].items():
                # Wenn der Schlüssel bereits ein Dictionary in der Szene ist, aktualisiere es
                if key in self.current_game_state.current_scene and isinstance(self.current_game_state.current_scene[key], dict):
                    self.current_game_state.current_scene[key].update(value if isinstance(value, dict) else {"status": value})
                else:
                    # Sonst füge den Wert direkt hinzu
                    self.current_game_state.current_scene[key] = value
        
        # Aktualisiere den Spielweltzustand
        if "world_state_updates" in updates:
            for key, value in updates["world_state_updates"].items():
                if key in self.current_game_state.world_state and isinstance(self.current_game_state.world_state[key], dict):
                    self.current_game_state.world_state[key].update(value if isinstance(value, dict) else {"status": value})
                else:
                    self.current_game_state.world_state[key] = value
        
        # Aktualisiere die Questdaten
        if "quest_updates" in updates:
            for key, value in updates["quest_updates"].items():
                if key in self.current_game_state.quest_data and isinstance(self.current_game_state.quest_data[key], dict):
                    self.current_game_state.quest_data[key].update(value if isinstance(value, dict) else {"status": value})
                else:
                    self.current_game_state.quest_data[key] = value
        
        # Aktualisiere die Beschreibung der Szene mit den Konsequenzen, wenn vorhanden
        if "description" in consequences:
            # Füge die neue Beschreibung als neue Information hinzu
            # und behalte die ursprüngliche Beschreibung
            original_description = self.current_game_state.current_scene.get("description", "")
            new_description = consequences["description"]
            
            # Wenn die Beschreibung unterschiedlich ist, aktualisiere sie
            if original_description != new_description and new_description.strip():
                # Füge die neue Beschreibung zur Szene als letztes_ereignis oder ähnlich hinzu
                self.current_game_state.current_scene["letztes_ereignis"] = new_description
        
        # Markiere die Szene als abgeschlossen, wenn angegeben
        if consequences.get("scene_completed", False):
            self.current_game_state.current_scene["completed"] = True
    
    def _update_character(self, consequences: Dict[str, Any]) -> None:
        """
        Aktualisiert die Charakterdaten basierend auf den Konsequenzen.
        
        Args:
            consequences: Die Konsequenzdaten
        """
        updates = consequences.get("character_updates", {})
        char_id = self.current_character_data["id"]
        
        # Charakter aus der Datenbank laden
        character = self.character_manager.characters.get(char_id)
        if not character:
            print(f"Fehler: Charakter {char_id} konnte nicht geladen werden.")
            return
        
        # Hits hinzufügen/entfernen
        if "add_hits" in updates and updates["add_hits"] is not None:
            for _ in range(updates["add_hits"]):
                character.take_hit()
        
        if "heal_hits" in updates and updates["heal_hits"] is not None:
            for _ in range(updates["heal_hits"]):
                character.heal_hit()
        
        # Trauma hinzufügen
        if "add_trauma" in updates:
            character.add_trauma(updates["add_trauma"])
        
        # Bedingungen hinzufügen/entfernen
        if "add_condition" in updates:
            character.add_condition(updates["add_condition"])
        
        if "remove_condition" in updates:
            character.remove_condition(updates["remove_condition"])
        
        # Stunt Points ausgeben/auffüllen
        if "spend_stunt_points" in updates:
            for _ in range(updates["spend_stunt_points"]):
                character.spend_stunt_point()
        
        if "refresh_stunt_points" in updates and updates["refresh_stunt_points"]:
            character.refresh_stunt_points()
        
        # XP hinzufügen
        if "add_xp" in updates:
            character.add_xp(updates["add_xp"])
        
        # Items hinzufügen/entfernen
        if "add_item" in updates and updates["add_item"] is not None:
            from cyberstory.mechanics.interfaces import Item
            
            item_data = updates["add_item"]
            item = Item(
                name=item_data.get("name", ""),
                tags=item_data.get("tags", []),
                description=item_data.get("description", ""),
                is_special=item_data.get("is_special", False)
            )
            character.add_item(item)
        
        if "remove_item" in updates and updates["remove_item"] is not None:
            item_name = updates["remove_item"]
            # Hier müsste die Logik zum Entfernen eines Items implementiert werden
            # Da die Character-Klasse keine remove_item-Methode hat, muss diese ergänzt werden
        
        # Drive aktualisieren
        if "tick_drive" in updates and character.drive:
            box_index = updates["tick_drive"]
            character.drive.tick(box_index)
        
        if "cross_out_drive" in updates and character.drive:
            box_index = updates["cross_out_drive"]
            character.drive.cross_out(box_index)
        
        # Charakter in der Datenbank aktualisieren
        self.character_manager.db.save(character.to_dict())
        
        # Aktualisierte Daten neu laden
        self.current_character_data = self.character_manager.get_character(char_id)
    
    def _update_direct(self, updates: Dict[str, Any]) -> None:
        """
        Aktualisiert Spiel- und Charakterzustand direkt (ohne Würfelwurf).
        
        Args:
            updates: Die Aktualisierungsdaten
        """
        if "game_state" in updates:
            game_updates = updates["game_state"]
            
            # Historie aktualisieren
            if "history_event" in game_updates:
                self.current_game_state.add_to_history(game_updates["history_event"])
            
            # Szene aktualisieren
            if "scene_updates" in game_updates:
                for key, value in game_updates["scene_updates"].items():
                    self.current_game_state.current_scene[key] = value
            
            # Spielweltzustand aktualisieren
            if "world_state_updates" in game_updates:
                for key, value in game_updates["world_state_updates"].items():
                    self.current_game_state.world_state[key] = value
            
            # Quest aktualisieren
            if "quest_updates" in game_updates:
                for key, value in game_updates["quest_updates"].items():
                    self.current_game_state.quest_data[key] = value
        
        if "character" in updates:
            # Hier könnten Charakteraktualisierungen verarbeitet werden
            # Ähnlich wie in _update_character, aber direkt aus den updates
            pass
    
    def _is_game_completed(self) -> bool:
        """
        Prüft, ob das Spiel abgeschlossen ist.
        
        Returns:
            bool: True, wenn das Spiel abgeschlossen ist, sonst False
        """
        return self.current_game_state.quest_data.get("completed", False)
    
    def _end_game(self) -> None:
        """Beendet das Spiel und zeigt eine Zusammenfassung an."""
        self.ui.clear_screen()
        self.ui.display_title("SPIEL ABGESCHLOSSEN")
        
        # Quest-Abschluss
        quest = self.current_game_state.quest_data
        self.ui.display_text(f"Quest: {quest.get('name', 'Unbenannte Quest')}")
        self.ui.display_text(f"Status: {'Abgeschlossen' if quest.get('completed', False) else 'Nicht abgeschlossen'}")
        
        # Belohnungen
        if "rewards" in quest:
            rewards = quest["rewards"]
            self.ui.display_subtitle("Belohnungen")
            
            if "credits" in rewards:
                self.ui.display_text(f"Credits: {rewards['credits']}")
            
            if "xp" in rewards:
                self.ui.display_text(f"Erfahrungspunkte: {rewards['xp']}")
                
                # XP zum Charakter hinzufügen
                char_id = self.current_character_data["id"]
                character = self.character_manager.characters.get(char_id)
                if character:
                    character.add_xp(rewards["xp"])
                    self.character_manager.db.save(character.to_dict())
            
            if "items" in rewards and rewards["items"]:
                self.ui.display_text("Items:")
                for item in rewards["items"]:
                    self.ui.display_text(f"- {item.get('name', '')}")
        
        # Verlauf
        self.ui.display_subtitle("Spielverlauf")
        history = self.current_game_state.history[-10:] if len(self.current_game_state.history) > 10 else self.current_game_state.history
        for event in history:
            self.ui.display_text(f"- {event}")
        
        self.ui.display_text("\nDrücke Enter, um fortzufahren...")
        input()
