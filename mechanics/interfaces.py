# mechanics/interfaces.py
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple

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