# mechanics/modifiers.py
from typing import Dict, List, Any, Callable

class DicePoolModifier:
    """Repräsentiert einen Modifikator für den Würfelpool."""
    
    def __init__(self, 
                 name: str, 
                 action_dice: int = 0, 
                 danger_dice: int = 0,
                 condition: Callable[[Dict[str, Any], Dict[str, Any]], bool] = None):
        """
        Initialisiert einen Würfelpool-Modifikator.
        
        Args:
            name: Name des Modifikators
            action_dice: Anzahl der hinzuzufügenden Action Dice (kann negativ sein)
            danger_dice: Anzahl der hinzuzufügenden Danger Dice (kann negativ sein)
            condition: Optionale Funktion, die prüft, ob der Modifikator angewendet werden soll
        """
        self.name = name
        self.action_dice = action_dice
        self.danger_dice = danger_dice
        self.condition = condition or (lambda char, ctx: True)
    
    def applies(self, character_data: Dict[str, Any], check_context: Dict[str, Any]) -> bool:
        """Prüft, ob der Modifikator angewendet werden soll."""
        return self.condition(character_data, check_context)
    
    def __str__(self) -> str:
        """String-Repräsentation des Modifikators."""
        result = f"{self.name}: "
        if self.action_dice != 0:
            result += f"{'+' if self.action_dice > 0 else ''}{self.action_dice} Action Dice"
        if self.danger_dice != 0:
            if self.action_dice != 0:
                result += ", "
            result += f"{'+' if self.danger_dice > 0 else ''}{self.danger_dice} Danger Dice"
        return result


class ModifierManager:
    """Verwaltet Würfelpool-Modifikatoren."""
    
    def __init__(self):
        """Initialisiert den Modifier-Manager."""
        self.modifiers = []
        self._initialize_standard_modifiers()
    
    def _initialize_standard_modifiers(self):
        """Initialisiert Standardmodifikatoren."""
        # Trademark
        self.add_modifier(DicePoolModifier(
            name="Trademark",
            action_dice=1,
            condition=lambda char, ctx: ctx.get("relevant_trademark", False)
        ))
        
        # Edges
        self.add_modifier(DicePoolModifier(
            name="Edge",
            action_dice=1,
            condition=lambda char, ctx: len(ctx.get("relevant_edges", [])) > 0
        ))
        
        # Traumas
        self.add_modifier(DicePoolModifier(
            name="Trauma",
            danger_dice=1,
            condition=lambda char, ctx: len(char.get("traumas", [])) > 0
        ))
        
        # Weitere Standardmodifikatoren...
    
    def add_modifier(self, modifier: DicePoolModifier):
        """Fügt einen Modifikator hinzu."""
        self.modifiers.append(modifier)
    
    def calculate_pool(self, 
                      character_data: Dict[str, Any], 
                      check_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Berechnet den Würfelpool basierend auf allen anwendbaren Modifikatoren.
        
        Args:
            character_data: Daten des Charakters
            check_context: Kontext des Checks
            
        Returns:
            Dict mit action_dice, danger_dice und applied_modifiers
        """
        action_dice = 1  # Basis: 1 Action Die
        danger_dice = 0
        applied_modifiers = []
        
        for modifier in self.modifiers:
            if modifier.applies(character_data, check_context):
                action_dice += modifier.action_dice
                danger_dice += modifier.danger_dice
                applied_modifiers.append(str(modifier))
        
        # Manuelle Overrides aus dem Kontext
        action_dice += check_context.get("additional_action_dice", 0)
        danger_dice += check_context.get("additional_danger_dice", 0)
        
        # Sicherstellen, dass Werte nicht negativ werden
        action_dice = max(1, action_dice)  # Mindestens 1 Action Die
        danger_dice = max(0, danger_dice)
        
        return {
            "action_dice": action_dice,
            "danger_dice": danger_dice,
            "applied_modifiers": applied_modifiers
        }