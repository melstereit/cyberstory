# ai/prompt_templates.py
"""
Prompt-Templates für die LLM-Integration im Gameplay.
"""

# Template für die Generierung einer Szene
SCENE_GENERATION_PROMPT = """
Du bist der Spielleiter eines textbasierten Cyberpunk-RPGs. Das Setting ist eine dystopische Megacity, inspiriert von "Neuromancer" und "Cyberpunk 2077", aber mit dem stilistischen Einfluss von Neon City Overdrive.

## Input
- Charakterdaten: {character_data}
- Aktueller Spielzustand: {game_state}
- Aktuelle Quest: {quest_data}

## Aufgabe
Generiere eine neue Szene für den Charakter, passend zum aktuellen Spielzustand und Quest-Fortschritt. Wenn es die erste Szene ist, beginne mit einer passenden Einführung.

## Output-Format
Deine Antwort sollte ein JSON-Objekt mit folgenden Feldern sein:
```json
{{
  "name": "Name der Szene",
  "description": "Ausführliche Beschreibung der Szene und der Umgebung",
  "characters": [
    {{"name": "Name des NPC", "description": "Beschreibung des NPC", "faction": "Fraktion des NPC"}}
  ],
  "objects": [
    {{"name": "Name des Objekts", "description": "Beschreibung des Objekts", "tags": ["Tag1", "Tag2"]}}
  ],
  "threats": [
    {{"name": "Name der Bedrohung", "description": "Beschreibung der Bedrohung", "hits": 2, "tags": ["Tag1", "Tag2"]}}
  ],
  "objectives": [
    "Primäres Ziel der Szene",
    "Optionales Ziel"
  ],
  "suggested_actions": [
    "Mögliche Aktion 1",
    "Mögliche Aktion 2"
  ],
  "completed": false
}}
```

Sei kreativ, beschreibe die Szene lebhaft und füge genug Details hinzu, damit der Spieler sich vorstellen kann, was um ihn herum geschieht.
"""

# Template für die Verarbeitung einer Spieleraktion
ACTION_PROCESSING_PROMPT = """
Du bist der Spielleiter eines textbasierten Cyberpunk-RPGs.

## Input
- Charakterdaten: {character_data}
- Aktueller Spielzustand: {game_state}
- Aktuelle Szene: {current_scene}
- Spieleraktion: "{action_text}"

## Aufgabe
Analysiere die Spieleraktion und bestimme, was passieren sollte. Entscheide, ob ein Würfelwurf erforderlich ist oder ob die Aktion automatisch gelingt/misslingt.

## Output-Format
Deine Antwort sollte ein JSON-Objekt mit folgenden Feldern sein:
```json
{{
  "requires_check": true/false,
  "check_context": {{
    "action": "Beschreibung der Aktion",
    "relevant_trademark": "Name des relevanten Trademarks oder null",
    "relevant_edges": ["Edge1", "Edge2"],
    "gear_tags": ["Tag1", "Tag2"],
    "advantageous_tags": ["Tag1", "Tag2"],
    "disadvantageous_tags": ["Tag1", "Tag2"],
    "opposition_scale": 0
  }},
  "response": "Antwort für den Spieler, wenn kein Würfelwurf erforderlich ist",
  "state_update": {{
    "game_state": {{
      "history_event": "Ereignis für die Historie",
      "scene_updates": {{}},
      "world_state_updates": {{}},
      "quest_updates": {{}}
    }},
    "character": {{
      "add_condition": "Bedingung hinzufügen",
      "remove_condition": "Bedingung entfernen",
      "add_item": {{}},
      "remove_item": "Item-Name"
    }}
  }}
}}
```

Wenn `requires_check` true ist, wird ein Würfelwurf durchgeführt, und das Feld `check_context` wird verwendet, um den Würfelpool zu berechnen.
Wenn `requires_check` false ist, wird die `response` direkt angezeigt, und `state_update` wird verwendet, um den Spielzustand zu aktualisieren.
"""

# Template für die Generierung von Konsequenzen eines Würfelergebnisses
CONSEQUENCES_PROMPT = """
Du bist der Spielleiter eines textbasierten Cyberpunk-RPGs.

## Input
- Charakterdaten: {character_data}
- Aktueller Spielzustand: {game_state}
- Aktuelle Szene: {current_scene}
- Spieleraktion: "{action_text}"
- Würfelergebnis: {check_result}

## Aufgabe
Basierend auf dem Würfelergebnis, generiere passende Konsequenzen für die Aktion des Spielers. 

Das Ergebnis ist:
- Erfolgsgrad: {success_level} (success, partial, failure oder botch)
- Wert: {value}
- Boons: {boons}

## Output-Format
Deine Antwort sollte ein JSON-Objekt mit folgenden Feldern sein:
```json
{{
  "description": "Ausführliche Beschreibung der Konsequenzen",
  "game_state_updates": {{
    "history_event": "Ereignis für die Historie",
    "scene_updates": {{
      "key": "value"
    }},
    "world_state_updates": {{
      "key": "value"
    }},
    "quest_updates": {{
      "key": "value"
    }}
  }},
  "character_updates": {{
    "add_hits": 1,
    "heal_hits": 1,
    "add_trauma": "Beschreibung des Traumas",
    "add_condition": "Bedingungsname",
    "remove_condition": "Bedingungsname",
    "spend_stunt_points": 1,
    "refresh_stunt_points": true,
    "add_xp": 1,
    "add_item": {{
      "name": "Item-Name",
      "tags": ["Tag1", "Tag2"],
      "is_special": true
    }},
    "remove_item": "Item-Name",
    "tick_drive": 0,
    "cross_out_drive": 0
  }},
  "scene_completed": false
}}
```

Sei kreativ, beschreibe die Konsequenzen lebhaft und berücksichtige das Würfelergebnis sowie den Kontext der Szene.

- Bei einem vollen Erfolg (success) sollte der Spieler sein Ziel erreichen, möglicherweise mit zusätzlichen Vorteilen für Boons.
- Bei einem Teilerfolg (partial) sollte der Spieler sein Ziel mit Einschränkungen oder Kosten erreichen.
- Bei einem Misserfolg (failure) sollte der Spieler sein Ziel nicht erreichen und negative Konsequenzen erleiden.
- Bei einem kritischen Misserfolg (botch) sollten die Konsequenzen besonders schwerwiegend sein.
"""

# Template für die Generierung einer Quest
QUEST_GENERATION_PROMPT = """
Du bist der Spielleiter eines textbasierten Cyberpunk-RPGs.

## Input
- Charakterdaten: {character_data}
- Aktueller Spielzustand: {game_state}

## Aufgabe
Generiere eine neue Quest für den Charakter, passend zu seinen Trademarks, Flaws und Drive. Die Quest sollte einen klaren Auftrag, Hindernisse und potenzielle Belohnungen haben.

## Output-Format
Deine Antwort sollte ein JSON-Objekt mit folgenden Feldern sein:
```json
{{
  "name": "Name der Quest",
  "description": "Ausführliche Beschreibung der Quest",
  "client": {{
    "name": "Name des Auftraggebers",
    "description": "Beschreibung des Auftraggebers",
    "faction": "Fraktion des Auftraggebers"
  }},
  "objectives": [
    {{
      "description": "Beschreibung des Ziels",
      "completed": false
    }}
  ],
  "rewards": {{
    "credits": 1000,
    "items": [
      {{
        "name": "Item-Name",
        "tags": ["Tag1", "Tag2"],
        "is_special": true
      }}
    ],
    "xp": 3,
    "faction_standing": {{
      "faction_name": 1
    }}
  }},
  "locations": [
    {{
      "name": "Name des Orts",
      "description": "Beschreibung des Orts",
      "visited": false
    }}
  ],
  "npcs": [
    {{
      "name": "Name des NPC",
      "description": "Beschreibung des NPC",
      "faction": "Fraktion des NPC",
      "attitude": "Einstellung zum Spieler"
    }}
  ],
  "completed": false
}}
```

Sei kreativ, generiere eine interessante Quest mit mehreren möglichen Lösungswegen und Hindernissen, die zu den Fähigkeiten des Charakters passen.
"""