# Konkrete Implementierung der Gemini API für das Cyberpunk RPG

Basierend auf der bereitgestellten API-Dokumentation (README) möchte ich konkrete Vorschläge für die API-Integration in unserem Terminal-basierten Cyberpunk RPG machen. Wir werden die neuere `google-genai` Bibliothek verwenden, die besser für Gemini 2.0+ geeignet ist.

## 1. LLM-Interface Implementierung

### 1.1. Installation und Grundeinrichtung

```python
# ai/llm_interface.py
from google import genai
from pydantic import BaseModel
import os
from typing import Dict, List, Any, Optional

class LLMInterface:
    def __init__(self, api_key=None):
        """Initialisiert die Verbindung zur Gemini API."""
        # API-Schlüssel aus Umgebungsvariable oder Parameter
        api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("API-Schlüssel muss entweder als Parameter übergeben oder als GOOGLE_API_KEY Umgebungsvariable gesetzt werden")
        
        # Client für API-Zugriff initialisieren
        self.client = genai.Client(api_key=api_key)
        
        # Standard-Modell einstellen (kann überschrieben werden)
        self.model = "gemini-2.0-flash"
        
        # Chat-Session für kontextuelle Interaktionen
        self.chat = None
```

### 1.2. Response-Schema mit Pydantic für strukturierte Antworten

```python
# ai/schemas.py
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional, Union

class SceneDescription(BaseModel):
    description: str = Field(..., description="Atmosphärische Beschreibung der Szene")
    npcs: List[Dict[str, str]] = Field(default_factory=list, description="Anwesende NPCs mit Namen und kurzer Beschreibung")
    objects: List[str] = Field(default_factory=list, description="Wichtige Objekte in der Szene")
    exits: List[str] = Field(default_factory=list, description="Mögliche Ausgänge")
    
class ActionResponse(BaseModel):
    description: str = Field(..., description="Beschreibung des Ergebnisses der Aktion")
    requires_check: bool = Field(default=False, description="Ob die Aktion einen Würfelwurf erfordert")
    check_details: Optional[Dict[str, Any]] = Field(default=None, description="Details zum durchzuführenden Check")
    consequences: List[str] = Field(default_factory=list, description="Mögliche Konsequenzen der Aktion")
    scene_changes: Dict[str, Any] = Field(default_factory=dict, description="Änderungen an der aktuellen Szene")

class GameState(BaseModel):
    response: str = Field(..., description="Antwort des Spielleiters")
    data_update: Dict[str, Any] = Field(default_factory=dict, description="Änderungen am Spielzustand")
    history_update: Optional[str] = Field(None, description="Zusammenfassung für langfristigen Kontext")
```

### 1.3. Methoden für verschiedene Spielphasen

```python
# ai/llm_interface.py (Fortsetzung)

def create_character_suggestions(self, background_story: str) -> Dict[str, List[str]]:
    """Generiert Vorschläge für Trademarks, Edges und Flaws basierend auf der Hintergrundgeschichte."""
    prompt = f"""
    Basierend auf folgender Hintergrundgeschichte eines Charakters in einem Cyberpunk-Setting:
    
    "{background_story}"
    
    Generiere passende Vorschläge für:
    1. Trademarks (besondere Fähigkeiten, Hintergründe oder Ausrüstung)
    2. Edges (spezifische Vorteile)
    3. Flaws (Nachteile oder Probleme)
    
    Antworte im JSON-Format.
    """
    
    response = self.client.models.generate_content(
        model=self.model,
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    
    return response.parsed

def generate_scene(self, current_quest: str, character_data: Dict, history: str) -> SceneDescription:
    """Generiert eine neue Szene basierend auf der aktuellen Quest und Spielgeschichte."""
    
    prompt = f"""
    Du bist der Spielleiter eines Cyberpunk-RPGs. Generiere eine neue Szene basierend auf:
    
    Aktuelle Quest: {current_quest}
    Bisherige Handlung: {history}
    Charakterdaten: {character_data}
    
    Erzeuge eine lebendige, atmosphärische Beschreibung mit den folgenden Elementen:
    1. Visuelle und sensorische Details der Umgebung
    2. Anwesende NPCs und ihre Haltung
    3. Wichtige Objekte und Details
    4. Mögliche Interaktionen und Gefahren
    
    Antworte im strukturierten JSON-Format mit den Feldern: description, npcs, objects, exits
    """
    
    response = self.client.models.generate_content(
        model=self.model,
        contents=prompt,
        config={"response_mime_type": "application/json", "response_schema": SceneDescription}
    )
    
    return response.parsed

def interpret_action(self, user_action: str, current_scene: Dict, character_data: Dict) -> ActionResponse:
    """Interpretiert eine Spieleraktion und generiert eine Antwort."""
    
    prompt = f"""
    Der Spieler versucht folgende Aktion: "{user_action}"
    
    Aktueller Kontext:
    {current_scene}
    
    Charakterdaten:
    {character_data}
    
    Interpretiere diese Aktion und generiere eine Antwort mit:
    1. Beschreibung des Ergebnisses
    2. Ob eine Würfelprobe erforderlich ist (Boolean)
    3. Details zur Würfelprobe (wenn erforderlich)
    4. Mögliche Konsequenzen
    5. Änderungen an der Szene
    
    Antworte im strukturierten JSON-Format.
    """
    
    response = self.client.models.generate_content(
        model=self.model,
        contents=prompt,
        config={"response_mime_type": "application/json", "response_schema": ActionResponse}
    )
    
    return response.parsed
```

### 1.4. Chat-basierte Spielleiterinteraktion

```python
# ai/llm_interface.py (Fortsetzung)

def initialize_game_master(self):
    """Initialisiert eine Chat-Session mit dem Spielleiter-System-Prompt."""
    
    system_instruction = """
    Du bist der Spielleiter eines textbasierten Cyberpunk-RPGs im Stil von Neon City Overdrive. 
    Deine Aufgabe ist es, eine lebendige, interaktive Welt zu erschaffen, in der der Spieler 
    Entscheidungen trifft, die die Geschichte beeinflussen.
    
    Als Spielleiter sollst du:
    1. Atmosphärische Beschreibungen liefern
    2. NPCs glaubwürdig darstellen
    3. Konsequenzen von Spieleraktionen interpretieren
    4. Situationen dramatisch und spannend gestalten
    5. Das Cyberpunk-Setting konsistent umsetzen
    
    Das Spiel folgt den Neon City Overdrive Regeln mit Würfelwürfen und Trademarks.
    
    Halte deine Antworten strukturiert im vereinbarten JSON-Format und achte auf konsistente
    Aktualisierung des Spielzustands.
    """
    
    self.chat = self.client.chats.create(
        model=self.model,
        config={"system_instruction": system_instruction}
    )
    
    return self.chat

def get_game_master_response(self, user_input: str, current_state: Dict) -> GameState:
    """Sendet Spielereingabe an die Chat-Session und erhält strukturierte Antwort."""
    
    if not self.chat:
        self.initialize_game_master()
    
    # Kontext hinzufügen
    message = f"""
    Spielereingabe: {user_input}
    
    Aktueller Spielzustand:
    {current_state}
    
    Antworte im vereinbarten JSON-Format mit:
    1. 'response': Deine Antwort als Spielleiter
    2. 'data_update': Notwendige Änderungen am Spielzustand
    3. 'history_update': Zusammenfassung für den Verlauf (optional)
    """
    
    response = self.chat.send_message(
        message=message,
        config={"response_mime_type": "application/json", "response_schema": GameState}
    )
    
    return response.parsed
```

### 1.5. Stream für progressives Rendern von Beschreibungen

```python
# ai/llm_interface.py (Fortsetzung)

def stream_narrative_description(self, prompt: str, callback=None):
    """Streamt eine narrative Beschreibung für progressives Anzeigen im Terminal."""
    
    for chunk in self.client.models.generate_content_stream(
        model=self.model,
        contents=prompt
    ):
        if callback:
            callback(chunk.text)
        else:
            yield chunk.text
```

## 2. Function Calling für Spielmechanik

```python
# ai/game_mechanics.py

def perform_dice_check(trademark: str, edges: List[str], 
                     tags: List[str], conditions: List[str], 
                     trauma_count: int, opposition_scale: int = 0):
    """Führt einen Würfelwurf basierend auf den Spielmechaniken durch."""
    # Implementierung der Würfelmechanik
    pass

def determine_consequences(result: int, context: Dict):
    """Bestimmt die Konsequenzen eines Würfelwurfs basierend auf dem Kontext."""
    # Implementierung der Konsequenzbestimmung
    pass

# ai/llm_interface.py (Fortsetzung)

def resolve_action_with_mechanics(self, action_response: ActionResponse, character_data: Dict) -> Dict:
    """Verarbeitet eine Aktion mit Spielmechanik-Integration über Function Calling."""
    
    if not action_response.requires_check:
        return {"success": True, "description": action_response.description, 
                "consequences": action_response.consequences}
    
    # Function Calling für Würfelwürfe
    prompt = f"""
    Führe einen Würfelwurf basierend auf den folgenden Informationen durch:
    
    Check-Details: {action_response.check_details}
    Charakterdaten: {character_data}
    
    Bestimme das Ergebnis und die entsprechenden Konsequenzen.
    """
    
    response = self.client.models.generate_content(
        model=self.model,
        contents=prompt,
        config={
            "tools": [perform_dice_check, determine_consequences],
            "response_mime_type": "application/json"
        }
    )
    
    return response.parsed
```

## 3. Integration in das Hauptspiel

```python
# game_engine/game_loop.py

from ai.llm_interface import LLMInterface
from data.json_handler import JSONHandler
from ui.terminal import TerminalUI
import os

class GameLoop:
    def __init__(self):
        # API-Schlüssel aus Umgebungsvariable oder aus config.py laden
        api_key = os.environ.get("GOOGLE_API_KEY")
        
        self.llm = LLMInterface(api_key=api_key)
        self.data = JSONHandler("data/game_data.json")
        self.ui = TerminalUI()
        
        # Spielzustand laden oder initialisieren
        self.game_state = self.data.load() or {"data_update": {}, "history_update": ""}
    
    def start_new_game(self):
        """Startet ein neues Spiel mit Charaktererstellung."""
        self.ui.display_intro()
        
        # Name und Hintergrundgeschichte erfassen
        name = self.ui.get_input("Wie lautet dein Name?")
        background = self.ui.get_input("Erzähle mir etwas über deine Hintergrundgeschichte:")
        
        # KI-generierte Vorschläge für Trademarks, etc.
        suggestions = self.llm.create_character_suggestions(background)
        
        # Charaktererstellung durchführen...
        # ...
        
        # Initialisiere Spielleiter-Chat
        self.llm.initialize_game_master()
        
        # Starte die erste Quest
        self.start_first_quest()
    
    def start_first_quest(self):
        """Startet die erste Quest des Spiels."""
        # Quest-Intro generieren
        quest_intro = self.llm.stream_narrative_description(
            "Generiere eine Einführung für die erste Quest: Ein mysteriöser Auftraggeber kontaktiert den Spieler für einen gefährlichen Hack-Job.",
            callback=self.ui.display_streaming_text
        )
        
        # Erste Szene generieren
        first_scene = self.llm.generate_scene(
            current_quest="Ein mysteriöser Auftraggeber",
            character_data=self.game_state["data_update"],
            history=""
        )
        
        # Anzeigen und in Spielzustand speichern
        self.ui.display_scene(first_scene)
        self.game_state["current_scene"] = first_scene.dict()
        self.data.save(self.game_state)
        
        # Hauptspielschleife starten
        self.main_loop()
    
    def main_loop(self):
        """Hauptspielschleife für die kontinuierliche Interaktion."""
        while True:
            # Spielereingabe holen
            user_input = self.ui.get_input("\nWas möchtest du tun?")
            
            if user_input.lower() in ["beenden", "exit", "quit"]:
                break
            
            # Systembefehle verarbeiten
            if user_input.startswith("/"):
                self.process_system_command(user_input)
                continue
            
            # Normale Aktion verarbeiten
            response = self.llm.get_game_master_response(
                user_input, 
                self.game_state
            )
            
            # Antwort anzeigen
            self.ui.display_text(response.response)
            
            # Spielzustand aktualisieren
            if response.data_update:
                self.game_state["data_update"].update(response.data_update)
            
            if response.history_update:
                self.game_state["history_update"] += "\n" + response.history_update
            
            # Spielstand speichern
            self.data.save(self.game_state)
```

## 4. Unterstützungsfunktionen für JSON-Verarbeitung

```python
# data/json_handler.py

import json
import os
from typing import Dict, Any, Optional

class JSONHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path
        
        # Sicherstellen, dass das Verzeichnis existiert
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    def load(self) -> Optional[Dict[str, Any]]:
        """Lädt den Spielzustand aus der JSON-Datei."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            return None
        except Exception as e:
            print(f"Fehler beim Laden des Spielzustands: {e}")
            return None
    
    def save(self, game_state: Dict[str, Any]) -> bool:
        """Speichert den Spielzustand in der JSON-Datei."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(game_state, file, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Fehler beim Speichern des Spielzustands: {e}")
            return False
```

## 5. Konfiguration und Umgebungsvariablen

```python
# utils/config.py

import os
import dotenv
from pathlib import Path

# .env Datei laden, falls vorhanden
dotenv.load_dotenv()

# Basis-Verzeichnis
BASE_DIR = Path(__file__).resolve().parent.parent

# API-Konfiguration
API_KEY = os.environ.get("GOOGLE_API_KEY")
DEFAULT_MODEL = "gemini-2.0-flash"  # Kann überschrieben werden

# Spielkonfiguration
MAX_HISTORY_LENGTH = 10000  # Maximale Länge des History-Updates
MAX_STUNT_POINTS = 3
MAX_HITS = 3

# UI-Konfiguration
TERMINAL_WIDTH = 80
TEXT_SPEED = 0.01  # Sekunden pro Zeichen für Textanimation
```

## Hinweise zur Verwendung der API

1. **API-Schlüssel**: Stelle sicher, dass ein API-Schlüssel über Google AI Studio erstellt wurde und als Umgebungsvariable `GOOGLE_API_KEY` gesetzt ist oder via `.env`-Datei geladen wird.

2. **Modellauswahl**: 
   - Für schnellere Antworten: `gemini-2.0-flash`
   - Für komplexere Narrative: `gemini-2.0-pro`
   - Bei eingeschränktem Budget: `gemini-1.5-flash`

3. **Strukturierte Antworten**: Nutze konsequent `response_mime_type: "application/json"` und `response_schema` für konsistente, parsbare Antworten.

4. **Token-Limit beachten**: Achte auf das Token-Limit und komprimiere History-Updates bei Bedarf.

5. **Streaming**: Verwende Streaming für längere Beschreibungen, um ein interaktiveres Erlebnis zu schaffen.

6. **Fehlerbehandlung**: Implementiere robuste Fehlerbehandlung für API-Timeouts oder unerwartete Antwortformate.

Mit diesen konkreten Implementierungsvorschlägen hast du eine solide Grundlage für die Integration der Gemini API in dein Cyberpunk RPG. Die Kombination aus strukturierten JSON-Antworten, Chat-basierter Spielleitung und Function Calling für Spielmechaniken ermöglicht ein dynamisches und immersives Spielerlebnis.