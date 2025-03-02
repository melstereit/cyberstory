class GameplayUI:
    """UI-Komponenten für das Gameplay."""
    
    def __init__(self, terminal_ui, character_display):
        """
        Initialisiert die Gameplay-UI.
        
        Args:
            terminal_ui: Instanz der Terminal-UI
            character_display: Instanz des CharacterDisplay
        """
        self.ui = terminal_ui
        self.character_display = character_display
    
    def display_scene(self, scene_data):
        """
        Zeigt eine Szene an.
        
        Args:
            scene_data: Die Daten der Szene
        """
        self.ui.clear_screen()
        self.ui.display_title(scene_data.get("name", "Aktuelle Szene"))
        
        # Beschreibung
        self.ui.display_text(scene_data.get("description", ""))
        
        # NPCs
        if "characters" in scene_data and scene_data["characters"]:
            self.ui.display_subtitle("Personen")
            for char in scene_data["characters"]:
                self.ui.display_text(f"{char['name']}: {char['description']}")
        
        # Objekte
        if "objects" in scene_data and scene_data["objects"]:
            self.ui.display_subtitle("Objekte")
            for obj in scene_data["objects"]:
                self.ui.display_text(f"{obj['name']}: {obj['description']}")
        
        # Ziele
        if "objectives" in scene_data and scene_data["objectives"]:
            self.ui.display_subtitle("Ziele")
            for objective in scene_data["objectives"]:
                self.ui.display_text(f"- {objective}")
        
        # Vorgeschlagene Aktionen
        if "suggested_actions" in scene_data and scene_data["suggested_actions"]:
            self.ui.display_subtitle("Mögliche Aktionen")
            for action in scene_data["suggested_actions"]:
                self.ui.display_text(f"- {action}")
    
    def display_character_status(self, character_data):
        """
        Zeigt den Status des Charakters an.
        
        Args:
            character_data: Die Charakterdaten
        """
        self.ui.display_subtitle("Charakterstatus")
        
        # Name und Fraktion
        name = character_data.get("name", "")
        faction = character_data.get("faction", "")
        self.ui.display_text(f"{name} ({faction})")
        
        # Hit Track
        hit_track = character_data.get("hit_track", [])
        hits = sum(1 for hit in hit_track if hit)
        max_hits = len(hit_track)
        self.ui.display_text(f"Hits: {hits}/{max_hits}")
        
        # Stunt Points
        sp = character_data.get("stunt_points", 0)
        max_sp = character_data.get("max_stunt_points", 3)
        self.ui.display_text(f"Stunt Points: {sp}/{max_sp}")
        
        # Traumas und Bedingungen
        traumas = character_data.get("traumas", [])
        if traumas:
            self.ui.display_text(f"Traumas: {', '.join(traumas)}")
        
        conditions = character_data.get("conditions", [])
        if conditions:
            self.ui.display_text(f"Conditions: {', '.join(conditions)}")
    
    def get_player_action(self):
        """
        Fordert eine Aktion vom Spieler an.
        
        Returns:
            str: Die eingegebene Aktion
        """
        return self.ui.get_input("\nWas möchtest du tun?")
    
    def display_check_result(self, check_result):
        """
        Zeigt das Ergebnis eines Würfelwurfs an.
        
        Args:
            check_result: Das Ergebnis des Würfelwurfs
        """
        self.ui.display_subtitle("Würfelwurf")
        
        result = check_result["result"]
        pool_details = check_result["pool_details"]
        
        # Würfelpool
        action_dice = pool_details["action_dice"]
        danger_dice = pool_details["danger_dice"]
        self.ui.display_text(f"Würfelpool: {action_dice} Action Dice vs. {danger_dice} Danger Dice")
        
        # Modifikatoren
        if "applied_modifiers" in pool_details and pool_details["applied_modifiers"]:
            self.ui.display_text("Angewendete Modifikatoren:")
            for mod in pool_details["applied_modifiers"]:
                self.ui.display_text(f"- {mod}")
        
        # Würfelergebnis
        self.ui.display_text(f"\nGewürfelt: {result.action_dice} vs. {result.danger_dice}")
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
    
    def display_consequences(self, consequences_data):
        """
        Zeigt die Konsequenzen eines Würfelwurfs an.
        
        Args:
            consequences_data: Die Konsequenzdaten
        """
        self.ui.display_subtitle("Konsequenzen")
        self.ui.display_text(consequences_data.get("description", ""))
    
    def display_quest_update(self, quest_data):
        """
        Zeigt ein Quest-Update an.
        
        Args:
            quest_data: Die Quest-Daten
        """
        self.ui.display_subtitle("Quest Update")
        self.ui.display_text(f"Quest: {quest_data.get('name', '')}")
        
        objectives = quest_data.get("objectives", [])
        self.ui.display_text("\nZiele:")
        for obj in objectives:
            status = "[X]" if obj.get("completed", False) else "[ ]"
            self.ui.display_text(f"{status} {obj.get('description', '')}")
        
        if quest_data.get("completed", False):
            self.ui.display_text("\nDie Quest wurde abgeschlossen!")
            
            rewards = quest_data.get("rewards", {})
            if rewards:
                self.ui.display_text("\nBelohnungen:")
                if "credits" in rewards:
                    self.ui.display_text(f"- Credits: {rewards['credits']}")
                if "xp" in rewards:
                    self.ui.display_text(f"- Erfahrungspunkte: {rewards['xp']}")
                if "items" in rewards and rewards["items"]:
                    self.ui.display_text("- Items:")
                    for item in rewards["items"]:
                        self.ui.display_text(f"  * {item['name']}")