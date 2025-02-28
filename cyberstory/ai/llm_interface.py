# ai/llm_interface.py
import os

from google import genai


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