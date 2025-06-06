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
from cyberstory.ai.schemas import Scene  # oder welches Modell auch immer benötigt wird


class LLMGameplayIntegration:
    """Integration von LLM-Funktionalitäten für das Gameplay."""
    
    def debug_scene_generation(self) -> Dict[str, Any]:
        """
        Testet die Szenengenerierung mit minimalen Testdaten.
        Diese Methode ist nur für Debug-Zwecke gedacht.
        
        Returns:
            Dict mit den Szenendaten oder Fallback-Szene bei Fehler
        """
        print("\n=== DEBUG SZENENGENERIERUNG ===")
        
        # Minimale Testdaten
        test_character = {
            "id": "test-char",
            "name": "Test Charakter",
            "faction": "Anarchisten",
            "trademarks": {
                "Codeslinger": {
                    "name": "Codeslinger",
                    "triggers": ["Hacking", "Cyber combat", "Security systems"]
                }
            },
            "edges": [
                {"name": "Hacking", "trademark": "Codeslinger"}
            ],
            "flaws": [
                {"name": "Wanted", "description": "Auf der Fahndungsliste von Corp Sec"}
            ],
            "drive": {
                "description": "Befreie dich von der Kontrolle der Megacorps",
                "track": [False] * 10
            }
        }
        
        test_game_state = {
            "id": "test-game",
            "active_character_id": "test-char",
            "current_scene": {},
            "quest_data": {},
            "world_state": {},
            "history": []
        }
        
        # Versuche, eine Szene zu generieren
        try:
            print("Starte Szenengenerierung mit Testdaten...")
            scene = self.generate_scene(test_game_state, test_character)
            print(f"Szenengenerierung abgeschlossen: {scene.get('name', 'Keine Szene generiert')}")
            print("=== DEBUG ENDE ===\n")
            return scene
        except Exception as e:
            print(f"!!! FEHLER BEI DER SZENENGENERIERUNG: {e} !!!")
            import traceback
            traceback.print_exc()
            print("=== DEBUG ENDE MIT FEHLER ===\n")
            return self._create_fallback_scene()
    
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
            check_result: Ergebnis der Würfelprobe als Dict
            action_text: Text der Spieleraktion
            
        Returns:
            Dict mit Konsequenzen, Updates für den Spielzustand und Charakteraktualisierungen
        """
        # Extrahiere relevante Daten für den Prompt
        current_scene = game_state.get("current_scene", {})
        
        # Extrahiere die Werte aus check_result - unabhängig davon, ob es ein Dict oder ein DiceResult-Objekt ist
        result = check_result["result"]
        
        # Hier verwenden wir die Werte direkt aus dem result-Objekt
        success_level = result.success_level if hasattr(result, 'success_level') else "failure"
        value = result.value if hasattr(result, 'value') else 0
        boons = result.boons if hasattr(result, 'boons') else 0
        
        # Konvertiere das result-Objekt in ein Dict, wenn es noch keins ist
        result_dict = result.to_dict() if hasattr(result, 'to_dict') else result
        
        # Erstelle einen sicheren Dict für die JSON-Serialisierung
        check_result_dict = {
            "result": result_dict,
            "pool_details": check_result["pool_details"]
        }
        
        # Erstelle den Prompt
        prompt = CONSEQUENCES_PROMPT.format(
            character_data=json.dumps(character_data, ensure_ascii=False),
            game_state=json.dumps(game_state, ensure_ascii=False),
            current_scene=json.dumps(current_scene, ensure_ascii=False),
            action_text=action_text,
            check_result=json.dumps(check_result_dict, ensure_ascii=False),
            success_level=success_level,
            value=value,
            boons=boons
        )
        
        # Sende den Prompt an das LLM
        response = self._send_to_llm(prompt)
        
        # Fallback-Konsequenzen, falls etwas schiefgeht
        if not response:
            return self._create_fallback_consequences(success_level)
        
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
    
    def _send_to_llm(self, prompt: str, schema_model=None) -> Optional[Dict[str, Any]]:
        try:
            print("\n=== LLM-ANFRAGE BEGINNT ===")
            print(f"Sende Anfrage an Modell: {self.llm.model}")
            print(f"Prompt (gekürzt): {prompt[:300]}...\n")
            
            # Debug: Prompt in Datei speichern
            with open("debug_last_prompt.txt", "w", encoding="utf-8") as f:
                f.write(prompt)
                print("Vollständiger Prompt in 'debug_last_prompt.txt' gespeichert.")
            
            # Konfiguration vorbereiten
            config = {'response_mime_type': 'application/json'}
            if schema_model:
                config['response_schema'] = schema_model
            
            # API-Anfrage senden mit JSON-Konfiguration
            response = self.llm.client.models.generate_content(
                model=self.llm.model,
                contents=prompt,
                config=config
            )
            
            # Debug: Rohantwort speichern
            with open("debug_last_response_raw.txt", "w", encoding="utf-8") as f:
                f.write(str(response))
                print("Rohantwort in 'debug_last_response_raw.txt' gespeichert.")
            
            print(f"LLM-Antwort erhalten, Rohtext: {response.text[:300]}...")
            
            # Verwenden von response.parsed statt manuelles Parsing
            if hasattr(response, 'parsed') and response.parsed is not None:
                result = response.parsed
                print(f"Automatisches JSON-Parsing erfolgreich")
                
                # Wenn das Ergebnis ein Pydantic-Modell ist, zu Dict konvertieren
                if hasattr(result, 'dict'):
                    result = result.dict()
                
            else:
                # Fallback auf manuelles JSON-Parsing wenn nötig
                import json
                try:
                    result = json.loads(response.text)
                    print(f"Manuelles JSON-Parsing erfolgreich")
                except json.JSONDecodeError as je:
                    print(f"JSON-Parsing-Fehler: {je}")
                    print(f"Vollständige Antwort: {response.text}")
                    return None
            
            # Debug: Geparste Antwort speichern
            with open("debug_last_response_parsed.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
                print("Geparste Antwort in 'debug_last_response_parsed.json' gespeichert.")
            
            print("=== LLM-ANFRAGE ENDE ===\n")
            return result
            
        except Exception as e:
            print(f"\n!!! FEHLER BEI DER LLM-ANFRAGE: {e} !!!")
            import traceback
            traceback.print_exc()  # Vollständigen Stack-Trace anzeigen
            print("\n=== LLM-ANFRAGE ENDE MIT FEHLER ===\n")
            return None
    
    def _create_fallback_scene(self) -> Dict[str, Any]:
        """Erstellt eine Fallback-Szene für den Fall eines Fehlers."""
        return {
            "name": "Neon-beleuchtete Gasse",
            "description": "Du stehst in einer engen Gasse, gesäumt von flackernden Neonlichtern, die die Pfützen auf dem regennassen Asphalt bunt färben. Die Luft ist erfüllt vom Geruch nach gebratenem Essen, Abgasen und dem metallischen Duft der Stadt. Menschen drängen sich vorbei, jeder in seine eigene Geschichte vertieft. ",
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
    
    def _create_fallback_consequences(self, success_level: str) -> Dict[str, Any]:
        """Erstellt Fallback-Konsequenzen für den Fall eines Fehlers."""
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