# examples/dice_example.py
from cyberstory.mechanics.check_manager import CheckManager
from cyberstory.mechanics.nco_dice_system import NCODiceSystem


def main():
    # Würfelsystem erstellen
    dice_system = NCODiceSystem()
    
    # Check-Manager erstellen
    check_manager = CheckManager(dice_system)
    
    # Beispiel-Charakterdaten
    character_data = {
        "name": "Raven",
        "trademarks": ["Codeslinger", "Infiltrator"],
        "edges": ["Hacking", "Security Systems", "Stealth"],
        "traumas": ["Damaged Cybereye"],
        "conditions": []
    }
    
    # Beispiel-Checkkontext
    check_context = {
        "action": "Hackversuch auf ein Sicherheitssystem",
        "relevant_trademark": "Codeslinger",
        "relevant_edges": ["Hacking", "Security Systems"],
        "gear_tags": ["High-End Deck"],
        "advantageous_tags": ["Vorbereitete Exploits"],
        "disadvantageous_tags": ["Hochmoderne Firewall", "Zeitmangel"],
        "opposition_scale": 1
    }
    
    # Check durchführen
    check_result = check_manager.perform_check(character_data, check_context)
    
    # Ergebnisse ausgeben
    print("=== WÜRFELPROBE ===")
    print(check_manager.get_check_description(check_result["pool_details"]))
    print("\n=== ERGEBNIS ===")
    print(check_result["result"])

if __name__ == "__main__":
    main()