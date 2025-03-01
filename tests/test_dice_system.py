import sys
import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Füge das Projekt-Stammverzeichnis zum Python-Pfad hinzu
sys.path.insert(0, str(Path(__file__).parent.parent))

from cyberstory.mechanics.nco_dice_system import NCODiceSystem
from cyberstory.mechanics.check_manager import CheckManager


class TestDiceSystem(unittest.TestCase):
    """Tests für das Würfelsystem und den Check-Manager."""
    
    def setUp(self):
        """Richtet die Testumgebung ein."""
        self.dice_system = NCODiceSystem()
        self.check_manager = CheckManager(self.dice_system)
        
        # Beispiel-Charakterdaten und Check-Kontext für Tests
        self.character_data = {
            "id": "test-char",
            "name": "Test Charakter",
            "trademarks": {"Codeslinger": {"name": "Codeslinger"}},
            "traumas": []
        }
        
        self.check_context = {
            "action": "Hacken eines Terminals",
            "relevant_trademark": "Codeslinger",
            "relevant_edges": ["Hacking"],
            "gear_tags": ["High-End Deck"],
            "advantageous_tags": []
        }
    
    def test_dice_roll(self):
        """Testet einen einfachen Würfelwurf."""
        # Stelle sicher, dass ein Würfelwurf ein valides Ergebnis liefert
        result = self.dice_system.perform_check(3, 1)
        
        # Überprüfe die grundlegende Struktur des Ergebnisses
        self.assertIsNotNone(result)
        self.assertIn(result.success_level, ["success", "partial", "failure", "botch"])
        self.assertIsInstance(result.value, int)
        self.assertIsInstance(result.action_dice, list)
        self.assertIsInstance(result.danger_dice, list)
        self.assertIsInstance(result.remaining_dice, list)
        self.assertIsInstance(result.boons, int)
        self.assertIsInstance(result.is_botch, bool)
        
        # Überprüfe die Länge der Würfelergebnisse
        self.assertEqual(len(result.action_dice), 3)
        self.assertEqual(len(result.danger_dice), 1)
    
    def test_deterministic_dice_roll(self):
        """Testet einen Würfelwurf mit vorbestimmten Würfelergebnissen."""
        # Patchen der random.randint-Funktion, um deterministische Ergebnisse zu erhalten
        with patch('random.randint') as mock_randint:
            # Setze vorbestimmte Würfelergebnisse
            # Action dice: 2, 5, 6
            # Danger dice: 5
            mock_randint.side_effect = [2, 5, 6, 5]
            
            # Führe den Würfelwurf durch
            result = self.dice_system.perform_check(3, 1)
            
            # Überprüfe das Ergebnis
            self.assertEqual(result.action_dice, [2, 5, 6])
            self.assertEqual(result.danger_dice, [5])
            self.assertEqual(result.remaining_dice, [2, 6])  # 5 wird durch Danger Die neutralisiert
            self.assertEqual(result.value, 6)
            self.assertEqual(result.success_level, "success")
            self.assertEqual(result.boons, 0)  # Nur ein 6er, also keine Boons
            self.assertFalse(result.is_botch)
    
    def test_dice_pool_calculation(self):
        """Testet die Berechnung des Würfelpools."""
        action_dice, danger_dice = self.dice_system.calculate_dice_pool(
            self.character_data, self.check_context
        )
        
        # Überprüfe die berechneten Würfelanzahlen
        # 1 (Basis) + 1 (Trademark) + 1 (Edge) + 1 (Gear Tag) = 4 Action Dice
        # 0 (keine Traumas oder andere negative Modifikatoren) = 0 Danger Dice
        self.assertEqual(action_dice, 4)
        self.assertEqual(danger_dice, 0)
        
        # Teste mit Traumas
        character_with_trauma = self.character_data.copy()
        character_with_trauma["traumas"] = ["Damaged Cybereye"]
        
        action_dice, danger_dice = self.dice_system.calculate_dice_pool(
            character_with_trauma, self.check_context
        )
        
        # Das Trauma sollte einen Danger Die hinzufügen
        self.assertEqual(danger_dice, 1)
    
    def test_check_manager(self):
        """Testet den Check-Manager."""
        # Patchen der perform_check-Methode des DiceSystem, um deterministische Ergebnisse zu erhalten
        with patch.object(self.dice_system, 'perform_check') as mock_perform_check:
            # Setze ein vorbestimmtes Ergebnis
            mock_result = MagicMock()
            mock_result.success_level = "success"
            mock_result.value = 6
            mock_result.to_dict.return_value = {
                "success_level": "success",
                "value": 6,
                "action_dice": [4, 5, 6],
                "danger_dice": [3],
                "remaining_dice": [4, 5, 6],
                "boons": 0,
                "is_botch": False
            }
            mock_perform_check.return_value = mock_result
            
            # Führe den Check durch
            check_result = self.check_manager.perform_check(
                self.character_data, self.check_context
            )
            
            # Überprüfe das Ergebnis
            self.assertIsNotNone(check_result)
            self.assertIn("result", check_result)
            self.assertIn("pool_details", check_result)
            self.assertIn("check_id", check_result)
            self.assertEqual(check_result["result"].success_level, "success")
            self.assertEqual(check_result["result"].value, 6)
    
    def test_modifiers(self):
        """Testet, ob Modifikatoren korrekt angewendet werden."""
        # Test mit zusätzlichen negativen Modifikatoren im Kontext
        context_with_modifiers = self.check_context.copy()
        context_with_modifiers["disadvantageous_tags"] = ["Lauter Umgebungslärm", "Schlechte Beleuchtung"]
        
        action_dice, danger_dice = self.dice_system.calculate_dice_pool(
            self.character_data, context_with_modifiers
        )
        
        # Die negativen Tags sollten Danger Dice hinzufügen
        self.assertEqual(danger_dice, 2)
        
        # Test mit zusätzlichen positiven Modifikatoren
        context_with_modifiers["advantageous_tags"] = ["Bekanntes System", "Zeit zur Vorbereitung"]
        
        action_dice, danger_dice = self.dice_system.calculate_dice_pool(
            self.character_data, context_with_modifiers
        )
        
        # Die positiven Tags sollten Action Dice hinzufügen (zusätzlich zu den bereits vorhandenen)
        self.assertEqual(action_dice, 6)  # 1 (Basis) + 1 (Trademark) + 1 (Edge) + 1 (Gear) + 2 (adv. Tags)


def manual_test_dice_system():
    """
    Manuelle Testfunktion für das Würfelsystem.
    Diese Funktion wird nicht automatisch ausgeführt, wenn die Datei als unittest ausgeführt wird,
    sondern muss explizit aufgerufen werden.
    """
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


# Diese Funktion wird aufgerufen, wenn die Datei direkt ausgeführt wird
if __name__ == "__main__":
    # Wenn die Datei direkt ausgeführt wird, führe entweder den manuellen Test aus...
    # manual_test_dice_system()
    
    # ...oder führe die unittest-Tests aus
    unittest.main()