# Testen und Ausprobieren des aktuellen Projektstands

Jetzt, da Phase 1 (Würfelsystem) und Phase 2 (Charaktersystem) mit Datenbankintegration abgeschlossen sind, kannst du den aktuellen Stand testen und ausprobieren. Hier ist eine Anleitung, wie du vorgehen kannst:

## 1. Projektstruktur einrichten

Stelle zunächst sicher, dass du die richtige Verzeichnisstruktur hast:

```bash
mkdir -p cyberpunk_rpg/{ai,character,data,mechanics,ui,utils,data/templates}
touch cyberpunk_rpg/__init__.py
touch cyberpunk_rpg/main.py
```

Erstelle in jedem Unterverzeichnis eine `__init__.py`-Datei:

```bash
touch cyberpunk_rpg/ai/__init__.py
touch cyberpunk_rpg/character/__init__.py
touch cyberpunk_rpg/data/__init__.py
touch cyberpunk_rpg/mechanics/__init__.py
touch cyberpunk_rpg/ui/__init__.py
touch cyberpunk_rpg/utils/__init__.py
```

## 2. Abhängigkeiten installieren

Erstelle eine `requirements.txt`-Datei mit den notwendigen Abhängigkeiten:

```
google-genai==1.0.0
python-dotenv==1.0.0
```

Installiere die Abhängigkeiten:

```bash
pip install -r requirements.txt
```

## 3. API-Schlüssel konfigurieren

Erstelle eine `.env`-Datei im Hauptverzeichnis und trage deinen Gemini-API-Schlüssel ein:

```
GOOGLE_API_KEY=dein_api_schlüssel_hier
```

## 4. Testskripte erstellen

Erstelle ein Verzeichnis für Testskripte und einzelne Tests für die verschiedenen Komponenten:

```bash
mkdir -p cyberpunk_rpg/tests
touch cyberpunk_rpg/tests/__init__.py
```

### Test für das Würfelsystem

Erstelle `cyberpunk_rpg/tests/test_dice.py`:

```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mechanics.nco_dice_system import NCODiceSystem
from mechanics.check_manager import CheckManager

def test_dice_system():
    print("\n=== Würfelsystem-Test ===")
    dice_system = NCODiceSystem()
    
    # Einfacher Würfelwurf
    print("\n1. Einfacher Würfelwurf (3 Action, 1 Danger):")
    result = dice_system.perform_check(3, 1)
    print(f"Action Dice: {result.action_dice}")
    print(f"Danger Dice: {result.danger_dice}")
    print(f"Verbleibende Würfel: {result.remaining_dice}")
    print(f"Höchstes Ergebnis: {result.value}")
    print(f"Erfolgsgrad: {result.success_level}")
    print(f"Boons: {result.boons}")
    
    # Check-Manager
    print("\n2. Check mit Check-Manager:")
    check_manager = CheckManager(dice_system)
    
    # Beispiel-Charakterdaten und Check-Kontext
    character_data = {
        "id": "test-char",
        "name": "Test Charakter",
        "trademarks": {"Codeslinger": {"name": "Codeslinger"}},
        "traumas": []
    }
    
    check_context = {
        "action": "Hacken eines Terminals",
        "relevant_trademark": "Codeslinger",
        "relevant_edges": ["Hacking"],
        "gear_tags": ["High-End Deck"],
        "advantageous_tags": []
    }
    
    check_result = check_manager.perform_check(character_data, check_context)
    print(check_manager.get_check_description(check_result["pool_details"]))
    print(f"Ergebnis: {check_result['result'].success_level} (Wert: {check_result['result'].value})")
    print(f"Check-ID: {check_result['check_id']}")

if __name__ == "__main__":
    test_dice_system()
```

### Test für das Charaktersystem

Erstelle `cyberpunk_rpg/tests/test_character.py`:

```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from character.manager import CharacterManager
from character.interfaces import Trademark, Edge, Flaw, Drive, Item

def test_character_system():
    print("\n=== Charaktersystem-Test ===")
    
    # CharacterManager initialisieren
    char_manager = CharacterManager()
    
    # 1. Charakter erstellen
    print("\n1. Charakter erstellen:")
    char_data = char_manager.create_character("Raven", "Anarchisten")
    char_id = char_data.get("id")
    print(f"Charakter erstellt: {char_data['name']} (ID: {char_id})")
    
    # 2. Trademarks hinzufügen
    print("\n2. Trademarks hinzufügen:")
    trademark1 = Trademark(
        name="Codeslinger",
        triggers=["Hacking", "Security systems", "Computers"]
    )
    trademark2 = Trademark(
        name="Infiltrator",
        triggers=["Stealth", "Locks", "Security systems"]
    )
    
    char_manager.add_trademark(char_id, trademark1)
    char_manager.add_trademark(char_id, trademark2)
    print("Trademarks hinzugefügt: Codeslinger, Infiltrator")
    
    # 3. Edges hinzufügen
    print("\n3. Edges hinzufügen:")
    edge1 = Edge(name="Hacking", trademark="Codeslinger")
    edge2 = Edge(name="Security systems", trademark="Codeslinger")
    edge3 = Edge(name="Stealth", trademark="Infiltrator")
    
    char_manager.add_edge(char_id, edge1)
    char_manager.add_edge(char_id, edge2)
    char_manager.add_edge(char_id, edge3)
    print("Edges hinzugefügt: Hacking, Security systems, Stealth")
    
    # 4. Flaws hinzufügen
    print("\n4. Flaws hinzufügen:")
    flaw1 = Flaw(name="Wanted", description="Auf der Fahndungsliste von Osiris Corp")
    flaw2 = Flaw(name="Addiction", description="Abhängig von synthetischen Stimulanzien")
    
    char_manager.add_flaw(char_id, flaw1)
    char_manager.add_flaw(char_id, flaw2)
    print("Flaws hinzugefügt: Wanted, Addiction")
    
    # 5. Drive setzen
    print("\n5. Drive setzen:")
    drive = Drive(description="Clear my name from Osiris Corp's records")
    char_manager.set_drive(char_id, drive)
    print("Drive gesetzt: Clear my name from Osiris Corp's records")
    
    # 6. Ausrüstung hinzufügen
    print("\n6. Ausrüstung hinzufügen:")
    item1 = Item(name="High-End Deck", tags=["Fast", "Powerful", "Concealed"], is_special=True)
    item2 = Item(name="Pistol", tags=["Accurate", "Silenced"], is_special=True)
    item3 = Item(name="Synth-Leather Jacket", is_special=False)
    
    char_manager.add_item(char_id, item1)
    char_manager.add_item(char_id, item2)
    char_manager.add_item(char_id, item3)
    print("Ausrüstung hinzugefügt: High-End Deck, Pistol, Synth-Leather Jacket")
    
    # 7. Charakter laden und anzeigen
    print("\n7. Charakter laden und anzeigen:")
    updated_char = char_manager.get_character(char_id)
    print(f"Name: {updated_char['name']} (Fraktion: {updated_char['faction']})")
    print(f"Trademarks: {', '.join(updated_char['trademarks'].keys())}")
    
    edges = [edge["name"] for edge in updated_char["edges"]]
    print(f"Edges: {', '.join(edges)}")
    
    flaws = [flaw["name"] for flaw in updated_char["flaws"]]
    print(f"Flaws: {', '.join(flaws)}")
    
    print(f"Drive: {updated_char['drive']['description']}")
    
    inventory = [item["name"] for item in updated_char["inventory"]]
    print(f"Inventar: {', '.join(inventory)}")
    
    # 8. Alle Charaktere anzeigen
    print("\n8. Alle Charaktere anzeigen:")
    all_chars = char_manager.get_all_characters()
    for char in all_chars:
        print(f"- {char['name']} (ID: {char['id']})")
    
    # 9. Charakter aktualisieren
    print("\n9. Charakter aktualisieren:")
    updates = {
        "stunt_points": 2,  # 1 ausgegeben
        "xp": 3,             # 3 XP verdient
        "add_trauma": "Damaged Cybereye"  # Trauma hinzufügen
    }
    
    char_manager.update_character(char_id, updates)
    updated_char = char_manager.get_character(char_id)
    print(f"Stunt Points: {updated_char['stunt_points']}")
    print(f"XP: {updated_char['xp']}")
    print(f"Traumas: {updated_char['traumas']}")
    
    # Wir löschen den Testcharakter nicht, um ihn für andere Tests zu behalten
    # char_manager.delete_character(char_id)  
    print("\nTest abgeschlossen.")

if __name__ == "__main__":
    test_character_system()
```

### Test für die Datenbankintegration

Erstelle `cyberpunk_rpg/tests/test_database.py`:

```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.json_database import JSONDatabase
from data.game_state import GameState, GameStateManager
from data.session_handler import SessionHandler
from data.config_handler import ConfigHandler

def test_database():
    print("\n=== Datenbank-Test ===")
    
    # 1. Konfigurations-Handler testen
    print("\n1. Konfigurations-Handler:")
    config = ConfigHandler()
    
    print(f"Terminal-Breite: {config.get('ui.terminal_width')}")
    print(f"Animation Speed: {config.get('ui.animation_speed')}")
    
    # Konfiguration ändern
    config.set("ui.terminal_width", 100)
    print(f"Neue Terminal-Breite: {config.get('ui.terminal_width')}")
    
    # 2. Sitzungs-Handler testen
    print("\n2. Sitzungs-Handler:")
    session = SessionHandler()
    
    session.set_session_value("test_value", "Dies ist ein Test")
    print(f"Sitzungswert: {session.get_session_value('test_value')}")
    
    # 3. GameStateManager testen
    print("\n3. GameStateManager:")
    gsm = GameStateManager()
    
    # Verwende die Charakter-ID von test_character.py, falls verfügbar
    char_manager = CharacterManager()
    characters = char_manager.get_all_characters()
    
    if characters:
        char_id = characters[0]["id"]
        
        # Spiel erstellen
        game_state = gsm.new_game(char_id)
        game_id = game_state.id
        print(f"Neues Spiel erstellt: {game_id}")
        
        # Spielzustand ändern
        game_state.current_scene = {
            "name": "The Bar",
            "description": "Ein düsterer Ort mit vielen zwielichtigen Gestalten."
        }
        
        # Ereignisse zur Historie hinzufügen
        gsm.add_event_to_history("Charakter betritt die Bar")
        gsm.add_event_to_history("Charakter spricht mit dem Barkeeper")
        
        # Spielstand speichern
        gsm.save_game()
        print("Spielstand gespeichert")
        
        # Gespeicherte Spiele auflisten
        saved_games = gsm.get_saved_games()
        print(f"Gespeicherte Spiele: {len(saved_games)}")
        
        for game in saved_games:
            print(f"- {game['id']} (Charakter: {game['active_character_id']})")
    else:
        print("Keine Charaktere gefunden. Führe zuerst test_character.py aus.")
    
    print("\nTest abgeschlossen.")

if __name__ == "__main__":
    test_database()
```

## 5. Hauptanwendung starten

Wenn du alle Module korrekt implementiert hast, kannst du die Hauptanwendung starten:

```bash
cd cyberpunk
python main.py
```

## 6. Schrittweise Ausführung der Tests

Führe die Tests in der richtigen Reihenfolge aus, um die Komponenten zu testen:

1. Zuerst das Charaktersystem testen:
```bash
python tests/test_character.py
```

2. Dann die Datenbankintegration testen:
```bash
python tests/test_database.py
```

3. Schließlich das Würfelsystem testen:
```bash
python tests/test_dice.py
```

## 7. Experimentieren und Testen

Hier sind weitere Ideen zum Experimentieren mit dem aktuellen Stand:

### Charaktererstellung manuell testen

Erstelle eine Testdatei `cyberpunk_rpg/tests/test_character_creation.py`:

```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.terminal import TerminalUI
from character.manager import CharacterManager
from character.templates import TemplateManager
from character.creation import CharacterCreation
from character.gear_manager import GearManager
from ui.character_creation_ui import CharacterCreationUI

def test_character_creation():
    # UI initialisieren
    ui = TerminalUI()
    
    # Manager initialisieren
    char_manager = CharacterManager()
    template_manager = TemplateManager()
    gear_manager = GearManager()
    
    # Charaktererstellung initialisieren
    creation = CharacterCreation(char_manager, template_manager, gear_manager)
    
    # UI für die Charaktererstellung
    creation_ui = CharacterCreationUI(ui, creation)
    
    # Charaktererstellungsprozess starten
    creation_ui.start_creation()

if __name__ == "__main__":
    test_character_creation()
```

### LLM-Integration testen (wenn implementiert)

Falls du die LLM-Integration für die Charaktererstellung implementiert hast:

```python
import sys
import os
import dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

dotenv.load_dotenv()

from ai.llm_interface import LLMInterface
from character.llm_integration import CharacterLLMIntegration

def test_llm_integration():
    print("\n=== LLM-Integration-Test ===")
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("FEHLER: Kein API-Schlüssel gefunden. Setze GOOGLE_API_KEY in der .env-Datei.")
        return
    
    # LLM-Interface initialisieren
    llm = LLMInterface(api_key=api_key)
    
    # CharacterLLMIntegration initialisieren
    llm_integration = CharacterLLMIntegration(llm)
    
    # Hintergrundgeschichte für Vorschläge
    background = """
    Als ehemaliger Sicherheitsexperte bei Osiris Corp habe ich mich mit dem falschen Vorgesetzten angelegt. 
    Nach der Aufdeckung eines internen Korruptionsnetzwerks wurde ich entlassen und auf die schwarze Liste gesetzt. 
    Jetzt schlage ich mich mit Hacking-Jobs und Sicherheitsberatung für kleinere Firmen durch, 
    während ich versuche, meinen Namen reinzuwaschen.
    """
    
    print("\nTrademark-Vorschläge generieren...")
    trademarks = llm_integration.suggest_trademarks_from_background(background, count=3)
    
    print(f"Generierte {len(trademarks)} Trademarks:")
    for tm in trademarks:
        print(f"\n- {tm['name']}")
        print(f"  Beschreibung: {tm.get('description', 'Keine Beschreibung')}")
        print(f"  Triggers: {', '.join(tm.get('triggers', []))[:60]}...")
        print(f"  Flaws: {', '.join(tm.get('flaws', []))}")
    
    # Beispiel-Charakterdaten für weitere Tests
    character_data = {
        "name": "Raven",
        "trademarks": {"Codeslinger": {}, "Corporate Dropout": {}},
        "flaws": [{"name": "Wanted"}]
    }
    
    print("\nDrive-Vorschläge generieren...")
    drives = llm_integration.suggest_drives_for_character(character_data)
    
    print("Generierte Drives:")
    for drive in drives:
        print(f"- {drive}")
    
    print("\nTest abgeschlossen.")

if __name__ == "__main__":
    test_llm_integration()
```

## 8. Debugging-Tipps

Wenn du auf Probleme stößt:

1. **Überprüfe die Imports**: Stelle sicher, dass alle Modul-Importe korrekt sind.

2. **Überprüfe die Verzeichnisstruktur**: Die Verzeichnisstruktur muss korrekt sein, damit die relativen Imports funktionieren.

3. **Überprüfe die Konfigurationsdateien**: Stelle sicher, dass der API-Schlüssel korrekt eingerichtet ist.

4. **Debug-Ausgaben**: Füge temporär `print()`-Anweisungen an kritischen Stellen ein, um den Programmfluss zu verfolgen.

5. **Dateiberechtigungen**: Stelle sicher, dass dein Programm Lese- und Schreibrechte für die Datenverzeichnisse hat.

## 9. Nächste Schritte

Nachdem du das System getestet hast, könntest du:

1. **UI verbessern**: Erweitere die Terminal-UI um Farben und bessere Formatierung.

2. **Mehr Testszenarien erstellen**: Teste Grenzfälle wie volle Hit-Tracks, erschöpfte Stunt Points usw.

3. **Phase 3 vorbereiten**: Beginne mit der Planung der Spielmechanik-Implementierung für Phase 3.

Mit diesen Schritten kannst du den aktuellen Stand deines Projekts umfassend testen und die Funktionalität der implementierten Komponenten überprüfen.