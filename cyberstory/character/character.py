# character/character.py
import uuid
from typing import Dict, Any

from cyberstory.mechanics.interfaces import Trademark, Edge, Flaw, Drive, Item


class Character:
    """Repräsentiert einen Spielercharakter."""
    
    def __init__(self, name: str, character_id: str = None, faction: str = None):
        """
        Initialisiert einen Charakter.
        
        Args:
            name: Name des Charakters
            character_id: Eindeutige ID des Charakters (generiert, wenn nicht angegeben)
            faction: Fraktion des Charakters
        """
        self.id = character_id or str(uuid.uuid4())
        self.name = name
        self.faction = faction
        self.trademarks = {}  # name -> Trademark
        self.edges = []  # Liste von Edge-Objekten
        self.flaws = []  # Liste von Flaw-Objekten
        self.drive = None  # Drive-Objekt
        self.stunt_points = 3  # Standardwert
        self.max_stunt_points = 3  # Maximaler Wert
        self.inventory = []  # Liste von Item-Objekten
        self.xp = 0
        self.hit_track = [False, False, False]  # 3 Boxen, False = nicht markiert
        self.traumas = []  # Liste von Trauma-Strings
        self.conditions = []  # Liste von Condition-Strings
    
    def add_trademark(self, trademark: Trademark) -> bool:
        """
        Fügt ein Trademark hinzu.
        
        Args:
            trademark: Das hinzuzufügende Trademark
            
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if len(self.trademarks) >= 5:  # Maximale Anzahl von Trademarks
            return False
        
        self.trademarks[trademark.name] = trademark
        return True
    
    def add_edge(self, edge: Edge) -> bool:
        """
        Fügt einen Edge hinzu.
        
        Args:
            edge: Der hinzuzufügende Edge
            
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        # Prüfen, ob das zugehörige Trademark existiert
        if edge.trademark not in self.trademarks:
            return False
        
        self.edges.append(edge)
        return True
    
    def add_flaw(self, flaw: Flaw) -> bool:
        """
        Fügt einen Flaw hinzu.
        
        Args:
            flaw: Der hinzuzufügende Flaw
            
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        self.flaws.append(flaw)
        return True
    
    def set_drive(self, drive: Drive) -> bool:
        """
        Setzt den Drive des Charakters.
        
        Args:
            drive: Der Drive des Charakters
            
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        self.drive = drive
        return True
    
    def add_item(self, item: Item) -> bool:
        """
        Fügt ein Item zum Inventar hinzu.
        
        Args:
            item: Das hinzuzufügende Item
            
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        # Für spezielle Items: Prüfen, ob die maximale Anzahl erreicht ist
        if item.is_special:
            special_count = sum(1 for i in self.inventory if i.is_special)
            if special_count >= 4:  # Maximale Anzahl spezieller Items
                return False
        
        self.inventory.append(item)
        return True
    
    def remove_item(self, item_name: str) -> bool:
        """
        Entfernt ein Item aus dem Inventar.
        
        Args:
            item_name: Name des zu entfernenden Items
            
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        # Suche das Item im Inventar
        for i, item in enumerate(self.inventory):
            if item.name == item_name:
                # Entferne das Item
                self.inventory.pop(i)
                return True
        
        # Item nicht gefunden
        return False

    def take_hit(self) -> bool:
        """
        Markiert eine Hit-Box.
        
        Returns:
            bool: True, wenn eine Box markiert wurde, False wenn alle voll sind
        """
        for i, hit in enumerate(self.hit_track):
            if not hit:  # Leere Box gefunden
                self.hit_track[i] = True
                return True
        return False  # Alle Boxen sind bereits markiert
    
    def heal_hit(self) -> bool:
        """
        Heilt einen Hit.
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        for i in range(len(self.hit_track) - 1, -1, -1):
            if self.hit_track[i]:  # Markierte Box gefunden
                self.hit_track[i] = False
                return True
        return False  # Keine markierten Boxen gefunden
    
    def add_trauma(self, trauma: str) -> None:
        """Fügt ein Trauma hinzu."""
        self.traumas.append(trauma)
    
    def remove_trauma(self, trauma: str) -> bool:
        """
        Entfernt ein Trauma.
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if trauma in self.traumas:
            self.traumas.remove(trauma)
            return True
        return False
    
    def add_condition(self, condition: str) -> None:
        """Fügt eine Bedingung hinzu."""
        self.conditions.append(condition)
    
    def remove_condition(self, condition: str) -> bool:
        """
        Entfernt eine Bedingung.
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if condition in self.conditions:
            self.conditions.remove(condition)
            return True
        return False
    
    def spend_stunt_point(self) -> bool:
        """
        Gibt einen Stunt Point aus.
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if self.stunt_points > 0:
            self.stunt_points -= 1
            return True
        return False
    
    def refresh_stunt_points(self) -> None:
        """Füllt die Stunt Points auf das Maximum auf."""
        self.stunt_points = self.max_stunt_points
    
    def add_xp(self, amount: int) -> None:
        """Fügt Erfahrungspunkte hinzu."""
        self.xp += amount
    
    def spend_xp(self, amount: int) -> bool:
        """
        Gibt Erfahrungspunkte aus.
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if self.xp >= amount:
            self.xp -= amount
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert den Charakter in ein Dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "faction": self.faction,
            "trademarks": {name: tm.to_dict() for name, tm in self.trademarks.items()},
            "edges": [edge.to_dict() for edge in self.edges],
            "flaws": [flaw.to_dict() for flaw in self.flaws],
            "drive": self.drive.to_dict() if self.drive else None,
            "stunt_points": self.stunt_points,
            "max_stunt_points": self.max_stunt_points,
            "inventory": [item.to_dict() for item in self.inventory],
            "xp": self.xp,
            "hit_track": self.hit_track,
            "traumas": self.traumas,
            "conditions": self.conditions
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Character':
        """Erstellt einen Charakter aus einem Dictionary."""
        character = cls(
            name=data.get("name", ""),
            character_id=data.get("id"),
            faction=data.get("faction")
        )
        
        # Trademarks
        for tm_data in data.get("trademarks", {}).values():
            character.add_trademark(Trademark.from_dict(tm_data))
        
        # Edges
        for edge_data in data.get("edges", []):
            character.add_edge(Edge.from_dict(edge_data))
        
        # Flaws
        for flaw_data in data.get("flaws", []):
            character.add_flaw(Flaw.from_dict(flaw_data))
        
        # Drive
        if data.get("drive"):
            character.set_drive(Drive.from_dict(data["drive"]))
        
        # Stunt Points
        character.stunt_points = data.get("stunt_points", 3)
        character.max_stunt_points = data.get("max_stunt_points", 3)
        
        # Inventory
        for item_data in data.get("inventory", []):
            character.add_item(Item.from_dict(item_data))
        
        # XP
        character.xp = data.get("xp", 0)
        
        # Hit Track
        character.hit_track = data.get("hit_track", [False, False, False])
        
        # Traumas und Conditions
        character.traumas = data.get("traumas", [])
        character.conditions = data.get("conditions", [])
        
        return character