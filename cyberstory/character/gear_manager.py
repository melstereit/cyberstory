# character/gear_manager.py
import json
import os
import random
from typing import Optional

from cyberstory.mechanics.interfaces import Item


class GearManager:
    """Verwaltet Ausrüstungsgegenstände."""
    
    def __init__(self, gear_file: str = "data/templates/gear.json"):
        """
        Initialisiert den GearManager.
        
        Args:
            gear_file: Pfad zur JSON-Datei für die Ausrüstungsdaten
        """
        self.gear_file = gear_file
        
        # Verzeichnis erstellen, falls es nicht existiert
        os.makedirs(os.path.dirname(gear_file), exist_ok=True)
        
        # Ausrüstungsdaten
        self.gear_categories = {}  # name -> list of items
        
        # Daten laden, falls vorhanden
        self.load_data()
    
    def load_data(self) -> bool:
        """
        Lädt Ausrüstungsdaten aus der JSON-Datei.
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        try:
            if os.path.exists(self.gear_file):
                with open(self.gear_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.gear_categories = data
                return True
            else:
                # Erstelle Standarddatei, wenn sie nicht existiert
                self._create_default_gear()
                return True
                
        except Exception as e:
            print(f"Fehler beim Laden der Ausrüstungsdaten: {e}")
        
        return False
    
    def _create_default_gear(self) -> None:
        """Erstellt Standardausrüstungsdaten."""
        default_gear = {
            "ranged_weapons": [
                {
                    "name": "Light Pistol",
                    "tags": ["Concealed", "Quick draw"],
                    "description": "A small, easily concealable handgun."
                },
                {
                    "name": "Heavy Pistol",
                    "tags": ["Intimidating", "Armor piercing"],
                    "description": "A large-caliber handgun with stopping power."
                },
                # Weitere aus dem Original-Dokument...
            ],
            "melee_weapons": [
                {
                    "name": "Switchblade",
                    "tags": ["Concealed", "Quick"],
                    "description": "A concealable blade that flips out with the press of a button."
                },
                {
                    "name": "Monofilament Whip",
                    "tags": ["Deadly", "Reach"],
                    "description": "An almost invisible whip that can cut through most materials."
                },
                # Weitere aus dem Original-Dokument...
            ],
            "armor": [
                {
                    "name": "Armored Jacket",
                    "tags": ["Bullet proof", "Concealed"],
                    "description": "A stylish jacket with bulletproof panels."
                },
                {
                    "name": "Combat Armor",
                    "tags": ["Bullet proof", "Energy absorption", "Exoskeleton"],
                    "description": "Heavy-duty armor for serious combat situations."
                },
                # Weitere aus dem Original-Dokument...
            ],
            "vehicles": [
                {
                    "name": "Motorcycle",
                    "tags": ["Fast", "Agile"],
                    "description": "A standard motorcycle for quick transportation."
                },
                {
                    "name": "Hoverbike",
                    "tags": ["Fly", "Fast", "Flashy"],
                    "description": "A flashy flying bike that hovers above the ground."
                },
                # Weitere aus dem Original-Dokument...
            ],
            "tools": [
                {
                    "name": "Medipack",
                    "tags": ["Portable", "Well-stocked"],
                    "description": "A kit with medical supplies for emergency treatment."
                },
                {
                    "name": "B&E Kit",
                    "tags": ["Concealed", "Quiet"],
                    "description": "Tools for breaking and entering without making noise."
                },
                # Weitere aus dem Original-Dokument...
            ],
            "cyberware": [
                {
                    "name": "Cyber Eyes",
                    "tags": ["Thermal imaging", "Camera", "HUD"],
                    "description": "Replacement eyes with enhanced capabilities."
                },
                {
                    "name": "Wired Reflexes",
                    "tags": ["Fast", "Quick draw"],
                    "description": "Neural enhancements that speed up reaction time."
                },
                # Weitere aus dem Original-Dokument...
            ]
        }
        
        with open(self.gear_file, 'w', encoding='utf-8') as f:
            json.dump(default_gear, f, ensure_ascii=False, indent=2)
        
        self.gear_categories = default_gear
    
    def get_item(self, category: str, name: str) -> Optional[Item]:
        """
        Gibt ein bestimmtes Item zurück.
        
        Args:
            category: Kategorie des Items
            name: Name des Items
        
        Returns:
            Item-Objekt oder None
        """
        if category in self.gear_categories:
            for item_data in self.gear_categories[category]:
                if item_data.get("name") == name:
                    return Item(
                        name=item_data.get("name", ""),
                        tags=item_data.get("tags", []),
                        description=item_data.get("description", ""),
                        is_special=True  # Standardmäßig als spezielles Item betrachten
                    )
        
        return None
    
    def get_random_item(self, category: str = None) -> Optional[Item]:
        """
        Gibt ein zufälliges Item zurück.
        
        Args:
            category: Kategorie (optional)
        
        Returns:
            Item-Objekt oder None
        """
        if not category:
            # Zufällige Kategorie
            if not self.gear_categories:
                return None
            
            category = random.choice(list(self.gear_categories.keys()))
        
        if category in self.gear_categories and self.gear_categories[category]:
            item_data = random.choice(self.gear_categories[category])
            return Item(
                name=item_data.get("name", ""),
                tags=item_data.get("tags", []),
                description=item_data.get("description", ""),
                is_special=True  # Standardmäßig als spezielles Item betrachten
            )
        
        return None
    
    def roll_for_gear(self, num_tags: int) -> bool:
        """
        Würfelt für ein Ausrüstungsstück mit der angegebenen Anzahl von Tags.
        
        Args:
            num_tags: Anzahl der Tags
        
        Returns:
            bool: True, wenn der Wurf erfolgreich war (>= num_tags), sonst False
        """
        roll = random.randint(1, 6)
        return roll >= num_tags