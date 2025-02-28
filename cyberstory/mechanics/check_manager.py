# mechanics/check_manager.py
import time
import uuid
from typing import Dict, Any, List

from cyberstory import DiceSystemInterface, ModifierManager, JSONDatabase


class CheckResult:
    """Repräsentiert das Ergebnis einer Würfelprobe mit zusätzlichen Metadaten."""
    
    def __init__(self, 
                 id: str = None,
                 timestamp: float = None,
                 character_id: str = None,
                 context: Dict[str, Any] = None,
                 dice_result: Dict[str, Any] = None,
                 consequences: List[str] = None):
        """
        Initialisiert das CheckResult-Objekt.
        
        Args:
            id: ID des Ergebnisses (wird generiert, wenn nicht angegeben)
            timestamp: Zeitstempel des Checks
            character_id: ID des Charakters
            context: Kontext des Checks
            dice_result: Ergebnis der Würfelprobe
            consequences: Konsequenzen des Checks
        """
        self.id = id or str(uuid.uuid4())
        self.timestamp = timestamp or time.time()
        self.character_id = character_id
        self.context = context or {}
        self.dice_result = dice_result or {}
        self.consequences = consequences or []
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Konvertiert das CheckResult in ein Dictionary.
        
        Returns:
            Dictionary-Repräsentation des CheckResults
        """
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "character_id": self.character_id,
            "context": self.context,
            "dice_result": self.dice_result,
            "consequences": self.consequences
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CheckResult':
        """
        Erstellt ein CheckResult aus einem Dictionary.
        
        Args:
            data: Dictionary mit CheckResult-Daten
            
        Returns:
            CheckResult-Objekt
        """
        return cls(
            id=data.get("id"),
            timestamp=data.get("timestamp"),
            character_id=data.get("character_id"),
            context=data.get("context"),
            dice_result=data.get("dice_result"),
            consequences=data.get("consequences")
        )


class CheckManager:
    """Verwaltet die Durchführung von Würfelproben mit Persistenz."""
    
    def __init__(self, dice_system: DiceSystemInterface, data_dir: str = "data/checks"):
        """
        Initialisiert den Check-Manager.
        
        Args:
            dice_system: Das zu verwendende Würfelsystem
            data_dir: Verzeichnis für die Check-Ergebnisse
        """
        self.dice_system = dice_system
        self.modifier_manager = ModifierManager()
        self.db = JSONDatabase(data_dir, CheckResult)
    
    def perform_check(self, 
                     character_data: Dict[str, Any], 
                     check_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Führt eine Würfelprobe durch und speichert das Ergebnis.
        
        Args:
            character_data: Daten des Charakters
            check_context: Kontext des Checks
            
        Returns:
            Dict mit result (DiceResult) und pool_details
        """
        # Würfelpool berechnen
        pool_details = self.modifier_manager.calculate_pool(character_data, check_context)
        action_dice = pool_details["action_dice"]
        danger_dice = pool_details["danger_dice"]
        
        # Würfelprobe durchführen
        result = self.dice_system.perform_check(action_dice, danger_dice)
        
        # Ergebnis speichern
        check_result = CheckResult(
            character_id=character_data.get("id"),
            context=check_context,
            dice_result=result.to_dict()
        )
        self.db.save(check_result.to_dict())
        
        return {
            "result": result,
            "pool_details": pool_details,
            "check_id": check_result.id
        }
    
    def get_check_history(self, character_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Gibt die letzten Checks eines Charakters zurück.
        
        Args:
            character_id: ID des Charakters
            limit: Maximale Anzahl der zurückzugebenden Checks
        
        Returns:
            Liste der letzten Checks
        """
        # Hier müssten wir eigentlich alle Checks laden und filtern, 
        # aber für eine einfache Implementierung reicht das:
        all_checks = self.db.list_all()
        
        character_checks = [
            check.to_dict() for check in all_checks 
            if check.character_id == character_id
        ]
        
        # Sortieren nach Zeitstempel (neueste zuerst)
        character_checks.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        
        return character_checks[:limit]
    
    def add_consequence_to_check(self, check_id: str, consequence: str) -> bool:
        """
        Fügt einem Check eine Konsequenz hinzu.
        
        Args:
            check_id: ID des Checks
            consequence: Die hinzuzufügende Konsequenz
        
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        check_data = self.db.load(check_id)
        
        if check_data is None:
            return False
        
        check_data.consequences.append(consequence)
        return self.db.save(check_data.to_dict())
    
    def get_check_description(self, pool_details: Dict[str, Any]) -> str:
        """
        Erzeugt eine Beschreibung des Würfelpools.
        
        Args:
            pool_details: Die Würfelpool-Details
            
        Returns:
            Formatierte Beschreibung des Würfelpools
        """
        # Implementierung wie zuvor
        description = f"Würfelpool: {pool_details['action_dice']} Action Dice vs. {pool_details['danger_dice']} Danger Dice\n"
        
        if pool_details["applied_modifiers"]:
            description += "Angewendete Modifikatoren:\n"
            for modifier in pool_details["applied_modifiers"]:
                description += f"- {modifier}\n"
        
        return description