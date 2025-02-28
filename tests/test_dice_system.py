# tests/test_dice_system.py
import random
import unittest

from cyberstory import NCODiceSystem


class TestNCODiceSystem(unittest.TestCase):
    
    def setUp(self):
        self.dice_system = NCODiceSystem()
    
    def test_basic_roll(self):
        """Testet einen einfachen Würfelwurf."""
        # Seed für Reproduzierbarkeit
        random.seed(42)
        
        result = self.dice_system.perform_check(3, 1)
        
        self.assertEqual(len(result.action_dice), 3)
        self.assertEqual(len(result.danger_dice), 1)
        
        # Mit dem Seed 42 erwartete Werte
        self.assertEqual(result.action_dice, [1, 6, 5])
        self.assertEqual(result.danger_dice, [3])
        
        # Danger Die sollte kein Action Die neutralisieren
        self.assertEqual(result.remaining_dice, [1, 6, 5])
        
        # Höchster Wert ist 6
        self.assertEqual(result.value, 6)
        self.assertEqual(result.success_level, "success")
        self.assertEqual(result.boons, 0)  # Nur ein 6er, also kein Boon
    
    def test_neutralization(self):
        """Testet die Neutralisierung von Action Dice."""
        # Manueller Testfall mit fester Ausgabe
        dice_system = NCODiceSystem()
        
        # Mock für random.randint
        original_randint = random.randint
        
        try:
            # Action Dice: 4, 2, 6
            # Danger Dice: 4, 2
            # Nach Neutralisierung: 6
            random.randint = lambda a, b: [4, 2, 6, 4, 2][random.randint.call_count - 1]
            random.randint.call_count = 1
            
            result = dice_system.perform_check(3, 2)
            
            self.assertEqual(result.action_dice, [4, 2, 6])
            self.assertEqual(result.danger_dice, [4, 2])
            self.assertEqual(result.remaining_dice, [6])
            self.assertEqual(result.value, 6)
            self.assertEqual(result.success_level, "success")
            self.assertEqual(result.boons, 0)
        finally:
            random.randint = original_randint
    
    def test_botch(self):
        """Testet einen kritischen Misserfolg (Botch)."""
        dice_system = NCODiceSystem()
        
        # Mock für random.randint
        original_randint = random.randint
        
        try:
            # Action Dice: 1, 1, 3
            # Danger Dice: 3
            # Nach Neutralisierung: 1, 1
            # Alle verbleibenden Würfel sind 1, daher Botch
            random.randint = lambda a, b: [1, 1, 3, 3][random.randint.call_count - 1]
            random.randint.call_count = 1
            
            result = dice_system.perform_check(3, 1)
            
            self.assertEqual(result.action_dice, [1, 1, 3])
            self.assertEqual(result.danger_dice, [3])
            self.assertEqual(result.remaining_dice, [1, 1])
            self.assertTrue(result.is_botch)
            self.assertEqual(result.success_level, "botch")
        finally:
            random.randint = original_randint

if __name__ == "__main__":
    unittest.main()