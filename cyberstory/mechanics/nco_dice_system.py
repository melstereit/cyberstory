import random
from typing import Dict, Any, Tuple

from cyberstory.mechanics.interfaces import DiceSystemInterface, DiceResult

class NCODiceSystem(DiceSystemInterface):
    """Implementierung des Neon City Overdrive Würfelsystems."""
    
    def perform_check(self, 
                     action_dice: int = 1, 
                     danger_dice: int = 0) -> DiceResult:
        """
        Führt einen Würfelwurf im NCO-System durch.
        
        Args:
            action_dice: Anzahl der Action Dice
            danger_dice: Anzahl der Danger Dice
            
        Returns:
            DiceResult: Das Ergebnis des Würfelwurfs
        """
        # Sicherstellen, dass mindestens 1 Action Die vorhanden ist
        action_dice = max(1, action_dice)
        danger_dice = max(0, danger_dice)
        
        # Würfeln
        action_results = [random.randint(1, 6) for _ in range(action_dice)]
        danger_results = [random.randint(1, 6) for _ in range(danger_dice)]
        
        # Neutralisierung von Action Dice durch Danger Dice
        remaining_dice = action_results.copy()
        
        for danger_value in danger_results:
            if danger_value in remaining_dice:
                remaining_dice.remove(danger_value)
        
        # Ergebnis bestimmen
        if not remaining_dice or all(d == 1 for d in remaining_dice):
            # Botch: keine Action Dice übrig oder nur 1er
            return DiceResult(
                success_level="botch",
                value=0,
                action_dice=action_results,
                danger_dice=danger_results,
                remaining_dice=remaining_dice,
                boons=0,
                is_botch=True
            )
        
        # Höchster verbleibender Würfel
        highest_value = max(remaining_dice)
        
        # Anzahl der 6er (Boons) zählen
        boons = remaining_dice.count(6) - 1 if highest_value == 6 else 0
        boons = max(0, boons)  # Sicherstellen, dass es nicht negativ wird
        
        # Erfolgsgrad bestimmen
        if highest_value == 6:
            success_level = "success"
        elif highest_value in [4, 5]:
            success_level = "partial"
        else:  # 1, 2, 3
            success_level = "failure"
        
        return DiceResult(
            success_level=success_level,
            value=highest_value,
            action_dice=action_results,
            danger_dice=danger_results,
            remaining_dice=remaining_dice,
            boons=boons,
            is_botch=False
        )
    
    def calculate_dice_pool(self, 
                           character_data: Dict[str, Any], 
                           check_context: Dict[str, Any]) -> Tuple[int, int]:
        """
        Berechnet den Würfelpool basierend auf Charakterdaten und Kontext.
        
        Args:
            character_data: Daten des Charakters
            check_context: Kontext des Checks (Aktion, relevante Trademarks/Edges, etc.)
            
        Returns:
            Tuple[int, int]: (action_dice, danger_dice)
        """
        action_dice = 1  # Basis: 1 Action Die
        danger_dice = 0
        
        # AKTION: Trademark
        if "relevant_trademark" in check_context and check_context["relevant_trademark"]:
            action_dice += 1
        
        # AKTION: Edges
        relevant_edges = check_context.get("relevant_edges", [])
        action_dice += len(relevant_edges)
        
        # AKTION: Ausrüstungstags
        gear_tags = check_context.get("gear_tags", [])
        action_dice += len(gear_tags)
        
        # AKTION: Vorteilhafte Tags
        advantageous_tags = check_context.get("advantageous_tags", [])
        action_dice += len(advantageous_tags)
        
        # GEFAHR: Traumas
        traumas = character_data.get("traumas", [])
        danger_dice += len(traumas)
        
        # GEFAHR: Bedingungen
        conditions = character_data.get("conditions", [])
        danger_dice += len(conditions)
        
        # GEFAHR: Hindernisse
        disadvantageous_tags = check_context.get("disadvantageous_tags", [])
        danger_dice += len(disadvantageous_tags)
        
        # GEFAHR: Gegner-Scale
        scale = check_context.get("opposition_scale", 0)
        danger_dice += scale
        
        # GEFAHR: Fehlende Ausrüstung
        if check_context.get("missing_gear", False):
            danger_dice += 1
        
        return action_dice, danger_dice