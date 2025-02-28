# data/interfaces.py
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Type, TypeVar, Generic

T = TypeVar('T')

class DatabaseInterface(Generic[T]):
    """Interface für den Datenbankzugriff."""
    
    @abstractmethod
    def save(self, data: T, id_field: str = "id") -> bool:
        """
        Speichert Daten in der Datenbank.
        
        Args:
            data: Die zu speichernden Daten
            id_field: Der Name des ID-Feldes (Standard: "id")
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        pass
    
    @abstractmethod
    def load(self, id_value: str = None) -> Optional[T]:
        """
        Lädt Daten aus der Datenbank.
        
        Args:
            id_value: Der Wert des ID-Feldes (wenn None, werden alle Daten geladen)
            
        Returns:
            Die geladenen Daten oder None bei Fehler
        """
        pass
    
    @abstractmethod
    def update(self, id_value: str, updates: Dict[str, Any], id_field: str = "id") -> bool:
        """
        Aktualisiert Daten in der Datenbank.
        
        Args:
            id_value: Der Wert des ID-Feldes
            updates: Die zu aktualisierenden Felder und ihre neuen Werte
            id_field: Der Name des ID-Feldes (Standard: "id")
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        pass
    
    @abstractmethod
    def delete(self, id_value: str, id_field: str = "id") -> bool:
        """
        Löscht Daten aus der Datenbank.
        
        Args:
            id_value: Der Wert des ID-Feldes
            id_field: Der Name des ID-Feldes (Standard: "id")
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        pass
    
    @abstractmethod
    def list_all(self) -> List[T]:
        """
        Gibt alle Datensätze zurück.
        
        Returns:
            Liste aller Datensätze
        """
        pass
    
    @abstractmethod
    def exists(self, id_value: str, id_field: str = "id") -> bool:
        """
        Prüft, ob ein Datensatz existiert.
        
        Args:
            id_value: Der Wert des ID-Feldes
            id_field: Der Name des ID-Feldes (Standard: "id")
            
        Returns:
            bool: True, wenn der Datensatz existiert, sonst False
        """
        pass