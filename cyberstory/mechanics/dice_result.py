# mechanics/dice_result.py
from typing import List, Dict, Any

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
        """
        Gibt eine Dictionary-Repräsentation zurück.
        
        Returns:
            Dictionary mit den Würfelergebnisdaten
        """
        return {
            "success_level": self.success_level,
            "value": self.value,
            "action_dice": self.action_dice,
            "danger_dice": self.danger_dice,
            "remaining_dice": self.remaining_dice,
            "boons": self.boons,
            "is_botch": self.is_botch
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DiceResult':
        """
        Erstellt ein DiceResult aus einem Dictionary.
        
        Args:
            data: Dictionary mit den Würfelergebnisdaten
            
        Returns:
            DiceResult-Objekt
        """
        return cls(
            success_level=data.get("success_level", "failure"),
            value=data.get("value", 0),
            action_dice=data.get("action_dice", []),
            danger_dice=data.get("danger_dice", []),
            remaining_dice=data.get("remaining_dice", []),
            boons=data.get("boons", 0),
            is_botch=data.get("is_botch", False)
        )