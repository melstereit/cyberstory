# character/manager.py
import json
import os
from typing import Dict, List, Any, Optional

from cyberstory import Character
from cyberstory import CharacterInterface, Trademark, Edge, Flaw, Drive, Item

class CharacterManager(CharacterInterface):
    """Verwaltet Charaktere und deren Persistenz."""
    
    def __init__(self, data_dir: str = "data/characters"):
        """
        Initialisiert den CharacterManager.
        
        Args:
            data_dir: Verzeichnis für die Charakterdaten
        """
        self.db = JSONDatabase(data_dir)
        self.characters = {}  # id -> Character (Cache)
        
        # Lade die Charaktere in den Cache
        self._load_characters()
    
    def _load_characters(self) -> None:
        """Lädt alle Charaktere in den Cache."""
        for char_data in self.db.list_all():
            character = Character.from_dict(char_data)
            self.characters[character.id] = character
    
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
            
            # In der Datenbank speichern
            self.db.save(character.to_dict())
            
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
            # In der Datenbank aktualisieren
            self.db.save(self.characters[character_id].to_dict())
        
        return result
    
    # ... (weitere Methoden wie add_edge, add_flaw usw. ähnlich anpassen)
    
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
        
        # Versuche, aus der Datenbank zu laden
        char_data = self.db.load(character_id)
        if char_data:
            character = Character.from_dict(char_data)
            self.characters[character_id] = character
            return character.to_dict()
        
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
            char_data = self.db.load(character_id)
            if char_data:
                self.characters[character_id] = Character.from_dict(char_data)
            else:
                return False
        
        character = self.characters[character_id]
        
        try:
            # Aktualisiere die Charakterdaten
            # (Implementation wie zuvor)
            
            # In der Datenbank aktualisieren
            self.db.save(character.to_dict())
            
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
        # Lade alle Charaktere neu aus der Datenbank
        self._load_characters()
        
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
        
        return self.db.delete(character_id)
