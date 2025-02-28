# Cyberpunk RPG Terminal-Based MVP Konzept

Basierend auf deinem Prompt und den bereitgestellten Materialien (Neon City Overdrive) werde ich ein Konzept für ein KI-basiertes TTRPG im Terminal mit Python entwickeln. Hier ist mein Vorschlag für einen MVP (Minimum Viable Product):

## 1. Spielphasen und Anforderungen

### 1.1. Spielphasen:

1. **Spielinitialisierung**
   - Laden der Konfigurationen
   - Verbindung mit der LLM-API herstellen

2. **Charaktererstellung**
   - Spieler gibt Namen und Hintergrundgeschichte ein
   - Auswahl von 2 Trademarks (mit je 3 Triggern)
   - Auswahl von Flaws
   - Festlegung eines Drives
   - Ausrüstungsverteilung

3. **Erste Quest**
   - Einführung durch KI-Spielleiter
   - Erste Begegnung mit dem mysteriösen Auftraggeber
   - Hackauftrag als Einstiegsmission

4. **Spielablauf (Game Loop)**
   - Szenenaufbau durch KI
   - Spielereingabe und -aktionen
   - Würfelmechanik und Konfliktauflösung
   - Szenenübergänge
   - Questabschluss

5. **Downtime**
   - Charakterentwicklung
   - Verwaltung des Drive-Fortschritts
   - Erholung und Heilung

6. **Offene Spielwelt**
   - Multiple Questangebote
   - Freie Erkundung

### 1.2. Anforderungen je Phase:

| Phase | Python-Code | LLM |
|-------|-------------|-----|
| Spielinitialisierung | Konfiguration laden, Spielzustand initialisieren | - |
| Charaktererstellung | Optionen anzeigen, Eingaben speichern | Vorschläge für Charakterkonzepte und Hintergrundgeschichten |
| Erste Quest | Würfelmechanik, Statusverwaltung | Questgenerierung, Szenenbeschreibung, NPC-Dialoge |
| Spielablauf | Mechanikverarbeitung, Statustracking | Narration, Interpretation von Spieleraktionen, Reaktionen |
| Downtime | XP-Berechnung, Charakterfortschritt | Kontextrelevante Ereignisse, Konsequenzen |
| Offene Spielwelt | Questverwaltung, Ortsnavigation | Generierung von Quests und Orten, lebendige Welt |

## 2. Funktionsaufteilung

### 2.1. Python-Code übernimmt:

- **Spielmechanik**
  - Würfeln (Action Dice, Danger Dice)
  - Checks und Ergebnisauswertung
  - Kampfmechanik
  - Charakterstatus (Hits, Trauma, Stunt Points)

- **Spielzustandsverwaltung**
  - JSON-Datenverwaltung
  - Speichern/Laden von Spielständen
  - Tracking von Quests und Fortschritt

- **Benutzeroberfläche**
  - Terminalanzeige und Formatierung
  - Eingabeverarbeitung
  - Menünavigation

### 2.2. LLM übernimmt:

- **Narrative Generierung**
  - Szenenbeschreibungen 
  - NPC-Dialoge
  - Questgenerierung
  - Konsequenzen von Aktionen

- **Spielleitung**
  - Interpretation der Spieleraktionen
  - Anpassung der Spielwelt an Entscheidungen
  - Erzeugung von Atmosphäre und Stimmung

- **Entscheidungsfindung für NPCs**
  - Reaktionen von NPCs
  - Taktik von Gegnern
  - Umweltreaktionen

## 3. JSON-Datenstruktur

```json
{
  "response": null,
  "data_update": {
    "name": null,
    "faction": null,
    "trademarks": {},
    "flaws": [],
    "drive": {
      "description": "",
      "track": [false, false, false, false, false, false, false, false, false, false]
    },
    "edges": [],
    "stunt_points": 3,
    "inventory": [],
    "xp": 0,
    "current_quest": null,
    "locations": {
      "known": [],
      "current_location": null,
      "routes": {}
    },
    "contacts": {
      "allies": [],
      "factions_status": {},
      "current_intel": ""
    },
    "enemies": {
      "known": [],
      "suspected": [],
      "status": {}
    },
    "quest_log": [],
    "status_effects": []
  },
  "history_update": null,
  "game_state": {
    "current_scene": null,
    "scene_objects": {},
    "scene_characters": {},
    "active_timers": []
  },
  "world": {
    "locations": {},
    "npcs": {},
    "factions": {}
  }
}
```

## 4. Python-Programmarchitektur

```
cyberpunk_rpg/
├── main.py                  # Haupteinstiegspunkt 
├── game_engine/
│   ├── __init__.py
│   ├── state_manager.py     # Spielzustandsverwaltung
│   ├── character.py         # Charakterverwaltung
│   ├── dice.py              # Würfelmechanik
│   ├── combat.py            # Kampfsystem
│   └── quest.py             # Questverwaltung
├── ui/
│   ├── __init__.py
│   ├── terminal.py          # Terminalanzeige
│   ├── input_handler.py     # Eingabeverarbeitung
│   └── formatters.py        # Textformatierung
├── ai/
│   ├── __init__.py
│   ├── llm_interface.py     # API-Kommunikation
│   ├── prompt_builder.py    # Promptgenerierung
│   ├── response_parser.py   # Antwortverarbeitung
│   └── templates.py         # Promptvorlagen
├── data/
│   ├── __init__.py
│   ├── json_handler.py      # JSON-Operationen
│   ├── game_data.json       # Spielstandsdaten
│   └── templates/
│       ├── trademarks.json  # Vorlagen für Trademarks
│       ├── drives.json      # Vorlagen für Drives
│       └── gear.json        # Ausrüstungsvorlagen
└── utils/
    ├── __init__.py
    ├── config.py            # Konfigurationseinstellungen
    └── helpers.py           # Hilfsfunktionen
```

## 5. Detaillierter Ablauf des Spiels

### 5.1. Spielinitialisierung
- Ladeanzeige und Begrüßung
- Spieloptionen (Neues Spiel / Laden)
- Verbindung zur LLM-API prüfen

### 5.2. Charaktererstellung
- Schrittweise Eingabeaufforderungen
- LLM generiert Vorschläge basierend auf Spielereingaben
- Daten in JSON-Struktur speichern

### 5.3. Spielablauf
1. KI generiert Szenenbeschreibung und schickt sie an Terminal
2. Spieler gibt Aktion ein
3. Python interpretiert grundlegende Befehle (Inventar anzeigen, Hilfe, etc.)
4. Komplexe Aktionen werden an LLM weitergeleitet
5. LLM interpretiert Aktion und generiert Konsequenzen
6. Bei Checks: Python würfelt und verarbeitet Ergebnisse
7. LLM beschreibt Ergebnis narrativ
8. Python aktualisiert Spielzustand in JSON
9. Weiter zu Schritt 1 oder Szenenübergang

## 6. Implementierungsplan

### Phase 1: Grundlegende Funktionalität
1. [x] Terminal-UI und Grundgerüst
2. JSON-Datenbankintegration
3. [x] Grundlegende Würfelmechanik
4. LLM-API-Integration

### Phase 2: Charaktersystem
1. [x] Charaktererstellung
2. [x] Trademarks, Edges, Flaws
3. [x] Inventarverwaltung
4. [x] Charakterstatusanzeige

### Phase 3: Spielmechanik
1. Check-System implementieren
2. Kampfsystem
3. Stunt Points und Konsequenzen
4. Heilung und Traumas

### Phase 4: LLM-Integration
1. Promptvorlagen erstellen
2. Szenengenerierer
3. NPC-Interaktionen
4. Questgenerator

### Phase 5: Hauptspielschleife
1. Szenenübergänge
2. Quest-Tracking
3. Downtime-Aktivitäten
4. XP und Charakterfortschritt

### Phase 6: Testing und Verfeinerung
1. Spielbalance
2. Prompt-Optimierung
3. Fehlerbehebung
4. Dokumentation

## 7. LLM-Prompting-Strategie

Für effektive LLM-Nutzung werden wir drei Haupttypen von Prompts verwenden:

1. **Systemprompt**: Definiert die Rolle des LLM als Spielleiter und enthält die Spielregeln.
   ```
   Du bist der Spielleiter eines textbasierten Cyberpunk-RPGs. Das Setting ist eine dystopische Megacity, inspiriert von "Neuromancer" und "Cyberpunk 2077", aber mit dem stilistischen Einfluss von Neon City Overdrive. Deine Aufgabe ist es, eine lebendige, interaktive Welt zu erschaffen...
   ```

2. **Aktionsprompt**: Für die Interpretation von Spieleraktionen.
   ```
   Der Spieler versucht folgende Aktion: "{user_action}"
   Aktueller Kontext: {current_scene}
   Charakterdaten: {character_summary}
   
   Interpretiere diese Aktion und generiere eine Antwort im JSON-Format mit:
   1. Beschreibung des Ergebnisses
   2. Notwendige Würfelprobe (falls erforderlich)
   3. Mögliche Konsequenzen
   4. Änderungen an der Szene
   ```

3. **Szenenprompt**: Für die Generierung neuer Szenen.
   ```
   Generiere eine neue Szene basierend auf:
   Aktuelle Quest: {current_quest}
   Bisherige Handlung: {short_history}
   Spieleraktionen: {recent_actions}
   
   Die Beschreibung sollte folgendes enthalten:
   1. Atmosphärische Beschreibung der Umgebung
   2. Anwesende NPCs und ihre Haltung
   3. Sichtbare Objekte/Details
   4. Potenzielle Gefahren
   5. Mögliche Interaktionen
   ```

## 8. Beispiel für einen Spielablauf

1. **Spielstart:**
   ```
   >>> Willkommen bei Neon City Overdrive: Terminal Edition
   >>> Verbindung zur KI hergestellt...
   >>> Neues Spiel starten? [J/N]: J
   ```

2. **Charaktererstellung:**
   ```
   >>> Wie lautet dein Name? Raven
   >>> Erzähle mir etwas über deine Hintergrundgeschichte:
   >>> Ich bin in den Slums von Sektor 7 aufgewachsen...
   
   [KI generiert Vorschläge für Trademarks basierend auf Eingabe]
   
   >>> Wähle deine erste Trademark:
   >>> 1. Metroplexer
   >>> 2. Bounty Hunter
   >>> 3. Codeslinger
   >>> Deine Wahl: 3
   ...
   ```

3. **Erste Szene:**
   ```
   [KI generiert Beschreibung]
   
   >>> Der Regen prasselt auf das verrostete Wellblechdach der Bar "Letzte Chance".
   >>> Das Neonlicht draußen taucht den Raum in ein krankes Grün.
   >>> In der hintersten Ecke sitzt eine Frau mit silbernen Implantaten an den
   >>> Schläfen. Sie nickt dir zu und deutet auf den Stuhl gegenüber.
   
   >>> Was möchtest du tun? Ich gehe zu ihr und setze mich
   
   [KI interpretiert und antwortet]
   
   >>> Du schlängelst dich durch die Menge betrunkener Grinder-Arbeiter.
   >>> Als du dich setzt, huscht ein leichtes Lächeln über das Gesicht der Frau.
   >>> "Du bist also Raven. Man sagt, du kennst dich mit Systemen aus. Ich habe
   >>> einen Job für dich..."
   ...
   ```

4. **Check-Beispiel:**
   ```
   >>> Was möchtest du tun? Ich will versuchen, in den Computer einzuhacken
   
   [KI interpretiert und entscheidet, dass ein Check nötig ist]
   
   >>> Würfelprobe erforderlich: Hacking-Check
   >>> Deine Trademark 'Codeslinger' kommt zur Anwendung.
   >>> Edge 'Hacking' gibt +1 Action Die.
   >>> Das System ist gut gesichert: +1 Danger Die.
   >>> Lege Würfel: 3 Action Dice, 1 Danger Die
   
   [Python würfelt]
   
   >>> Action Dice: 2, 5, 6
   >>> Danger Die: 5
   >>> Die 5 wird annulliert!
   >>> Höchstes Ergebnis: 6 - Erfolg!
   
   [KI beschreibt das Ergebnis]
   
   >>> Deine Finger tanzen über das Interface. Codezeilenzeilen fließen über den
   >>> Bildschirm, während du geschickt die Sicherheitsprotokolle umgehst.
   >>> Mit einem zufriedenen Grinsen verschaffst du dir Zugang zu den
   >>> gesicherten Dateien...
   ```

## Schlussfolgerung

Diese MVP-Konzeption bietet eine solide Grundlage für dein KI-basiertes TTRPG-System. Die klare Aufteilung zwischen Python-Code (für Spielmechanik und -zustand) und LLM (für narrative Elemente) nutzt die Stärken beider Technologien optimal. Das JSON-Dateiformat als Datenbank ermöglicht einfache Persistenz ohne komplexe Datenbankeinrichtung.

Das System ist modular aufgebaut, sodass du es schrittweise entwickeln und erweitern kannst. Mit diesem Konzept kannst du einen funktionalen MVP entwickeln, der die Kernelemente des Cyberpunk-RPGs umsetzt und gleichzeitig flexibel genug ist, um später erweitert zu werden.