# data/json_database.py
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Type, TypeVar

from cyberstory.data.data_interfaces import DatabaseInterface

T = TypeVar('T')

class JSONDatabase(DatabaseInterface[T]):
    """
    Implementierung einer einfachen JSON-Datenbank.
    
    Diese Klasse bietet grundlegende CRUD-Operationen für JSON-Dateien.
    Jeder Datensatz wird als einzelne JSON-Datei gespeichert, wobei der Dateiname
    auf dem ID-Feld basiert.
    """
    
    def __init__(self, data_dir: str, model_class: Type[T] = dict):
        """
        Initialisiert die JSON-Datenbank.
        
        Args:
            data_dir: Verzeichnis für die JSON-Dateien
            model_class: Klasse zum Deserialisieren der Daten (Standard: dict)
        """
        self.data_dir = Path(data_dir)
        self.model_class = model_class
        
        # Verzeichnis erstellen, falls es nicht existiert
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _get_file_path(self, id_value: str) -> Path:
        """
        Erzeugt den Dateipfad für eine ID.
        
        Args:
            id_value: Der Wert des ID-Feldes
            
        Returns:
            Path: Der Dateipfad
        """
        return self.data_dir / f"{id_value}.json"
    
    def save(self, data: T, id_field: str = "id") -> bool:
        """
        Speichert Daten in einer JSON-Datei.
        
        Args:
            data: Die zu speichernden Daten
            id_field: Der Name des ID-Feldes (Standard: "id")
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            # ID-Wert extrahieren
            if isinstance(data, dict):
                id_value = data.get(id_field)
            else:
                id_value = getattr(data, id_field, None)
            
            if not id_value:
                raise ValueError(f"Keine gültige ID gefunden. Das Feld '{id_field}' fehlt oder ist leer.")
            
            # Daten serialisieren
            if hasattr(data, "to_dict"):
                data_dict = data.to_dict()
            elif hasattr(data, "__dict__"):
                data_dict = data.__dict__
            else:
                data_dict = data
            
            # JSON-Datei schreiben
            file_path = self._get_file_path(id_value)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, ensure_ascii=False, indent=2)
            
            return True
        
        except Exception as e:
            print(f"Fehler beim Speichern der Daten: {e}")
            return False
    
    def load(self, id_value: str = None) -> Optional[T]:
        """
        Lädt Daten aus einer JSON-Datei.
        
        Args:
            id_value: Der Wert des ID-Feldes (wenn None, wird ein leeres dict zurückgegeben)
            
        Returns:
            Die geladenen Daten oder None bei Fehler
        """
        try:
            if id_value is None:
                return self.model_class() if callable(self.model_class) else None
            
            file_path = self._get_file_path(id_value)
            
            if not file_path.exists():
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data_dict = json.load(f)
            
            # Daten deserialisieren
            if self.model_class == dict:
                return data_dict
            elif hasattr(self.model_class, "from_dict"):
                return self.model_class.from_dict(data_dict)
            else:
                return self.model_class(**data_dict)
        
        except Exception as e:
            print(f"Fehler beim Laden der Daten: {e}")
            return None
    
    def update(self, id_value: str, updates: Dict[str, Any], id_field: str = "id") -> bool:
        """
        Aktualisiert Daten in einer JSON-Datei.
        
        Args:
            id_value: Der Wert des ID-Feldes
            updates: Die zu aktualisierenden Felder und ihre neuen Werte
            id_field: Der Name des ID-Feldes (Standard: "id")
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            # Daten laden
            data = self.load(id_value)
            
            if data is None:
                return False
            
            # Daten aktualisieren
            if isinstance(data, dict):
                data.update(updates)
            else:
                for key, value in updates.items():
                    setattr(data, key, value)
            
            # Daten speichern
            return self.save(data, id_field)
        
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Daten: {e}")
            return False
    
    def delete(self, id_value: str, id_field: str = "id") -> bool:
        """
        Löscht eine JSON-Datei.
        
        Args:
            id_value: Der Wert des ID-Feldes
            id_field: Der Name des ID-Feldes (Standard: "id")
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            file_path = self._get_file_path(id_value)
            
            if not file_path.exists():
                return False
            
            os.remove(file_path)
            return True
        
        except Exception as e:
            print(f"Fehler beim Löschen der Daten: {e}")
            return False
    
    def list_all(self) -> List[T]:
        """
        Gibt alle Datensätze zurück.
        
        Returns:
            Liste aller Datensätze
        """
        try:
            result = []
            
            for file_path in self.data_dir.glob("*.json"):
                id_value = file_path.stem
                data = self.load(id_value)
                
                if data is not None:
                    result.append(data)
            
            return result
        
        except Exception as e:
            print(f"Fehler beim Auflisten der Daten: {e}")
            return []
    
    def exists(self, id_value: str, id_field: str = "id") -> bool:
        """
        Prüft, ob eine JSON-Datei existiert.
        
        Args:
            id_value: Der Wert des ID-Feldes
            id_field: Der Name des ID-Feldes (Standard: "id")
            
        Returns:
            bool: True, wenn die Datei existiert, sonst False
        """
        file_path = self._get_file_path(id_value)
        return file_path.exists()