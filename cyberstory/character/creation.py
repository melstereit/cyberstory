# character/creation.py
import random
from typing import Dict, List, Any

from cyberstory import CharacterManager
from cyberstory import GearManager
from cyberstory import TemplateManager
from cyberstory import Trademark, Edge, Flaw, Drive, Item


class CharacterCreation:
    """Verwaltet den Charaktererstellungsprozess."""
    
    def __init__(self, character_manager: CharacterManager, template_manager: TemplateManager, gear_manager: GearManager):
        """
        Initialisiert den CharacterCreation-Manager.
        
        Args:
            character_manager: Instanz des CharacterManagers
            template_manager: Instanz des TemplateManagers
            gear_manager: Instanz des GearManagers
        """
        self.character_manager = character_manager
        self.template_manager = template_manager
        self.gear_manager = gear_manager
        
        # Aktueller Charakter in Erstellung
        self.current_character_id = None
    
    def start_creation(self, name: str, faction: str = None) -> Dict[str, Any]:
        """
        Startet den Charaktererstellungsprozess.
        
        Args:
            name: Name des Charakters
            faction: Fraktion des Charakters
        
        Returns:
            Dict mit den Charakterdaten
        """
        character_data = self.character_manager.create_character(name, faction)
        self.current_character_id = character_data.get("id")
        return character_data
    
    def suggest_trademarks(self, background_story: str = None, count: int = 5) -> List[Dict[str, Any]]:
        """
        Schlägt Trademarks basierend auf der Hintergrundgeschichte vor.
        
        Args:
            background_story: Hintergrundgeschichte des Charakters
            count: Anzahl der Vorschläge
        
        Returns:
            Liste von Trademark-Dictionaries
        """
        suggestions = []
        
        # Hier könnte die Integration mit dem LLM erfolgen
        # Für jetzt einfach zufällige Vorschläge aus den Templates
        
        categories = list(self.template_manager.trademarks.keys())
        for _ in range(count):
            category = random.choice(categories)
            tm = self.template_manager.get_random_trademark(category)
            if tm and tm not in suggestions:
                suggestions.append(tm)
        
        return suggestions
    
    def add_trademark_to_character(self, trademark_name: str, triggers: List[str]) -> bool:
        """
        Fügt ein Trademark zum aktuellen Charakter hinzu.
        
        Args:
            trademark_name: Name des Trademarks
            triggers: Liste der Trigger für das Trademark
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if not self.current_character_id:
            return False
        
        trademark = Trademark(name=trademark_name, triggers=triggers)
        return self.character_manager.add_trademark(self.current_character_id, trademark)
    
    def suggest_edges(self, trademark_name: str, count: int = 3) -> List[str]:
        """
        Schlägt Edges für ein Trademark vor.
        
        Args:
            trademark_name: Name des Trademarks
            count: Anzahl der Vorschläge
        
        Returns:
            Liste von Edge-Namen
        """
        all_edges = self.template_manager.get_trademark_edges(trademark_name)
        
        if len(all_edges) <= count:
            return all_edges
        
        # Zufällige Auswahl, wenn es mehr als count Edges gibt
        return random.sample(all_edges, count)
    
    def add_edge_to_character(self, edge_name: str, trademark_name: str) -> bool:
        """
        Fügt einen Edge zum aktuellen Charakter hinzu.
        
        Args:
            edge_name: Name des Edges
            trademark_name: Name des zugehörigen Trademarks
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if not self.current_character_id:
            return False
        
        edge = Edge(name=edge_name, trademark=trademark_name)
        return self.character_manager.add_edge(self.current_character_id, edge)
    
    def suggest_flaws(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        Schlägt Flaws vor.
        
        Args:
            count: Anzahl der Vorschläge
        
        Returns:
            Liste von Flaw-Dictionaries
        """
        suggestions = []
        
        # Hier könnte die Integration mit dem LLM erfolgen
        # Für jetzt einfach zufällige Vorschläge aus den Templates
        
        for _ in range(count):
            flaw = self.template_manager.get_random_flaw()
            if flaw and flaw not in suggestions:
                suggestions.append(flaw)
        
        return suggestions
    
    def add_flaw_to_character(self, flaw_name: str, description: str = "") -> bool:
        """
        Fügt einen Flaw zum aktuellen Charakter hinzu.
        
        Args:
            flaw_name: Name des Flaws
            description: Beschreibung des Flaws
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if not self.current_character_id:
            return False
        
        flaw = Flaw(name=flaw_name, description=description)
        return self.character_manager.add_flaw(self.current_character_id, flaw)
    
    def suggest_drives(self, count: int = 3) -> List[str]:
        """
        Schlägt Drives vor.
        
        Args:
            count: Anzahl der Vorschläge
        
        Returns:
            Liste von Drive-Beschreibungen
        """
        suggestions = []
        
        # Hier könnte die Integration mit dem LLM erfolgen
        # Für jetzt einfach zufällige Vorschläge aus den Templates
        
        categories = set(drive_cat.get("category") for drive_cat in self.template_manager.drives)
        for category in categories:
            if len(suggestions) < count:
                drive = self.template_manager.get_random_drive(category)
                if drive:
                    suggestions.append(drive)
        
        # Füllen mit weiteren zufälligen Drives, falls nicht genug
        while len(suggestions) < count:
            drive = self.template_manager.get_random_drive()
            if drive and drive not in suggestions:
                suggestions.append(drive)
        
        return suggestions
    
    def set_drive_for_character(self, drive_description: str) -> bool:
        """
        Setzt den Drive für den aktuellen Charakter.
        
        Args:
            drive_description: Beschreibung des Drives
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if not self.current_character_id:
            return False
        
        drive = Drive(description=drive_description)
        return self.character_manager.set_drive(self.current_character_id, drive)
    
    def roll_for_gear(self, item_name: str, category: str, tags: List[str]) -> bool:
        """
        Führt einen Würfelwurf für ein spezifisches Ausrüstungsstück durch.
        
        Args:
            item_name: Name des Items
            category: Kategorie des Items
            tags: Liste der Tags für das Item
        
        Returns:
            bool: True, wenn der Wurf erfolgreich war, sonst False
        """
        if not self.current_character_id:
            return False
        
        # Würfeln für das Gear
        success = self.gear_manager.roll_for_gear(len(tags))
        
        if success:
            # Erstelle das Item und füge es hinzu
            item = Item(name=item_name, tags=tags, is_special=True)
            return self.character_manager.add_item(self.current_character_id, item)
        
        return False
    
    def add_basic_gear(self, item_name: str, description: str = "") -> bool:
        """
        Fügt ein Basis-Ausrüstungsstück zum aktuellen Charakter hinzu.
        
        Args:
            item_name: Name des Items
            description: Beschreibung des Items
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if not self.current_character_id:
            return False
        
        item = Item(name=item_name, description=description, is_special=False)
        return self.character_manager.add_item(self.current_character_id, item)
    
    def suggest_gear(self, trademark_name: str, count: int = 3) -> List[Dict[str, Any]]:
        """
        Schlägt Ausrüstung basierend auf einem Trademark vor.
        
        Args:
            trademark_name: Name des Trademarks
            count: Anzahl der Vorschläge
        
        Returns:
            Liste von Gear-Dictionaries
        """
        suggestions = []
        
        # Hier könnte die Integration mit dem LLM erfolgen
        # Für jetzt einfach zufällige Vorschläge aus den Templates
        
        # Ordne Trademarks grob Kategorien zu
        category_map = {
            "Codeslinger": ["tools", "cyberware"],
            "Infiltrator": ["tools", "melee_weapons"],
            "Gunfighter": ["ranged_weapons"],
            "Bounty Hunter": ["ranged_weapons", "armor"],
            # Weitere Zuordnungen...
        }
        
        categories = category_map.get(trademark_name, list(self.gear_manager.gear_categories.keys()))
        
        for _ in range(count):
            category = random.choice(categories)
            if category in self.gear_manager.gear_categories:
                item_data = random.choice(self.gear_manager.gear_categories[category])
                if item_data not in suggestions:
                    suggestions.append(item_data)
        
        return suggestions
    
    def complete_creation(self) -> Dict[str, Any]:
        """
        Schließt den Charaktererstellungsprozess ab.
        
        Returns:
            Dict mit den vollständigen Charakterdaten
        """
        if not self.current_character_id:
            return {}
        
        character_data = self.character_manager.get_character(self.current_character_id)
        self.current_character_id = None  # Zurücksetzen für die nächste Erstellung
        
        return character_data