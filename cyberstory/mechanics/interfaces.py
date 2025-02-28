# character/interfaces.py
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class Trademark:
    """Repräsentiert ein Trademark (Kernkompetenz) eines Charakters."""
    
    def __init__(self, name: str, triggers: List[str] = None, description: str = ""):
        """
        Initialisiert ein Trademark.
        
        Args:
            name: Name des Trademarks
            triggers: Liste potentieller Auslöser/Fähigkeiten
            description: Beschreibung des Trademarks
        """
        self.name = name
        self.triggers = triggers or []
        self.description = description
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert das Trademark in ein Dictionary."""
        return {
            "name": self.name,
            "triggers": self.triggers,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Trademark':
        """Erstellt ein Trademark aus einem Dictionary."""
        return cls(
            name=data.get("name", ""),
            triggers=data.get("triggers", []),
            description=data.get("description", "")
        )


class Edge:
    """Repräsentiert einen Edge (spezifischer Vorteil) eines Charakters."""
    
    def __init__(self, name: str, trademark: str, description: str = ""):
        """
        Initialisiert einen Edge.
        
        Args:
            name: Name des Edges
            trademark: Name des zugehörigen Trademarks
            description: Beschreibung des Edges
        """
        self.name = name
        self.trademark = trademark
        self.description = description
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert den Edge in ein Dictionary."""
        return {
            "name": self.name,
            "trademark": self.trademark,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Edge':
        """Erstellt einen Edge aus einem Dictionary."""
        return cls(
            name=data.get("name", ""),
            trademark=data.get("trademark", ""),
            description=data.get("description", "")
        )


class Flaw:
    """Repräsentiert einen Flaw (Nachteil) eines Charakters."""
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialisiert einen Flaw.
        
        Args:
            name: Name des Flaws
            description: Beschreibung des Flaws
        """
        self.name = name
        self.description = description
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert den Flaw in ein Dictionary."""
        return {
            "name": self.name,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Flaw':
        """Erstellt einen Flaw aus einem Dictionary."""
        return cls(
            name=data.get("name", ""),
            description=data.get("description", "")
        )


class Drive:
    """Repräsentiert einen Drive (Motivation) eines Charakters."""
    
    def __init__(self, description: str, track: List[bool] = None):
        """
        Initialisiert einen Drive.
        
        Args:
            description: Beschreibung des Drives
            track: Fortschrittsleiste (10 Boxen, True = markiert, False = leer)
        """
        self.description = description
        self.track = track or [False] * 10  # 10 leere Boxen als Standard
    
    def tick(self, index: int) -> bool:
        """
        Markiert eine Box in der Fortschrittsleiste.
        
        Args:
            index: Index der zu markierenden Box (0-9)
            
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if 0 <= index < len(self.track):
            self.track[index] = True
            return True
        return False
    
    def cross_out(self, index: int) -> bool:
        """
        Kreuzt eine Box in der Fortschrittsleiste aus (setzt sie zurück).
        
        Args:
            index: Index der auszukreuzenden Box (0-9)
            
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if 0 <= index < len(self.track):
            self.track[index] = False
            return True
        return False
    
    def progress(self) -> int:
        """Gibt die Anzahl der markierten Boxen zurück."""
        return sum(1 for box in self.track if box)
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert den Drive in ein Dictionary."""
        return {
            "description": self.description,
            "track": self.track
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Drive':
        """Erstellt einen Drive aus einem Dictionary."""
        return cls(
            description=data.get("description", ""),
            track=data.get("track", [False] * 10)
        )


class Item:
    """Repräsentiert ein Ausrüstungsstück."""
    
    def __init__(self, name: str, tags: List[str] = None, description: str = "", is_special: bool = False):
        """
        Initialisiert ein Item.
        
        Args:
            name: Name des Items
            tags: Liste von Tags, die das Item beschreiben
            description: Beschreibung des Items
            is_special: Ob es sich um ein spezielles Item handelt
        """
        self.name = name
        self.tags = tags or []
        self.description = description
        self.is_special = is_special
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert das Item in ein Dictionary."""
        return {
            "name": self.name,
            "tags": self.tags,
            "description": self.description,
            "is_special": self.is_special
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Item':
        """Erstellt ein Item aus einem Dictionary."""
        return cls(
            name=data.get("name", ""),
            tags=data.get("tags", []),
            description=data.get("description", ""),
            is_special=data.get("is_special", False)
        )


class CharacterInterface(ABC):
    """Interface für die Charakterverwaltung."""
    
    @abstractmethod
    def create_character(self, name: str, faction: str = None) -> Dict[str, Any]:
        """Erstellt einen neuen Charakter."""
        pass
    
    @abstractmethod
    def add_trademark(self, character_id: str, trademark: Trademark) -> bool:
        """Fügt ein Trademark hinzu."""
        pass
    
    @abstractmethod
    def add_edge(self, character_id: str, edge: Edge) -> bool:
        """Fügt einen Edge hinzu."""
        pass
    
    @abstractmethod
    def add_flaw(self, character_id: str, flaw: Flaw) -> bool:
        """Fügt einen Flaw hinzu."""
        pass
    
    @abstractmethod
    def set_drive(self, character_id: str, drive: Drive) -> bool:
        """Setzt den Drive."""
        pass
    
    @abstractmethod
    def add_item(self, character_id: str, item: Item) -> bool:
        """Fügt ein Item zum Inventar hinzu."""
        pass
    
    @abstractmethod
    def get_character(self, character_id: str) -> Optional[Dict[str, Any]]:
        """Gibt die Charakterdaten zurück."""
        pass
    
    @abstractmethod
    def update_character(self, character_id: str, updates: Dict[str, Any]) -> bool:
        """Aktualisiert die Charakterdaten."""
        pass

# mechanics/interfaces.py
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple

class DiceResult:
    """Repräsentiert das Ergebnis eines Würfelwurfs."""
    
    def __init__(self, 
                 success_level: str,
                 value: int, 
                 action_dice: List[int], 
                 danger_dice: List[int],
                 remaining_dice: List[int],
                 boons: int = 0,
                 is_botch: bool = False):
        """
        Initialisiert ein Würfelergebnis.
        
        Args:
            success_level: "success", "partial", "failure", "botch"
            value: Der höchste verbleibende Würfelwert
            action_dice: Alle geworfenen Action Dice
            danger_dice: Alle geworfenen Danger Dice
            remaining_dice: Verbleibende Action Dice nach Neutralisierung
            boons: Anzahl der zusätzlichen Erfolge (6er)
            is_botch: Ob ein kritischer Misserfolg vorliegt
        """
        self.success_level = success_level
        self.value = value
        self.action_dice = action_dice
        self.danger_dice = danger_dice
        self.remaining_dice = remaining_dice
        self.boons = boons
        self.is_botch = is_botch
    
    def __str__(self) -> str:
        """String-Repräsentation des Ergebnisses."""
        if self.is_botch:
            return f"Botch! Kritischer Misserfolg."
        
        result = f"{self.success_level.capitalize()} (Wert: {self.value})"
        if self.boons > 0:
            result += f" mit {self.boons} Boon{'s' if self.boons > 1 else ''}"
        
        result += f"\nAction Dice: {self.action_dice}"
        result += f"\nDanger Dice: {self.danger_dice}"
        result += f"\nVerbleibende Würfel: {self.remaining_dice}"
        
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """Gibt eine Dictionary-Repräsentation zurück."""
        return {
            "success_level": self.success_level,
            "value": self.value,
            "action_dice": self.action_dice,
            "danger_dice": self.danger_dice,
            "remaining_dice": self.remaining_dice,
            "boons": self.boons,
            "is_botch": self.is_botch
        }


class DiceSystemInterface(ABC):
    """Interface für Würfelsysteme."""
    
    @abstractmethod
    def perform_check(self, 
                      action_dice: int = 1, 
                      danger_dice: int = 0) -> DiceResult:
        """
        Führt einen Würfelwurf durch.
        
        Args:
            action_dice: Anzahl der Action Dice
            danger_dice: Anzahl der Danger Dice
            
        Returns:
            DiceResult: Das Ergebnis des Würfelwurfs
        """
        pass
    
    @abstractmethod
    def calculate_dice_pool(self, 
                           character_data: Dict[str, Any], 
                           check_context: Dict[str, Any]) -> Tuple[int, int]:
        """
        Berechnet den Würfelpool basierend auf Charakterdaten und Kontext.
        
        Args:
            character_data: Daten des Charakters
            check_context: Kontext des Checks (Aktion, Umgebung, etc.)
            
        Returns:
            Tuple[int, int]: (action_dice, danger_dice)
        """
        pass