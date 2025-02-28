# data/game_state.py
from data.json_database import JSONDatabase
from typing import Dict, List, Any, Optional
import uuid
import os
from pathlib import Path
import json

class GameState:
    """
    Klasse zur Verwaltung des Spielzustands.
    
    Diese Klasse speichert und lädt den aktuellen Spielzustand, einschließlich
    des aktiven Charakters, der aktuellen Szene, der Questinformationen usw.
    """
    
    def __init__(self, 
                 id: str = None, 
                 active_character_id: str = None,
                 current_scene: Dict[str, Any] = None,
                 quest_data: Dict[str, Any] = None,
                 world_state: Dict[str, Any] = None,
                 history: List[str] = None):
        """
        Initialisiert den Spielzustand.
        
        Args:
            id: ID des Spielzustands (wird generiert, wenn nicht angegeben)
            active_character_id: ID des aktiven Charakters
            current_scene: Daten der aktuellen Szene
            quest_data: Daten der aktuellen Quest
            world_state: Zustand der Spielwelt
            history: Verlauf der Spielereignisse
        """
        self.id = id or str(uuid.uuid4())
        self.active_character_id = active_character_id
        self.current_scene = current_scene or {}
        self.quest_data = quest_data or {}
        self.world_state = world_state or {}
        self.history = history or []
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Konvertiert den Spielzustand in ein Dictionary.
        
        Returns:
            Dictionary-Repräsentation des Spielzustands
        """
        return {
            "id": self.id,
            "active_character_id": self.active_character_id,
            "current_scene": self.current_scene,
            "quest_data": self.quest_data,
            "world_state": self.world_state,
            "history": self.history
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameState':
        """
        Erstellt einen Spielzustand aus einem Dictionary.
        
        Args:
            data: Dictionary mit Spielzustandsdaten
            
        Returns:
            GameState-Objekt
        """
        return cls(
            id=data.get("id"),
            active_character_id=data.get("active_character_id"),
            current_scene=data.get("current_scene"),
            quest_data=data.get("quest_data"),
            world_state=data.get("world_state"),
            history=data.get("history")
        )
    
    def add_to_history(self, event: str) -> None:
        """
        Fügt ein Ereignis zum Spielverlauf hinzu.
        
        Args:
            event: Das hinzuzufügende Ereignis
        """
        self.history.append(event)
        
        # Beschränke die Historie auf eine maximale Anzahl von Einträgen (z.B. 100)
        max_history_entries = 100
        if len(self.history) > max_history_entries:
            self.history = self.history[-max_history_entries:]


class GameStateManager:
    """
    Manager für den Spielzustand.
    
    Diese Klasse bietet Methoden zum Speichern, Laden und Verwalten des Spielzustands.
    """
    
    def __init__(self, data_dir: str = "data/game_states"):
        """
        Initialisiert den GameStateManager.
        
        Args:
            data_dir: Verzeichnis für die Spielstandsdaten
        """
        self.db = JSONDatabase(data_dir, GameState)
        self.active_game_state = None
    
    def new_game(self, character_id: str) -> GameState:
        """
        Erstellt ein neues Spiel.
        
        Args:
            character_id: ID des Charakters
            
        Returns:
            GameState-Objekt
        """
        game_state = GameState(active_character_id=character_id)
        self.active_game_state = game_state
        self.save_game()
        
        return game_state
    
    def save_game(self) -> bool:
        """
        Speichert den aktuellen Spielzustand.
        
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        if self.active_game_state is None:
            return False
        
        return self.db.save(self.active_game_state)
    
    def save_game_as(self, name: str) -> bool:
        """
        Speichert den aktuellen Spielzustand unter einem neuen Namen.
        
        Args:
            name: Der neue Name
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        if self.active_game_state is None:
            return False
        
        # Erstelle eine Kopie des aktuellen Spielzustands
        game_state_dict = self.active_game_state.to_dict()
        game_state_dict["id"] = name
        
        new_game_state = GameState.from_dict(game_state_dict)
        return self.db.save(new_game_state)
    
    def load_game(self, id_value: str) -> Optional[GameState]:
        """
        Lädt einen Spielzustand.
        
        Args:
            id_value: ID des Spielzustands
            
        Returns:
            GameState-Objekt oder None bei Fehler
        """
        game_state = self.db.load(id_value)
        
        if game_state is not None:
            self.active_game_state = game_state
        
        return game_state
    
    def get_saved_games(self) -> List[Dict[str, Any]]:
        """
        Gibt eine Liste aller gespeicherten Spiele zurück.
        
        Returns:
            Liste von Spielstandsdaten
        """
        game_states = self.db.list_all()
        
        # Erzeuge eine vereinfachte Liste mit weniger Daten
        result = []
        for game_state in game_states:
            result.append({
                "id": game_state.id,
                "active_character_id": game_state.active_character_id,
                "last_scene": game_state.current_scene.get("name", "Unbekannt"),
                "history_length": len(game_state.history)
            })
        
        return result
    
    def delete_game(self, id_value: str) -> bool:
        """
        Löscht einen Spielzustand.
        
        Args:
            id_value: ID des Spielzustands
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        # Wenn der aktive Spielzustand gelöscht wird, setze ihn zurück
        if self.active_game_state is not None and self.active_game_state.id == id_value:
            self.active_game_state = None
        
        return self.db.delete(id_value)
    
    def update_active_game(self, updates: Dict[str, Any]) -> bool:
        """
        Aktualisiert den aktiven Spielzustand.
        
        Args:
            updates: Die zu aktualisierenden Felder und ihre neuen Werte
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        if self.active_game_state is None:
            return False
        
        for key, value in updates.items():
            setattr(self.active_game_state, key, value)
        
        return self.save_game()
    
    def add_event_to_history(self, event: str) -> bool:
        """
        Fügt ein Ereignis zum Spielverlauf hinzu.
        
        Args:
            event: Das hinzuzufügende Ereignis
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        if self.active_game_state is None:
            return False
        
        self.active_game_state.add_to_history(event)
        return self.save_game()