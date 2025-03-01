# data/config_handler.py
import json
import os
from pathlib import Path
from typing import Dict, Any


class ConfigHandler:
    """
    Handler für Konfigurationseinstellungen.
    
    Diese Klasse lädt und speichert globale Konfigurationseinstellungen.
    """
    
    def __init__(self, config_file: str = "resources/config.json"):
        """
        Initialisiert den ConfigHandler.
        
        Args:
            config_file: Pfad zur Konfigurationsdatei
        """
        self.config_file = Path(config_file)
        
        # Verzeichnis erstellen, falls es nicht existiert
        os.makedirs(self.config_file.parent, exist_ok=True)
        
        # Standardkonfiguration
        self.config = {
            "api_key": None,
            "model": "gemini-2.0-flash",
            "data_dirs": {
                "characters": "resources/characters",
                "game_states": "resources/game_states",
                "templates": "resources/templates"
            },
            "ui": {
                "terminal_width": 80,
                "animation_speed": 0.01,
                "color_enabled": True
            },
            "game": {
                "max_history_entries": 100,
                "max_stunt_points": 3,
                "max_hits": 3
            }
        }
        
        # Lade die Konfiguration, falls vorhanden
        self.load_config()
    
    def load_config(self) -> bool:
        """
        Lädt die Konfiguration aus der Datei.
        
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._update_nested_dict(self.config, data)
                return True
            
            # Wenn die Datei nicht existiert, erstelle sie mit der Standardkonfiguration
            return self.save_config()
        
        except Exception as e:
            print(f"Fehler beim Laden der Konfiguration: {e}")
            return False
    
    def save_config(self) -> bool:
        """
        Speichert die Konfiguration in der Datei.
        
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            
            return True
        
        except Exception as e:
            print(f"Fehler beim Speichern der Konfiguration: {e}")
            return False
    
    def _update_nested_dict(self, d: Dict, u: Dict) -> Dict:
        """
        Aktualisiert ein verschachteltes Dictionary.
        
        Args:
            d: Das zu aktualisierende Dictionary
            u: Die Aktualisierungen
            
        Returns:
            Das aktualisierte Dictionary
        """
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                d[k] = self._update_nested_dict(d[k], v)
            else:
                d[k] = v
        return d
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Gibt einen Konfigurationswert zurück.
        
        Args:
            key: Der Schlüssel (kann verschachtelt sein, z.B. "ui.terminal_width")
            default: Der Standardwert, falls der Schlüssel nicht existiert
            
        Returns:
            Der Konfigurationswert oder der Standardwert
        """
        try:
            parts = key.split('.')
            value = self.config
            
            for part in parts:
                if part not in value:
                    return default
                value = value[part]
            
            return value
        
        except Exception:
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """
        Setzt einen Konfigurationswert.
        
        Args:
            key: Der Schlüssel (kann verschachtelt sein, z.B. "ui.terminal_width")
            value: Der Wert
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            parts = key.split('.')
            config = self.config
            
            # Navigiere zur richtigen Stelle im Dictionary
            for i in range(len(parts) - 1):
                part = parts[i]
                
                if part not in config:
                    config[part] = {}
                
                config = config[part]
            
            # Setze den Wert
            config[parts[-1]] = value
            
            return self.save_config()
        
        except Exception as e:
            print(f"Fehler beim Setzen des Konfigurationswerts: {e}")
            return False