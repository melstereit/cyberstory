# test_llm.py
import os
import json
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env Datei
load_dotenv()

from cyberstory.ai.llm_interface import LLMInterface
from cyberstory.ai.gameplay_integration import LLMGameplayIntegration

def test_llm_connection():
    """Testet die grundlegende Verbindung zum LLM."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Kein API-Schlüssel gefunden. Bitte setze die Umgebungsvariable GOOGLE_API_KEY.")
        return
    
    # LLM-Interface initialisieren
    llm = LLMInterface(api_key=api_key)
    
    # Einfachen Test durchführen
    prompt = "Antworte mit einem einfachen JSON-Objekt mit einem 'message'-Feld, das 'Hello, World!' enthält."
    
    try:
        print(f"Sende Testanfrage an Modell: {llm.model}")
        response = llm.client.models.generate_content(
            model=llm.model,
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        
        print(f"Rohtext-Antwort: {response.text}")
        
        # Versuche die JSON-Antwort zu parsen
        try:
            result = response.parsed
            print(f"Geparste Antwort: {result}")
            return True
        except Exception as e:
            print(f"Fehler beim Parsen der JSON-Antwort: {e}")
            return False
            
    except Exception as e:
        print(f"Fehler bei der LLM-Verbindung: {e}")
        return False

def test_scene_generation():
    """Testet die Szenengenerierung mit dem LLM."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Kein API-Schlüssel gefunden. Bitte setze die Umgebungsvariable GOOGLE_API_KEY.")
        return
    
    # LLM-Interface und Gameplay-Integration initialisieren
    llm = LLMInterface(api_key=api_key)
    gameplay_llm = LLMGameplayIntegration(llm)
    
    # Debug-Methode aufrufen
    scene = gameplay_llm.debug_scene_generation()
    
    # Ergebnis anzeigen
    if scene:
        print("\nGenerierte Szene:")
        print(f"Name: {scene.get('name')}")
        print(f"Beschreibung: {scene.get('description')[:100]}...")
        return scene
    else:
        print("Keine Szene generiert.")
        return None

if __name__ == "__main__":
    print("=== TEST LLM-VERBINDUNG ===")
    connection_ok = test_llm_connection()
    print(f"LLM-Verbindungstest {'erfolgreich' if connection_ok else 'fehlgeschlagen'}")
    
    if connection_ok:
        print("\n=== TEST SZENENGENERIERUNG ===")
        scene = test_scene_generation()