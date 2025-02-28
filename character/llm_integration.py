# character/llm_integration.py
from character.interfaces import Trademark, Edge, Flaw, Drive, Item
from ai.llm_interface import LLMInterface
from typing import Dict, List, Any, Optional
import json

class CharacterLLMIntegration:
    """Integration von LLM-Funktionalitäten für die Charaktererstellung."""
    
    def __init__(self, llm_interface: LLMInterface):
        """
        Initialisiert die LLM-Integration.
        
        Args:
            llm_interface: Instanz des LLM-Interfaces
        """
        self.llm = llm_interface
    
    def suggest_trademarks_from_background(self, background_story: str, count: int = 5) -> List[Dict[str, Any]]:
        """
        Schlägt Trademarks basierend auf der Hintergrundgeschichte vor.
        
        Args:
            background_story: Hintergrundgeschichte des Charakters
            count: Anzahl der Vorschläge
        
        Returns:
            Liste von Trademark-Dictionaries
        """
        prompt = f"""
        Du bist ein Assistent für die Charaktererstellung in einem Cyberpunk-Rollenspiel.
        
        Basierend auf der folgenden Hintergrundgeschichte, schlage {count} passende "Trademarks" vor.
        Ein Trademark definiert die Vergangenheit, den Beruf, die einzigartigen Talente oder die spezielle Ausrüstung des Charakters.
        
        Hintergrundgeschichte:
        {background_story}
        
        Für jedes Trademark gib an:
        1. Einen Namen
        2. Eine Liste von 8-10 "Triggers" (Fähigkeiten, Kenntnisse oder Eigenschaften)
        3. Eine kurze Beschreibung
        4. Vorschläge für 2-3 mögliche "Flaws" (Nachteile)
        
        Beispiel für ein Trademark:
        {{
            "name": "Codeslinger",
            "triggers": ["Hacking", "Cyber combat", "Security systems", "Computers", "Ghost chip", "Sense motives", "Notice", "Repair"],
            "description": "Ein Hacker, der sich im digitalen Raum besser zurechtfindet als in der realen Welt.",
            "flaws": ["Traceable", "Unfit", "Socially awkward"]
        }}
        
        Antworte im JSON-Format mit einer Liste von Trademark-Objekten.
        """
        
        try:
            response = self.llm.client.models.generate_content(
                model=self.llm.model,
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            
            # Parsed JSON aus der Antwort extrahieren
            result = response.parsed
            
            # Sicherstellen, dass das Ergebnis eine Liste ist
            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and "trademarks" in result:
                return result["trademarks"]
            else:
                return []
                
        except Exception as e:
            print(f"Fehler bei der LLM-Anfrage: {e}")
            return []
    
    def suggest_edges_for_trademark(self, trademark: Dict[str, Any], count: int = 3) -> List[str]:
        """
        Schlägt Edges für ein Trademark vor.
        
        Args:
            trademark: Trademark-Dictionary
            count: Anzahl der Vorschläge
        
        Returns:
            Liste von Edge-Namen
        """
        # Verwende einfach die vorhandenen Trigger als Edges
        triggers = trademark.get("triggers", [])
        
        if len(triggers) <= count:
            return triggers
        
        # Ansonsten LLM verwenden, um die besten auszuwählen
        prompt = f"""
        Du bist ein Assistent für die Charaktererstellung in einem Cyberpunk-Rollenspiel.
        
        Für das Trademark "{trademark.get('name')}" mit der Beschreibung "{trademark.get('description')}" 
        und folgenden potenziellen "Triggers" (Fähigkeiten):
        
        {', '.join(triggers)}
        
        Wähle die {count} am besten geeigneten Edges (spezifische Vorteile) aus diesen Triggers aus.
        Berücksichtige dabei, welche am relevantesten für ein Cyberpunk-Setting sind und dem Charakter die größten Vorteile bieten würden.
        
        Antworte im JSON-Format mit einer Liste von Strings, die die ausgewählten Edges enthalten.
        """
        
        try:
            response = self.llm.client.models.generate_content(
                model=self.llm.model,
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            
            # Parsed JSON aus der Antwort extrahieren
            result = response.parsed
            
            # Sicherstellen, dass das Ergebnis eine Liste ist
            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and "edges" in result:
                return result["edges"]
            else:
                return triggers[:count]  # Fallback: Nimm die ersten count Trigger
                
        except Exception as e:
            print(f"Fehler bei der LLM-Anfrage: {e}")
            return triggers[:count]  # Fallback: Nimm die ersten count Trigger
    
    def suggest_flaws_for_character(self, character_data: Dict[str, Any], count: int = 5) -> List[Dict[str, Any]]:
        """
        Schlägt Flaws basierend auf den Charakterdaten vor.
        
        Args:
            character_data: Charakterdaten
            count: Anzahl der Vorschläge
        
        Returns:
            Liste von Flaw-Dictionaries
        """
        trademarks = character_data.get("trademarks", {})
        trademark_names = list(trademarks.keys())
        
        prompt = f"""
        Du bist ein Assistent für die Charaktererstellung in einem Cyberpunk-Rollenspiel.
        
        Für einen Charakter mit den folgenden Trademarks:
        {', '.join(trademark_names)}
        
        Schlage {count} passende "Flaws" (Nachteile) vor. Ein Flaw ist ein Nachteil, Problem oder eine Schwierigkeit, 
        mit der der Charakter zu kämpfen hat. Flaws sollten interessant sein und Rollenspiel-Möglichkeiten bieten.
        
        Für jeden Flaw gib an:
        1. Einen Namen
        2. Eine kurze Beschreibung
        
        Beispiel für einen Flaw:
        {{
            "name": "Trust no-one",
            "description": "Du bist äußerst misstrauisch und hast Schwierigkeiten, anderen zu vertrauen, selbst wenn sie dir helfen wollen."
        }}
        
        Antworte im JSON-Format mit einer Liste von Flaw-Objekten.
        """
        
        try:
            response = self.llm.client.models.generate_content(
                model=self.llm.model,
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            
            # Parsed JSON aus der Antwort extrahieren
            result = response.parsed
            
            # Sicherstellen, dass das Ergebnis eine Liste ist
            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and "flaws" in result:
                return result["flaws"]
            else:
                return []
                
        except Exception as e:
            print(f"Fehler bei der LLM-Anfrage: {e}")
            return []
    
    def suggest_drives_for_character(self, character_data: Dict[str, Any], count: int = 3) -> List[str]:
        """
        Schlägt Drives basierend auf den Charakterdaten vor.
        
        Args:
            character_data: Charakterdaten
            count: Anzahl der Vorschläge
        
        Returns:
            Liste von Drive-Beschreibungen
        """
        trademarks = character_data.get("trademarks", {})
        trademark_names = list(trademarks.keys())
        
        flaws = character_data.get("flaws", [])
        flaw_names = [flaw.get("name", "") for flaw in flaws]
        
        prompt = f"""
        Du bist ein Assistent für die Charaktererstellung in einem Cyberpunk-Rollenspiel.
        
        Für einen Charakter mit den folgenden Trademarks:
        {', '.join(trademark_names)}
        
        Und den folgenden Flaws:
        {', '.join(flaw_names)}
        
        Schlage {count} passende "Drives" (Motivationen) vor. Ein Drive ist das, was den Charakter antreibt, 
        gefährliche Jobs anzunehmen. Es ist ein tiefes Verlangen oder ein wichtiges persönliches Ziel.
        
        Jeder Drive sollte spezifisch, greifbar und im Cyberpunk-Setting verankert sein. Beispiele könnten sein:
        - "Expose Yen Group's crimes"
        - "Find my sister's killer"
        - "Remove my cortex bomb"
        
        Antworte im JSON-Format mit einer Liste von Strings, die die Drive-Beschreibungen enthalten.
        """
        
        try:
            response = self.llm.client.models.generate_content(
                model=self.llm.model,
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            
            # Parsed JSON aus der Antwort extrahieren
            result = response.parsed
            
            # Sicherstellen, dass das Ergebnis eine Liste ist
            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and "drives" in result:
                return result["drives"]
            else:
                return []
                
        except Exception as e:
            print(f"Fehler bei der LLM-Anfrage: {e}")
            return []
    
    def suggest_gear_for_character(self, character_data: Dict[str, Any], count: int = 4) -> List[Dict[str, Any]]:
        """
        Schlägt Ausrüstung basierend auf den Charakterdaten vor.
        
        Args:
            character_data: Charakterdaten
            count: Anzahl der Vorschläge
        
        Returns:
            Liste von Gear-Dictionaries
        """
        trademarks = character_data.get("trademarks", {})
        trademark_names = list(trademarks.keys())
        
        prompt = f"""
        Du bist ein Assistent für die Charaktererstellung in einem Cyberpunk-Rollenspiel.
        
        Für einen Charakter mit den folgenden Trademarks:
        {', '.join(trademark_names)}
        
        Schlage {count} passende Ausrüstungsgegenstände vor. Jeder Gegenstand kann spezielle Tags haben, 
        die seine Eigenschaften beschreiben. Je mehr Tags ein Gegenstand hat, desto schwieriger ist es, 
        ihn zu erhalten (Würfelwurf erforderlich).
        
        Für jeden Gegenstand gib an:
        1. Einen Namen
        2. Eine Liste von 1-4 Tags
        3. Eine kurze Beschreibung
        
        Beispiele für Kategorien:
        - Ranged Weapons (Accurate, Area of effect, Armor piercing, Silenced, ...)
        - Melee Weapons (Sharp, Concealable, Quick, Deadly, ...)
        - Armor (Bullet proof, Stun resistance, Concealed, Light weight, ...)
        - Vehicles (Fast, Agile, Armored, Fly, ...)
        - Tools (Portable, Well-stocked, Advanced, Concealed, ...)
        - Cyberware (Thermal imaging, Fast, Quick draw, ...)
        
        Beispiel für einen Gegenstand:
        {{
            "name": "Cyber Eyes",
            "tags": ["Thermal imaging", "Camera", "HUD"],
            "description": "Replacement eyes with enhanced capabilities."
        }}
        
        Antworte im JSON-Format mit einer Liste von Gear-Objekten.
        """
        
        try:
            response = self.llm.client.models.generate_content(
                model=self.llm.model,
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            
            # Parsed JSON aus der Antwort extrahieren
            result = response.parsed
            
            # Sicherstellen, dass das Ergebnis eine Liste ist
            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and "gear" in result:
                return result["gear"]
            else:
                return []
                
        except Exception as e:
            print(f"Fehler bei der LLM-Anfrage: {e}")
            return []