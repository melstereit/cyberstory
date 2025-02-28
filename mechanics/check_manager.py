# mechanics/check_manager.py
from mechanics.interfaces import DiceSystemInterface, DiceResult
from mechanics.modifiers import ModifierManager
from typing import Dict, List, Any, Optional

class CheckManager:
    """Verwaltet die Durchführung von Würfelproben."""
    
    def __init__(self, dice_system: DiceSystemInterface):
        """
        Initialisiert den Check-Manager.
        
        Args:
            dice_system: Das zu verwendende Würfelsystem
        """
        self.dice_system = dice_system
        self.modifier_manager = ModifierManager()
    
    def perform_check(self, 
                     character_data: Dict[str, Any], 
                     check_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Führt eine Würfelprobe durch.
        
        Args:
            character_data: Daten des Charakters
            check_context: Kontext des Checks
            
        Returns:
            Dict mit result (DiceResult) und pool_details
        """
        # Würfelpool berechnen
        pool_details = self.modifier_manager.calculate_pool(character_data, check_context)
        action_dice = pool_details["action_dice"]
        danger_dice = pool_details["danger_dice"]
        
        # Würfelprobe durchführen
        result = self.dice_system.perform_check(action_dice, danger_dice)
        
        return {
            "result": result,
            "pool_details": pool_details
        }
    
    def get_check_description(self, pool_details: Dict[str, Any]) -> str:
        """
        Erzeugt eine Beschreibung des Würfelpools.
        
        Args:
            pool_details: Die Würfelpool-Details
            
        Returns:
            Formatierte Beschreibung des Würfelpools
        """
        description = f"Würfelpool: {pool_details['action_dice']} Action Dice vs. {pool_details['danger_dice']} Danger Dice\n"
        
        if pool_details["applied_modifiers"]:
            description += "Angewendete Modifikatoren:\n"
            for modifier in pool_details["applied_modifiers"]:
                description += f"- {modifier}\n"
        
        return description