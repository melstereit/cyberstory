# data/session_handler.py
from data.interfaces import DatabaseInterface
from typing import Dict, List, Any, Optional
import json
import os
from pathlib import Path
import time

class SessionHandler:
    """
    Handler für die aktuelle Spielsitzung.
    
    Diese Klasse speichert und lädt Daten für die aktuelle Spielsitzung,
    einschließlich temporärer Daten, die zwischen den Sitzungen verloren gehen können.
    """
    
    def __init__(self, session_file: str = "data/current_session.json"):
        """
        Initialisiert den SessionHandler.
        
        Args:
            session_file: Pfad zur Sitzungsdatei
        """
        self.session_file = Path(session_file)
        
        # Verzeichnis erstellen, falls es nicht existiert
        os.makedirs(self.session_file.parent, exist_ok=True)
        
        # Standardsitzungsdaten
        self.session_data = {
            "active_game_state_id": None,
            "active_character_id": None,
            "ui_settings": {
                "terminal_width": 80,
                "animation_speed": 0.01
            },
            "last_access": time.time()
        }
        
        # Lade die Sitzungsdaten, falls vorhanden
        self.load_session()
    
    def load_session(self) -> bool:
        """
        Lädt die Sitzungsdaten aus der Datei.
        
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.session_data.update(data)
                return True
            
            return False
        
        except Exception as e:
            print(f"Fehler beim Laden der Sitzungsdaten: {e}")
            return False
    
    def save_session(self) -> bool:
        """
        Speichert die Sitzungsdaten in der Datei.
        
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            # Aktualisiere den Zeitstempel des letzten Zugriffs
            self.session_data["last_access"] = time.time()
            
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(self.session_data, f, ensure_ascii=False, indent=2)
            
            return True
        
        except Exception as e:
            print(f"Fehler beim Speichern der Sitzungsdaten: {e}")
            return False
    
    def update_session(self, updates: Dict[str, Any]) -> bool:
        """
        Aktualisiert die Sitzungsdaten.
        
        Args:
            updates: Die zu aktualisierenden Felder und ihre neuen Werte
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            self.session_data.update(updates)
            return self.save_session()
        
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Sitzungsdaten: {e}")
            return False
    
    def get_session_value(self, key: str, default: Any = None) -> Any:
        """
        Gibt einen Wert aus den Sitzungsdaten zurück.
        
        Args:
            key: Der Schlüssel
            default: Der Standardwert, falls der Schlüssel nicht existiert
            
        Returns:
            Der Wert oder der Standardwert
        """
        return self.session_data.get(key, default)
    
    def set_session_value(self, key: str, value: Any) -> bool:
        """
        Setzt einen Wert in den Sitzungsdaten.
        
        Args:
            key: Der Schlüssel
            value: Der Wert
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            self.session_data[key] = value
            return self.save_session()
        
        except Exception as e:
            print(f"Fehler beim Setzen des Sitzungswerts: {e}")
            return False
    
    def clear_session(self) -> bool:
        """
        Löscht die Sitzungsdaten.
        
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            # Zurücksetzen auf Standardwerte, aber UI-Einstellungen beibehalten
            ui_settings = self.session_data.get("ui_settings", {})
            
            self.session_data = {
                "active_game_state_id": None,
                "active_character_id": None,
                "ui_settings": ui_settings,
                "last_access": time.time()
            }
            
            return self.save_session()
        
        except Exception as e:
            print(f"Fehler beim Löschen der Sitzungsdaten: {e}")
            return False