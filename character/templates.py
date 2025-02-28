# character/templates.py
from character.interfaces import Trademark, Edge, Flaw, Drive
from typing import Dict, List, Any, Optional
import json
import os
import random

class TemplateManager:
    """Verwaltet Templates für Trademarks, Edges, Flaws, usw."""
    
    def __init__(self, template_dir: str = "data/templates"):
        """
        Initialisiert den TemplateManager.
        
        Args:
            template_dir: Verzeichnis für Template-Dateien
        """
        self.template_dir = template_dir
        
        # Verzeichnis erstellen, falls es nicht existiert
        os.makedirs(template_dir, exist_ok=True)
        
        # Templates laden
        self.trademarks = {}  # category -> list of trademarks
        self.load_trademarks()
        
        self.drives = []  # Liste von Drive-Templates
        self.load_drives()
        
        self.flaws = []  # Liste von Flaw-Templates
        self.load_flaws()
    
    def load_trademarks(self) -> bool:
        """
        Lädt Trademark-Templates aus der JSON-Datei.
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        try:
            tm_file = os.path.join(self.template_dir, "trademarks.json")
            
            if os.path.exists(tm_file):
                with open(tm_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.trademarks = data
                return True
            else:
                # Erstelle Standarddatei, wenn sie nicht existiert
                self._create_default_trademarks()
                return True
                
        except Exception as e:
            print(f"Fehler beim Laden der Trademark-Templates: {e}")
        
        return False
    
    def _create_default_trademarks(self) -> None:
        """Erstellt Standardvorlagen für Trademarks."""
        default_trademarks = {
            "backgrounds": [
                {
                    "name": "Arcology Brat",
                    "triggers": ["Educated", "Lie", "Savings", "Sneak", "Gossip", "Athletic", "Respectable", "I know my rights!"],
                    "flaws": ["Family ties", "Looks soft", "Naive", "Fraternity/Sorority ties"]
                },
                {
                    "name": "Gutter Scum",
                    "triggers": ["Begging", "Sneak", "Pick pockets", "Switchblade", "Spot danger", "Escape", "Fight dirty", "I know these streets"],
                    "flaws": ["Gang ties", "Always filthy", "Snitch", "Criminal record"]
                }
                # Weitere aus dem Original-Dokument...
            ],
            "roles": [
                {
                    "name": "Codeslinger",
                    "triggers": ["Hacking", "Notice", "Cyber combat", "Computers", "Security systems", "Defence programs", "Ghost chip", "Repair", "Sense motives"],
                    "flaws": ["Traceable", "Unfit", "Socially awkward"]
                },
                {
                    "name": "Infiltrator",
                    "triggers": ["Stealthy", "Quick", "Hide", "Alarms", "Awareness", "Locks", "Concealed weapon", "Chameleon DNA", "Agile", "Climb", "Traps", "Silent takedown", "Escape"],
                    "flaws": ["Trust no-one", "Calling card", "Wanted"]
                }
                # Weitere aus dem Original-Dokument...
            ],
            "cyberware": [
                {
                    "name": "Cyber Arms",
                    "triggers": ["Push", "Pull", "Hit hard", "Block a blow", "Crush", "Armored", "Blades"],
                    "flaws": ["Poor tactile sense", "Clumsy fingers"]
                },
                {
                    "name": "Cyber Eyes",
                    "triggers": ["Notice", "Target assist", "Thermal imaging", "Camera", "HUD", "VR"],
                    "flaws": ["Easily hacked", "Obvious", "Faulty"]
                }
                # Weitere aus dem Original-Dokument...
            ]
        }
        
        tm_file = os.path.join(self.template_dir, "trademarks.json")
        
        with open(tm_file, 'w', encoding='utf-8') as f:
            json.dump(default_trademarks, f, ensure_ascii=False, indent=2)
        
        self.trademarks = default_trademarks
    
    def load_drives(self) -> bool:
        """
        Lädt Drive-Templates aus der JSON-Datei.
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        try:
            drive_file = os.path.join(self.template_dir, "drives.json")
            
            if os.path.exists(drive_file):
                with open(drive_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.drives = data
                return True
            else:
                # Erstelle Standarddatei, wenn sie nicht existiert
                self._create_default_drives()
                return True
                
        except Exception as e:
            print(f"Fehler beim Laden der Drive-Templates: {e}")
        
        return False
    
    def _create_default_drives(self) -> None:
        """Erstellt Standardvorlagen für Drives."""
        default_drives = [
            {
                "category": "Debt",
                "drives": [
                    "Repay my debt to the Razr Girls",
                    "Recover what I stole from Osiris",
                    "Buy out my Tyla Pharma contract",
                    "Repay Pollux for saving my life",
                    "Bribe Corp Sec to delete my files",
                    "Cover my brother's gambling debt"
                ]
            },
            {
                "category": "Survival",
                "drives": [
                    "Remove my cortex bomb",
                    "Find my missing birth records",
                    "Prove I didn't kill \"Bam Bam\" Crow",
                    "Get back in good with Osiris",
                    "Cure my lover's nano-virus",
                    "Re-skin in a top-of-the-line body"
                ]
            },
            {
                "category": "Vengeance",
                "drives": [
                    "Destroy my family's reputation",
                    "Prove my worth to Warren Falstaff",
                    "Expose Yen Group's crimes",
                    "Find my sister's killer",
                    "Bring down Kitsune Media Corp",
                    "Take control of the family business"
                ]
            }
        ]
        
        drive_file = os.path.join(self.template_dir, "drives.json")
        
        with open(drive_file, 'w', encoding='utf-8') as f:
            json.dump(default_drives, f, ensure_ascii=False, indent=2)
        
        self.drives = default_drives
    
    def load_flaws(self) -> bool:
        """
        Lädt Flaw-Templates aus der JSON-Datei.
        
        Returns:
            bool: True, wenn erfolgreich, sonst False
        """
        try:
            flaw_file = os.path.join(self.template_dir, "flaws.json")
            
            if os.path.exists(flaw_file):
                with open(flaw_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.flaws = data
                return True
            else:
                # Erstelle Standarddatei, wenn sie nicht existiert
                self._create_default_flaws()
                return True
                
        except Exception as e:
            print(f"Fehler beim Laden der Flaw-Templates: {e}")
        
        return False
    
    def _create_default_flaws(self) -> None:
        """Erstellt Standardvorlagen für Flaws."""
        default_flaws = [
            {"name": "Family ties", "description": "You have family obligations that often get in the way."},
            {"name": "Wanted", "description": "Someone is looking for you, and not in a good way."},
            {"name": "Addiction", "description": "You are addicted to a substance or behavior."},
            {"name": "Debt", "description": "You owe someone money, favors, or services."},
            {"name": "Notorious", "description": "Your face or name is well-known for the wrong reasons."},
            {"name": "Vengeful", "description": "You can't let go of a grudge, even when it's in your best interest."},
            {"name": "Phobia", "description": "You have an irrational fear that can paralyze you."},
            {"name": "Flashbacks", "description": "Traumatic memories haunt you and can be triggered unexpectedly."},
            {"name": "Code of honor", "description": "You follow strict personal rules that can be limiting."},
            {"name": "Reckless", "description": "You take unnecessary risks and act without thinking."}
        ]
        
        flaw_file = os.path.join(self.template_dir, "flaws.json")
        
        with open(flaw_file, 'w', encoding='utf-8') as f:
            json.dump(default_flaws, f, ensure_ascii=False, indent=2)
        
        self.flaws = default_flaws
    
    def get_random_trademark(self, category: str = None) -> Optional[Dict[str, Any]]:
        """
        Gibt ein zufälliges Trademark aus einer Kategorie zurück.
        
        Args:
            category: Kategorie (backgrounds, roles, cyberware, etc.)
        
        Returns:
            Dictionary mit den Trademark-Daten oder None
        """
        if not category:
            # Zufällige Kategorie
            if not self.trademarks:
                return None
            
            category = random.choice(list(self.trademarks.keys()))
        
        if category in self.trademarks and self.trademarks[category]:
            return random.choice(self.trademarks[category])
        
        return None
    
    def get_random_drive(self, category: str = None) -> Optional[str]:
        """
        Gibt einen zufälligen Drive zurück.
        
        Args:
            category: Kategorie (Debt, Survival, Vengeance, etc.)
        
        Returns:
            Drive-String oder None
        """
        if not self.drives:
            return None
        
        if category:
            # Suche nach der Kategorie
            for drive_cat in self.drives:
                if drive_cat.get("category") == category:
                    return random.choice(drive_cat.get("drives", []))
        else:
            # Zufällige Kategorie
            drive_cat = random.choice(self.drives)
            return random.choice(drive_cat.get("drives", []))
        
        return None
    
    def get_random_flaw(self) -> Optional[Dict[str, Any]]:
        """
        Gibt einen zufälligen Flaw zurück.
        
        Returns:
            Dictionary mit den Flaw-Daten oder None
        """
        if self.flaws:
            return random.choice(self.flaws)
        
        return None
    
    def get_trademark_edges(self, trademark_name: str) -> List[str]:
        """
        Gibt alle möglichen Edges für ein Trademark zurück.
        
        Args:
            trademark_name: Name des Trademarks
        
        Returns:
            Liste von Edge-Namen
        """
        for category in self.trademarks.values():
            for tm in category:
                if tm.get("name") == trademark_name:
                    return tm.get("triggers", [])
        
        return []