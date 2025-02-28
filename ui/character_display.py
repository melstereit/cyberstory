# ui/character_display.py
from ui.terminal import TerminalUI
from typing import Dict, List, Any, Optional

class CharacterDisplay:
    """Zeigt Charakterinformationen im Terminal an."""
    
    def __init__(self, terminal_ui: TerminalUI):
        """
        Initialisiert das CharacterDisplay.
        
        Args:
            terminal_ui: Instanz der Terminal-UI
        """
        self.ui = terminal_ui
    
    def display_character_sheet(self, character_data: Dict[str, Any]) -> None:
        """
        Zeigt ein vollständiges Charakterblatt an.
        
        Args:
            character_data: Die Charakterdaten
        """
        self.ui.clear_screen()
        self.ui.display_title(f"CHARAKTERBLATT: {character_data.get('name')}")
        
        # Grundlegende Informationen
        self.ui.display_text(f"Name: {character_data.get('name')}")
        self.ui.display_text(f"Fraktion: {character_data.get('faction')}")
        self.ui.display_text(f"XP: {character_data.get('xp', 0)}")
        
        # Status
        self.ui.display_subtitle("STATUS")
        
        # Hit Track
        hit_track = character_data.get("hit_track", [])
        hit_display = "Hits: " + "".join(["[X]" if hit else "[ ]" for hit in hit_track])
        self.ui.display_text(hit_display)
        
        # Stunt Points
        sp = character_data.get("stunt_points", 0)
        max_sp = character_data.get("max_stunt_points", 3)
        sp_display = "Stunt Points: " + "".join(["[X]" if i < sp else "[ ]" for i in range(max_sp)])
        self.ui.display_text(sp_display)
        
        # Traumas
        traumas = character_data.get("traumas", [])
        if traumas:
            self.ui.display_text("Traumas:")
            for trauma in traumas:
                self.ui.display_text(f"  - {trauma}")
        
        # Conditions
        conditions = character_data.get("conditions", [])
        if conditions:
            self.ui.display_text("Conditions:")
            for condition in conditions:
                self.ui.display_text(f"  - {condition}")
        
        # Trademarks und Edges
        self.ui.display_subtitle("TRADEMARKS & EDGES")
        
        trademarks = character_data.get("trademarks", {})
        edges = character_data.get("edges", [])
        
        # Gruppiere Edges nach Trademark
        edge_by_trademark = {}
        for edge in edges:
            tm_name = edge.get("trademark", "")
            if tm_name not in edge_by_trademark:
                edge_by_trademark[tm_name] = []
            edge_by_trademark[tm_name].append(edge.get("name", ""))
        
        # Zeige Trademarks mit ihren Edges
        for name, tm in trademarks.items():
            tm_edges = edge_by_trademark.get(name, [])
            self.ui.display_text(f"{name}: {', '.join(tm.get('triggers', []))}")
            if tm_edges:
                self.ui.display_text(f"  Edges: {', '.join(tm_edges)}")
        
        # Flaws
        self.ui.display_subtitle("FLAWS")
        
        flaws = character_data.get("flaws", [])
        for flaw in flaws:
            self.ui.display_text(f"{flaw.get('name')}: {flaw.get('description')}")
        
        # Drive
        self.ui.display_subtitle("DRIVE")
        
        drive = character_data.get("drive", {})
        if drive:
            self.ui.display_text(drive.get("description", ""))
            
            # Drive Track
            track = drive.get("track", [])
            track_display = "Drive Track: " + "".join(["[X]" if box else "[ ]" for box in track])
            self.ui.display_text(track_display)
        
        # Inventar
        self.ui.display_subtitle("INVENTAR")
        
        inventory = character_data.get("inventory", [])
        special_items = [item for item in inventory if item.get("is_special")]
        basic_items = [item for item in inventory if not item.get("is_special")]
        
        if special_items:
            self.ui.display_text("Spezielle Ausrüstung:")
            for item in special_items:
                self.ui.display_text(f"  {item.get('name')}: {', '.join(item.get('tags', []))}")
        
        if basic_items:
            self.ui.display_text("Grundausrüstung:")
            for item in basic_items:
                self.ui.display_text(f"  {item.get('name')}")
        
        self.ui.display_text("\nDrücke Enter, um fortzufahren...")
        input()
    
    def display_character_summary(self, character_data: Dict[str, Any]) -> None:
        """
        Zeigt eine Kurzübersicht des Charakters an.
        
        Args:
            character_data: Die Charakterdaten
        """
        name = character_data.get("name", "")
        faction = character_data.get("faction", "")
        
        # Hit Track
        hit_track = character_data.get("hit_track", [])
        hits = sum(1 for hit in hit_track if hit)
        max_hits = len(hit_track)
        
        # Stunt Points
        sp = character_data.get("stunt_points", 0)
        max_sp = character_data.get("max_stunt_points", 3)
        
        # Trademarks
        trademarks = list(character_data.get("trademarks", {}).keys())
        
        # Zusammenfassung
        self.ui.display_text(f"{name} ({faction}) - Hits: {hits}/{max_hits}, SP: {sp}/{max_sp}")
        self.ui.display_text(f"Trademarks: {', '.join(trademarks)}")
        
        # Aktuelle Conditions
        conditions = character_data.get("conditions", [])
        if conditions:
            self.ui.display_text(f"Conditions: {', '.join(conditions)}")
        
        # Traumas
        traumas = character_data.get("traumas", [])
        if traumas:
            self.ui.display_text(f"Traumas: {', '.join(traumas)}")
    
    def display_character_list(self, characters: List[Dict[str, Any]]) -> Optional[str]:
        """
        Zeigt eine Liste von Charakteren an und lässt den Benutzer einen auswählen.
        
        Args:
            characters: Liste von Charakterdaten
        
        Returns:
            Die ID des ausgewählten Charakters oder None bei Abbruch
        """
        self.ui.clear_screen()
        self.ui.display_title("CHARAKTERE")
        
        if not characters:
            self.ui.display_text("Keine Charaktere vorhanden.")
            self.ui.display_text("\nDrücke Enter, um fortzufahren...")
            input()
            return None
        
        options = []
        for char in characters:
            name = char.get("name", "")
            faction = char.get("faction", "")
            
            # Kurzzusammenfassung
            trademarks = list(char.get("trademarks", {}).keys())
            trademark_text = ", ".join(trademarks) if trademarks else "Keine Trademarks"
            
            options.append(f"{name} ({faction}) - {trademark_text}")
        
        choice = self.ui.get_choice("Wähle einen Charakter:", options)
        
        if choice < len(characters):
            return characters[choice].get("id")
        
        return None