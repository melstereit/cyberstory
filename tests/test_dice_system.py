# tests/test_dice_system.py
import random
import unittest
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import from cyberstory
from cyberstory.mechanics.nco_dice_system import NCODiceSystem
from mechanics.check_manager import CheckManager

def test_dice_system():
    print("\n=== Würfelsystem-Test ===")
    dice_system = NCODiceSystem()
    
    # Einfacher Würfelwurf
    print("\n1. Einfacher Würfelwurf (3 Action, 1 Danger):")
    result = dice_system.perform_check(3, 1)
    print(f"Action Dice: {result.action_dice}")
    print(f"Danger Dice: {result.danger_dice}")
    print(f"Verbleibende Würfel: {result.remaining_dice}")
    print(f"Höchstes Ergebnis: {result.value}")
    print(f"Erfolgsgrad: {result.success_level}")
    print(f"Boons: {result.boons}")
    
    # Check-Manager
    print("\n2. Check mit Check-Manager:")
    check_manager = CheckManager(dice_system)
    
    # Beispiel-Charakterdaten und Check-Kontext
    character_data = {
        "id": "test-char",
        "name": "Test Charakter",
        "trademarks": {"Codeslinger": {"name": "Codeslinger"}},
        "traumas": []
    }
    
    check_context = {
        "action": "Hacken eines Terminals",
        "relevant_trademark": "Codeslinger",
        "relevant_edges": ["Hacking"],
        "gear_tags": ["High-End Deck"],
        "advantageous_tags": []
    }
    
    check_result = check_manager.perform_check(character_data, check_context)
    print(check_manager.get_check_description(check_result["pool_details"]))
    print(f"Ergebnis: {check_result['result'].success_level} (Wert: {check_result['result'].value})")
    print(f"Check-ID: {check_result['check_id']}")

if __name__ == "__main__":
    test_dice_system()