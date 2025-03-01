#!/usr/bin/env python3
"""
Debug-Skript für die Charaktererstellung
Dieses Skript prüft Schritt für Schritt die Probleme in der Charaktererstellung.
"""

import sys
import os
from pathlib import Path
import json

# Füge das Projekt-Stammverzeichnis zum Python-Pfad hinzu
sys.path.insert(0, str(Path(__file__).parent))

from cyberstory.character.manager import CharacterManager
from cyberstory.character.creation import CharacterCreation
from cyberstory.character.templates import TemplateManager
from cyberstory.character.gear_manager import GearManager
from cyberstory.mechanics.interfaces import Trademark, Edge, Flaw, Drive, Item


def debug_print(title, value):
    """Gibt einen Wert formatiert aus"""
    print(f"\n{'-'*20} {title} {'-'*20}")
    if isinstance(value, dict) or isinstance(value, list):
        print(json.dumps(value, indent=2))
    else:
        print(value)


def debug_character_creation():
    """Debugt den Charaktererstellungsprozess"""
    print("\n=== Debug der Charaktererstellung ===")
    
    # Initialisiere die Manager
    char_manager = CharacterManager()
    template_manager = TemplateManager()
    gear_manager = GearManager()
    
    # Initialisiere die Charaktererstellung
    creation = CharacterCreation(char_manager, template_manager, gear_manager)
    
    # 1. Erstelle einen Testcharakter
    print("\n1. Erstelle einen Testcharakter")
    character_data = creation.start_creation("DebugChar", "Anarchisten")
    char_id = character_data.get("id")
    debug_print("Ursprünglicher Charakter", character_data)
    
    # 2. Füge Trademarks hinzu
    print("\n2. Füge Trademarks hinzu")
    trademark1 = Trademark(
        name="Codeslinger",
        triggers=["Hacking", "Security systems", "Computers"]
    )
    trademark2 = Trademark(
        name="Infiltrator",
        triggers=["Stealth", "Locks", "Security systems"]
    )
    
    # Prüfe add_trademark
    result1 = creation.add_trademark_to_character(trademark1.name, trademark1.triggers)
    result2 = creation.add_trademark_to_character(trademark2.name, trademark2.triggers)
    
    debug_print("Ergebnis Trademark 1", result1)
    debug_print("Ergebnis Trademark 2", result2)
    
    # Prüfe den Zustand nach dem Hinzufügen
    char_data = char_manager.get_character(char_id)
    debug_print("Charakter nach Trademark-Hinzufügung", char_data)
    
    # 3. Füge Edges hinzu
    print("\n3. Füge Edges hinzu")
    edge1 = Edge(name="Hacking", trademark="Codeslinger")
    edge2 = Edge(name="Stealth", trademark="Infiltrator")
    
    # Prüfe add_edge
    result1 = creation.add_edge_to_character(edge1.name, edge1.trademark)
    result2 = creation.add_edge_to_character(edge2.name, edge2.trademark)
    
    debug_print("Ergebnis Edge 1", result1)
    debug_print("Ergebnis Edge 2", result2)
    
    # Prüfe den Zustand nach dem Hinzufügen
    char_data = char_manager.get_character(char_id)
    debug_print("Charakter nach Edge-Hinzufügung", char_data)
    
    # 4. Füge Flaws hinzu
    print("\n4. Füge Flaws hinzu")
    flaw1 = Flaw(name="Wanted", description="Auf der Fahndungsliste von Osiris Corp")
    flaw2 = Flaw(name="Addiction", description="Abhängig von synthetischen Stimulanzien")
    
    # Prüfe add_flaw
    try:
        # Schaue in der CharacterCreation-Klasse nach
        if hasattr(creation, 'add_flaw_to_character') and callable(creation.add_flaw_to_character):
            debug_print("Creation.add_flaw_to_character existiert", "JA")
            result1 = creation.add_flaw_to_character(flaw1.name, flaw1.description)
            debug_print("Ergebnis Flaw 1", result1)
        else:
            debug_print("Creation.add_flaw_to_character existiert", "NEIN")
        
        # Versuche es direkt über CharacterManager
        if hasattr(char_manager, 'add_flaw') and callable(char_manager.add_flaw):
            debug_print("CharManager.add_flaw existiert", "JA")
            result2 = char_manager.add_flaw(char_id, flaw2)
            debug_print("Ergebnis Flaw 2", result2)
        else:
            debug_print("CharManager.add_flaw existiert", "NEIN")
            
            # Inspiziere den Code (Implementierung fehlt?)
            import inspect
            if hasattr(char_manager, 'add_flaw'):
                debug_print("CharManager.add_flaw Code", inspect.getsource(char_manager.add_flaw))
            
    except Exception as e:
        debug_print("FEHLER bei Flaw-Hinzufügung", str(e))
    
    # Prüfe den Zustand nach dem Hinzufügen
    char_data = char_manager.get_character(char_id)
    debug_print("Charakter nach Flaw-Hinzufügung", char_data)
    
    # 5. Setze Drive
    print("\n5. Setze Drive")
    drive = Drive(description="Clear my name from Osiris Corp's records")
    
    # Prüfe set_drive
    try:
        if hasattr(creation, 'set_drive_for_character') and callable(creation.set_drive_for_character):
            debug_print("Creation.set_drive_for_character existiert", "JA")
            result = creation.set_drive_for_character(drive.description)
            debug_print("Ergebnis Drive setzen", result)
        else:
            debug_print("Creation.set_drive_for_character existiert", "NEIN")
        
        # Versuche es direkt über CharacterManager
        if hasattr(char_manager, 'set_drive') and callable(char_manager.set_drive):
            debug_print("CharManager.set_drive existiert", "JA")
            result = char_manager.set_drive(char_id, drive)
            debug_print("Ergebnis Drive setzen (direkt)", result)
        else:
            debug_print("CharManager.set_drive existiert", "NEIN")
            
            # Inspiziere den Code (Implementierung fehlt?)
            import inspect
            if hasattr(char_manager, 'set_drive'):
                debug_print("CharManager.set_drive Code", inspect.getsource(char_manager.set_drive))
            
    except Exception as e:
        debug_print("FEHLER bei Drive setzen", str(e))
    
    # Prüfe den Zustand nach dem Hinzufügen
    char_data = char_manager.get_character(char_id)
    debug_print("Charakter nach Drive setzen", char_data)
    
    # 6. Füge Ausrüstung hinzu
    print("\n6. Füge Ausrüstung hinzu")
    item1 = Item(name="High-End Deck", tags=["Fast", "Powerful", "Concealed"], is_special=True)
    
    # Prüfe roll_for_gear und add_item
    try:
        if hasattr(creation, 'roll_for_gear') and callable(creation.roll_for_gear):
            debug_print("Creation.roll_for_gear existiert", "JA")
            
            # Inspiziere die Methode
            import inspect
            debug_print("Creation.roll_for_gear Code", inspect.getsource(creation.roll_for_gear))
            
            result = creation.roll_for_gear(item1.name, "", item1.tags)
            debug_print("Ergebnis Gear-Roll", result)
        else:
            debug_print("Creation.roll_for_gear existiert", "NEIN")
        
        # Versuche es direkt über CharacterManager
        if hasattr(char_manager, 'add_item') and callable(char_manager.add_item):
            debug_print("CharManager.add_item existiert", "JA")
            result = char_manager.add_item(char_id, item1)
            debug_print("Ergebnis Item hinzufügen (direkt)", result)
        else:
            debug_print("CharManager.add_item existiert", "NEIN")
            
            # Inspiziere den Code (Implementierung fehlt?)
            import inspect
            if hasattr(char_manager, 'add_item'):
                debug_print("CharManager.add_item Code", inspect.getsource(char_manager.add_item))
            
    except Exception as e:
        debug_print("FEHLER bei Ausrüstung hinzufügen", str(e))
    
    # Prüfe den Zustand nach dem Hinzufügen
    char_data = char_manager.get_character(char_id)
    debug_print("Charakter nach Ausrüstung hinzufügen", char_data)
    
    # 7. Abschließender Zustand
    print("\n7. Kompletter Charakter am Ende")
    character_data = creation.complete_creation()
    debug_print("Abschließender Charakter", character_data)
    
    print("\nDebug abgeschlossen.")


if __name__ == "__main__":
    debug_character_creation()