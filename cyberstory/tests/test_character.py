import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from character.manager import CharacterManager
from cyberstory.mechanics.interfaces import Trademark, Edge, Flaw, Drive, Item

def test_character_system():
    print("\n=== Charaktersystem-Test ===")
    
    # CharacterManager initialisieren
    char_manager = CharacterManager()
    
    # 1. Charakter erstellen
    print("\n1. Charakter erstellen:")
    char_data = char_manager.create_character("Raven", "Anarchisten")
    char_id = char_data.get("id")
    print(f"Charakter erstellt: {char_data['name']} (ID: {char_id})")
    
    # 2. Trademarks hinzufügen
    print("\n2. Trademarks hinzufügen:")
    trademark1 = Trademark(
        name="Codeslinger",
        triggers=["Hacking", "Security systems", "Computers"]
    )
    trademark2 = Trademark(
        name="Infiltrator",
        triggers=["Stealth", "Locks", "Security systems"]
    )
    
    char_manager.add_trademark(char_id, trademark1)
    char_manager.add_trademark(char_id, trademark2)
    print("Trademarks hinzugefügt: Codeslinger, Infiltrator")
    
    # 3. Edges hinzufügen
    print("\n3. Edges hinzufügen:")
    edge1 = Edge(name="Hacking", trademark="Codeslinger")
    edge2 = Edge(name="Security systems", trademark="Codeslinger")
    edge3 = Edge(name="Stealth", trademark="Infiltrator")
    
    char_manager.add_edge(char_id, edge1)
    char_manager.add_edge(char_id, edge2)
    char_manager.add_edge(char_id, edge3)
    print("Edges hinzugefügt: Hacking, Security systems, Stealth")
    
    # 4. Flaws hinzufügen
    print("\n4. Flaws hinzufügen:")
    flaw1 = Flaw(name="Wanted", description="Auf der Fahndungsliste von Osiris Corp")
    flaw2 = Flaw(name="Addiction", description="Abhängig von synthetischen Stimulanzien")
    
    char_manager.add_flaw(char_id, flaw1)
    char_manager.add_flaw(char_id, flaw2)
    print("Flaws hinzugefügt: Wanted, Addiction")
    
    # 5. Drive setzen
    print("\n5. Drive setzen:")
    drive = Drive(description="Clear my name from Osiris Corp's records")
    char_manager.set_drive(char_id, drive)
    print("Drive gesetzt: Clear my name from Osiris Corp's records")
    
    # 6. Ausrüstung hinzufügen
    print("\n6. Ausrüstung hinzufügen:")
    item1 = Item(name="High-End Deck", tags=["Fast", "Powerful", "Concealed"], is_special=True)
    item2 = Item(name="Pistol", tags=["Accurate", "Silenced"], is_special=True)
    item3 = Item(name="Synth-Leather Jacket", is_special=False)
    
    char_manager.add_item(char_id, item1)
    char_manager.add_item(char_id, item2)
    char_manager.add_item(char_id, item3)
    print("Ausrüstung hinzugefügt: High-End Deck, Pistol, Synth-Leather Jacket")

    # 7. Charakter laden und anzeigen
    print("\n7. Charakter laden und anzeigen:")
    updated_char = char_manager.get_character(char_id)
    if updated_char:
        print(f"Name: {updated_char['name']} (Fraktion: {updated_char['faction']})")
    else:
        print("ERROR: Could not retrieve character data!")
    
    # 8. Alle Charaktere anzeigen
    print("\n8. Alle Charaktere anzeigen:")
    all_chars = char_manager.get_all_characters()
    for char in all_chars:
        print(f"- {char['name']} (ID: {char['id']})")
    
    # 9. Charakter aktualisieren
    print("\n9. Charakter aktualisieren:")
    updates = {
        "stunt_points": 2,  # 1 ausgegeben
        "xp": 3,             # 3 XP verdient
        "add_trauma": "Damaged Cybereye"  # Trauma hinzufügen
    }
    
    char_manager.update_character(char_id, updates)
    updated_char = char_manager.get_character(char_id)
    print(f"Stunt Points: {updated_char['stunt_points']}")
    print(f"XP: {updated_char['xp']}")
    print(f"Traumas: {updated_char['traumas']}")
    
    # Wir löschen den Testcharakter nicht, um ihn für andere Tests zu behalten
    # char_manager.delete_character(char_id)  
    print("\nTest abgeschlossen.")

if __name__ == "__main__":
    test_character_system()