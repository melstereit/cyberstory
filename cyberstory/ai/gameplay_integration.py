# cyberstory/ai/gameplay_integration.py
import json
from typing import Dict, Any, List, Optional

from cyberstory.ai.llm_interface import LLMInterface
from cyberstory.ai.prompt_templates import (
    SCENE_GENERATION_PROMPT,
    ACTION_PROCESSING_PROMPT,
    CONSEQUENCES_PROMPT,
    QUEST_GENERATION_PROMPT
)


class LLMGameplayIntegration:
    """Integration von LLM-Funktionalitäten für das Gameplay."""
    
    def __init__(self, llm_interface: LLMInterface):
        """
        Initialisiert die LLM-Integration für das Gameplay.
        
        Args:
            llm_interface: Instanz des LLM-Interfaces
        """
        self.llm = llm_interface
    
    def generate_scene(self, game_state: Dict[str, Any], character_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generiert eine neue Szene basierend auf dem Spielzustand.
        
        Args:
            game_state: Aktueller Spielzustand
            character_data: Aktuelle Charakterdaten
            
        Returns:
            Dict mit den Szenendaten
        """
        # Extrahiere relevante Daten für den Prompt
        quest_data = game_state.get("quest_data", {})
        
        # Erstelle den Prompt
        prompt = SCENE_GENERATION_PROMPT.format(
            character_data=json.dumps(character_data, ensure_ascii=False),
            game_state=json.dumps(game_state, ensure_ascii=False),
            quest_data=json.dumps(quest_data, ensure_ascii=False)
        )
        
        # Sende den Prompt an das LLM
        response = self._send_to_llm(prompt)
        
        # Fallback-Szene, falls etwas schiefgeht
        if not response:
            return self._create_fallback_scene()
        
        return response
    
    def process_player_action(self, 
                              game_state: Dict[str, Any], 
                              character_data: Dict[str, Any], 
                              action_text: str) -> Dict[str, Any]:
        """
        Verarbeitet eine Spieleraktion.
        
        Args:
            game_state: Aktueller Spielzustand
            character_data: Aktuelle Charakterdaten
            action_text: Text der Spieleraktion
            
        Returns:
            Dict mit Aktion, ob ein Würfelwurf erforderlich ist und Kontext
        """
        # Extrahiere relevante Daten für den Prompt
        current_scene = game_state.get("current_scene", {})
        
        # Erstelle den Prompt
        prompt = ACTION_PROCESSING_PROMPT.format(
            character_data=json.dumps(character_data, ensure_ascii=False),
            game_state=json.dumps(game_state, ensure_ascii=False),
            current_scene=json.dumps(current_scene, ensure_ascii=False),
            action_text=action_text
        )
        
        # Sende den Prompt an das LLM
        response = self._send_to_llm(prompt)
        
        # Fallback-Antwort, falls etwas schiefgeht
        if not response:
            return self._create_fallback_action_response(action_text)
        
        return response
    
    def generate_consequences(self, 
                             game_state: Dict[str, Any], 
                             character_data: Dict[str, Any], 
                             check_result: Dict[str, Any], 
                             action_text: str) -> Dict[str, Any]:
        """
        Generiert Konsequenzen basierend auf einem Würfelergebnis.
        
        Args:
            game_state: Aktueller Spielzustand
            character_data: Aktuelle Charakterdaten
            check_result: Ergebnis der Würfelprobe
            action_text: Text der Spieleraktion
            
        Returns:
            Dict mit Konsequenzen, Updates für den Spielzustand und Charakteraktualisierungen
        """
        # Extrahiere relevante Daten für den Prompt
        current_scene = game_state.get("current_scene", {})
        result = check_result.get("result", {})
        
        # Erstelle den Prompt
        prompt = CONSEQUENCES_PROMPT.format(
            character_data=json.dumps(character_data, ensure_ascii=False),
            game_state=json.dumps(game_state, ensure_ascii=False),
            current_scene=json.dumps(current_scene, ensure_ascii=False),
            action_text=action_text,
            check_result=json.dumps(check_result, ensure_ascii=False),
            success_level=result.success_level if hasattr(result, 'success_level') else "failure",
            value=result.value if hasattr(result, 'value') else 0,
            boons=result.boons if hasattr(result, 'boons') else 0
        )
        
        # Sende den Prompt an das LLM
        response = self._send_to_llm(prompt)
        
        # Fallback-Konsequenzen, falls etwas schiefgeht
        if not response:
            return self._create_fallback_consequences(result)
        
        return response
    
    def generate_quest(self, game_state: Dict[str, Any], character_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generiert eine neue Quest für den Charakter.
        
        Args:
            game_state: Aktueller Spielzustand
            character_data: Aktuelle Charakterdaten
            
        Returns:
            Dict mit den Quest-Daten
        """
        # Erstelle den Prompt
        prompt = QUEST_GENERATION_PROMPT.format(
            character_data=json.dumps(character_data, ensure_ascii=False),
            game_state=json.dumps(game_state, ensure_ascii=False)
        )
        
        # Sende den Prompt an das LLM
        response = self._send_to_llm(prompt)
        
        # Fallback-Quest, falls etwas schiefgeht
        if not response:
            return self._create_fallback_quest()
        
        return response
    
    def _send_to_llm(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Sendet einen Prompt an das LLM und gibt die Antwort zurück.
        
        Args:
            prompt: Der zu sendende Prompt
            
        Returns:
            Die geparste LLM-Antwort oder None bei Fehler
        """
        try:
            response = self.llm.client.models.generate_content(
                model=self.llm.model,
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            
            # Parsed JSON aus der Antwort extrahieren
            return response.parsed
            
        except Exception as e:
            print(f"Fehler bei der LLM-Anfrage: {e}")
            return None
    
    def _create_fallback_scene(self) -> Dict[str, Any]:
        """Erstellt eine Fallback-Szene für den Fall eines Fehlers."""
        return {
            "name": "Neon-beleuchtete Gasse",
            "description": "Du stehst in einer engen Gasse, gesäumt von flackernden Neonlichtern, die die Pfützen auf dem regennassen Asphalt bunt färben. Die Luft ist erfüllt vom Geruch nach gebratenem Essen, Abgasen und dem metallischen Duft der Stadt. Menschen drängen sich vorbei, jeder in seine eigene Geschichte vertieft.",
            "characters": [
                {"name": "Straßenverkäufer", "description": "Ein älterer Mann mit Cyber-Auge, der Syn-Ramen an einem kleinen Stand verkauft.", "faction": "Freelancer"}
            ],
            "objects": [
                {"name": "Öffentliches Terminal", "description": "Ein veraltetes öffentliches Datenterminal, das gelegentlich flackert.", "tags": ["Information", "Grid-Zugang"]}
            ],
            "threats": [],
            "objectives": [
                "Sammle Informationen über deine aktuelle Situation"
            ],
            "suggested_actions": [
                "Sprich mit dem Straßenverkäufer",
                "Nutze das öffentliche Terminal",
                "Erkunde die Umgebung weiter"
            ],
            "completed": False
        }
    
    def _create_fallback_action_response(self, action_text: str) -> Dict[str, Any]:
        """Erstellt eine Fallback-Antwort auf eine Aktion für den Fall eines Fehlers."""
        if "sprechen" in action_text.lower() or "rede" in action_text.lower() or "frag" in action_text.lower():
            return {
                "requires_check": False,
                "response": "Du versuchst, ein Gespräch zu beginnen, aber bekommst nur zögerliche, einsilbige Antworten."
            }
        
        if "untersuchen" in action_text.lower() or "anschauen" in action_text.lower() or "beobachten" in action_text.lower():
            return {
                "requires_check": False,
                "response": "Du untersuchst deine Umgebung genauer, entdeckst aber nichts Besonderes."
            }
        
        if "hacken" in action_text.lower() or "terminal" in action_text.lower() or "computer" in action_text.lower():
            return {
                "requires_check": True,
                "check_context": {
                    "action": "Hacken eines Terminals",
                    "relevant_trademark": "Codeslinger",
                    "relevant_edges": ["Hacking"],
                    "gear_tags": [],
                    "advantageous_tags": [],
                    "disadvantageous_tags": [],
                    "opposition_scale": 0
                }
            }
        
        if "kämpfen" in action_text.lower() or "angreifen" in action_text.lower() or "schlagen" in action_text.lower():
            return {
                "requires_check": True,
                "check_context": {
                    "action": "Kampf",
                    "relevant_trademark": "Enforcer",
                    "relevant_edges": ["Brawl"],
                    "gear_tags": [],
                    "advantageous_tags": [],
                    "disadvantageous_tags": [],
                    "opposition_scale": 1
                }
            }
        
        # Standardantwort
        return {
            "requires_check": False,
            "response": "Du führst die Aktion aus, aber nicht viel passiert. Vielleicht solltest du etwas Spezifischeres versuchen?"
        }
    
    def _create_fallback_consequences(self, result) -> Dict[str, Any]:
        """Erstellt Fallback-Konsequenzen für den Fall eines Fehlers."""
        success_level = result.success_level if hasattr(result, 'success_level') else "failure"
        
        if success_level == "success":
            return {
                "description": "Du hast Erfolg! Die Aktion gelingt wie gewünscht.",
                "game_state_updates": {
                    "history_event": "Erfolgreiche Aktion"
                },
                "character_updates": {}
            }
        
        if success_level == "partial":
            return {
                "description": "Du hast teilweise Erfolg, aber es gibt Komplikationen.",
                "game_state_updates": {
                    "history_event": "Teilweise erfolgreiche Aktion mit Komplikationen"
                },
                "character_updates": {}
            }
        
        if success_level == "failure":
            return {
                "description": "Die Aktion misslingt und führt zu negativen Konsequenzen.",
                "game_state_updates": {
                    "history_event": "Fehlgeschlagene Aktion"
                },
                "character_updates": {
                    "add_condition": "Dazed"
                }
            }
        
        if success_level == "botch":
            return {
                "description": "Die Aktion scheitert katastrophal!",
                "game_state_updates": {
                    "history_event": "Kritisch fehlgeschlagene Aktion"
                },
                "character_updates": {
                    "add_hits": 1
                }
            }
        
        return {
            "description": "Die Aktion hat ein unklares Ergebnis.",
            "game_state_updates": {
                "history_event": "Aktion mit unklarem Ausgang"
            },
            "character_updates": {}
        }
    
    def _create_fallback_quest(self) -> Dict[str, Any]:
        """Erstellt eine Fallback-Quest für den Fall eines Fehlers."""
        return {
            "name": "Daten-Paket",
            "description": "Ein anonymer Client braucht deine Hilfe, um ein wertvolles Datenpaket aus einem gesicherten Megacorp-Terminal zu extrahieren. Die Bezahlung ist gut, die Risiken sind hoch.",
            "client": {
                "name": "Anonymer Fixer",
                "description": "Ein gesichtsloser Kontakt, der nur über verschlüsselte Kanäle kommuniziert.",
                "faction": "Unbekannt"
            },
            "objectives": [
                {
                    "description": "Infiltriere das Megacorp-Gebäude",
                    "completed": False
                },
                {
                    "description": "Extrahiere das Datenpaket",
                    "completed": False
                },
                {
                    "description": "Entkommen ohne entdeckt zu werden",
                    "completed": False
                }
            ],
            "rewards": {
                "credits": 2000,
                "items": [],
                "xp": 3
            },
            "locations": [
                {
                    "name": "Megacorp-Tower",
                    "description": "Ein imposanter Wolkenkratzer mit strenger Sicherheit.",
                    "visited": False
                }
            ],
            "npcs": [
                {
                    "name": "Sicherheitschef",
                    "description": "Ein ehemaliger Militär mit Cyber-Upgrades und strengem Blick.",
                    "faction": "Megacorp",
                    "attitude": "Feindlich"
                }
            ],
            "completed": False
        }