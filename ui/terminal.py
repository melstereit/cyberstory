# ui/terminal.py
import os
import textwrap
import time
from typing import List, Optional

class TerminalUI:
    """Einfache Terminal-UI für das Cyberpunk RPG."""
    
    def __init__(self, width: int = 80):
        """
        Initialisiert die Terminal-UI.
        
        Args:
            width: Die Breite des Terminals in Zeichen
        """
        self.width = width
    
    def clear_screen(self) -> None:
        """Löscht den Bildschirm."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_title(self, title: str) -> None:
        """
        Zeigt einen formatierten Titel an.
        
        Args:
            title: Der anzuzeigende Titel
        """
        print("\n" + "=" * self.width)
        print(title.center(self.width))
        print("=" * self.width + "\n")
    
    def display_subtitle(self, subtitle: str) -> None:
        """
        Zeigt einen formatierten Untertitel an.
        
        Args:
            subtitle: Der anzuzeigende Untertitel
        """
        print("\n" + "-" * self.width)
        print(subtitle)
        print("-" * self.width)
    
    def display_text(self, text: str, wrap: bool = True) -> None:
        """
        Zeigt Text an, optional mit Umbruch.
        
        Args:
            text: Der anzuzeigende Text
            wrap: Ob der Text umgebrochen werden soll
        """
        if wrap:
            wrapped_lines = textwrap.wrap(text, width=self.width)
            for line in wrapped_lines:
                print(line)
        else:
            print(text)
    
    def display_streaming_text(self, text: str, delay: float = 0.01) -> None:
        """
        Zeigt Text mit einem Tippeffekt an.
        
        Args:
            text: Der anzuzeigende Text
            delay: Verzögerung zwischen den Zeichen in Sekunden
        """
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def get_input(self, prompt: str) -> str:
        """
        Fordert eine Eingabe vom Benutzer an.
        
        Args:
            prompt: Die Eingabeaufforderung
        
        Returns:
            Die Benutzereingabe
        """
        print(f"\n{prompt}")
        return input("> ").strip()
    
    def get_multiline_input(self, prompt: str = "Gib Text ein (leere Zeile zum Beenden):") -> str:
        """
        Fordert mehrzeilige Eingabe vom Benutzer an.
        
        Args:
            prompt: Die Eingabeaufforderung
        
        Returns:
            Die mehrzeilige Benutzereingabe
        """
        print(f"\n{prompt}")
        lines = []
        while True:
            line = input("> ").rstrip()
            if not line:
                break
            lines.append(line)
        return "\n".join(lines)
    
    def get_choice(self, prompt: str, options: List[str]) -> int:
        """
        Lässt den Benutzer eine Option aus einer Liste auswählen.
        
        Args:
            prompt: Die Eingabeaufforderung
            options: Die Liste der Optionen
        
        Returns:
            Der Index der ausgewählten Option
        """
        if not options:
            return -1
        
        print(f"\n{prompt}")
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")
        
        while True:
            try:
                choice = input("\nWähle eine Option (1-{}): ".format(len(options)))
                choice_index = int(choice) - 1
                
                if 0 <= choice_index < len(options):
                    return choice_index
                
                print(f"Ungültige Auswahl. Bitte wähle 1-{len(options)}.")
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Zahl ein.")
    
    def get_yes_no(self, prompt: str) -> bool:
        """
        Fordert eine Ja/Nein-Antwort vom Benutzer an.
        
        Args:
            prompt: Die Eingabeaufforderung
        
        Returns:
            True für Ja, False für Nein
        """
        print(f"\n{prompt} (J/N)")
        while True:
            choice = input("> ").strip().upper()
            if choice in ["J", "JA", "Y", "YES"]:
                return True
            elif choice in ["N", "NEIN", "NO"]:
                return False
            else:
                print("Bitte antworte mit J oder N.")
    
    def display_progress_bar(self, progress: float, total: float, width: int = 40) -> None:
        """
        Zeigt einen Fortschrittsbalken an.
        
        Args:
            progress: Der aktuelle Fortschritt
            total: Der Gesamtwert
            width: Die Breite des Fortschrittsbalkens
        """
        if total == 0:
            percent = 0
        else:
            percent = progress / total
        
        filled_length = int(width * percent)
        bar = '█' * filled_length + '-' * (width - filled_length)
        
        print(f"\r|{bar}| {percent:.1%}", end='\r')
        
        if progress == total:
            print()