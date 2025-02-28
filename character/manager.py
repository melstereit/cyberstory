# character/manager.py
from character.interfaces import CharacterInterface, Trademark, Edge, Flaw, Drive, Item
from character.character import Character
from typing import Dict, List, Any, Optional
import json
import os

class CharacterManager(CharacterInterface):
    """Verwaltet Charaktere und deren Persistenz."""
    
    def __init__(self, data_file: str = "data/characters.json"):
        """
        Initialisiert den CharacterManager.
        
        Args:
            data_file: Pfad zur JSON-Datei für die Charakterdaten
        """
        self.data_file = data_file
        self.characters = {}  # id -> Character
        
        # Verzeichnis erstellen, falls es nicht existiert
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        
        # Daten laden, falls vorhanden
        self.load_data()
    
    def load_data(self) -> bool:
        """
        Lädt Charakterdaten aus der JSON-Datei.
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    for char_data in data.get("characters", []):
                        character = Character.from_dict(char_data)
                        self.characters[character.id] = character
                
                return True
        except Exception as e:
            print(f"Fehler beim Laden der Charakterdaten: {e}")
        
        return False
    
    def save_data(self) -> bool:
        """
        Speichert Charakterdaten in der JSON-Datei.
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        try:
            data = {
                "characters": [char.to_dict() for char in self.characters.values()]
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Fehler beim Speichern der Charakterdaten: {e}")
        
        return False
    
    def create_character(self, name: str, faction: str = None) -> Dict[str, Any]:
        """
        Erstellt einen neuen Charakter.
        
        Args:
            name: Name des Charakters
            faction: Fraktion des Charakters
        
        Returns:
            Dict mit den Charakterdaten oder leeres Dict bei Fehler
        """
        try:
            character = Character(name=name, faction=faction)
            self.characters[character.id] = character
            self.save_data()
            return character.to_dict()
        except Exception as e:
            print(f"Fehler beim Erstellen des Charakters: {e}")
        
        return {}
    
    def add_trademark(self, character_id: str, trademark: Trademark) -> bool:
        """
        Fügt einem Charakter ein Trademark hinzu.
        
        Args:
            character_id: ID des Charakters
            trademark: Das hinzuzufügende Trademark
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if character_id not in self.characters:
            return False
        
        result = self.characters[character_id].add_trademark(trademark)
        if result:
            self.save_data()
        
        return result
    
    def add_edge(self, character_id: str, edge: Edge) -> bool:
        """
        Fügt einem Charakter einen Edge hinzu.
        
        Args:
            character_id: ID des Charakters
            edge: Der hinzuzufügende Edge
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if character_id not in self.characters:
            return False
        
        result = self.characters[character_id].add_edge(edge)
        if result:
            self.save_data()
        
        return result
    
    def add_flaw(self, character_id: str, flaw: Flaw) -> bool:
        """
        Fügt einem Charakter einen Flaw hinzu.
        
        Args:
            character_id: ID des Charakters
            flaw: Der hinzuzufügende Flaw
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if character_id not in self.characters:
            return False
        
        result = self.characters[character_id].add_flaw(flaw)
        if result:
            self.save_data()
        
        return result
    
    def set_drive(self, character_id: str, drive: Drive) -> bool:
        """
        Setzt den Drive eines Charakters.
        
        Args:
            character_id: ID des Charakters
            drive: Der Drive des Charakters
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if character_id not in self.characters:
            return False
        
        result = self.characters[character_id].set_drive(drive)
        if result:
            self.save_data()
        
        return result
    
    def add_item(self, character_id: str, item: Item) -> bool:
        """
        Fügt ein Item zum Inventar eines Charakters hinzu.
        
        Args:
            character_id: ID des Charakters
            item: Das hinzuzufügende Item
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if character_id not in self.characters:
            return False
        
        result = self.characters[character_id].add_item(item)
        if result:
            self.save_data()
        
        return result
    
    def get_character(self, character_id: str) -> Optional[Dict[str, Any]]:
        """
        Gibt die Charakterdaten zurück.
        
        Args:
            character_id: ID des Charakters
        
        Returns:
            Dict mit den Charakterdaten oder None bei Fehler
        """
        if character_id in self.characters:
            return self.characters[character_id].to_dict()
        
        return None
    
    def update_character(self, character_id: str, updates: Dict[str, Any]) -> bool:
        """
        Aktualisiert die Charakterdaten.
        
        Args:
            character_id: ID des Charakters
            updates: Dictionary mit den zu aktualisierenden Werten
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if character_id not in self.characters:
            return False
        
        character = self.characters[character_id]
        
        try:
            # Aktualisiere einfache Werte
            if "name" in updates:
                character.name = updates["name"]
            
            if "faction" in updates:
                character.faction = updates["faction"]
            
            if "stunt_points" in updates:
                character.stunt_points = updates["stunt_points"]
            
            if "xp" in updates:
                character.xp = updates["xp"]
            
            # Komplexere Updates
            
            # Hit Track
            if "hit_track" in updates:
                character.hit_track = updates["hit_track"]
            
            # Traumas
            if "add_trauma" in updates:
                character.add_trauma(updates["add_trauma"])
            
            if "remove_trauma" in updates:
                character.remove_trauma(updates["remove_trauma"])
            
            # Conditions
            if "add_condition" in updates:
                character.add_condition(updates["add_condition"])
            
            if "remove_condition" in updates:
                character.remove_condition(updates["remove_condition"])
            
            # Drive Track
            if "tick_drive" in updates and isinstance(updates["tick_drive"], int):
                if character.drive:
                    character.drive.tick(updates["tick_drive"])
            
            if "cross_drive" in updates and isinstance(updates["cross_drive"], int):
                if character.drive:
                    character.drive.cross_out(updates["cross_drive"])
            
            self.save_data()
            return True
            
        except Exception as e:
            print(f"Fehler beim Aktualisieren des Charakters: {e}")
        
        return False
    
    def get_all_characters(self) -> List[Dict[str, Any]]:
        """
        Gibt eine Liste aller Charaktere zurück.
        
        Returns:
            Liste von Dictionaries mit den Charakterdaten
        """
        return [char.to_dict() for char in self.characters.values()]
    
    def delete_character(self, character_id: str) -> bool:
        """
        Löscht einen Charakter.
        
        Args:
            character_id: ID des Charakters
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        if character_id in self.characters:
            del self.characters[character_id]
            self.save_data()
            return True
        
        return False