# Import only the necessary interfaces and base classes first
from mechanics.interfaces import (
    Trademark, Edge, Flaw, Drive, Item, 
    CharacterInterface, DiceResult, DiceSystemInterface
)
from data.data_interfaces import DatabaseInterface
from .data.session_handler import SessionHandler
from .data.config_handler import ConfigHandler
from .terminal_ui import TerminalUI
from .llm_interface import LLMInterface
from .character.manager import CharacterManager
from .template_manager import TemplateManager
from .gear_manager import GearManager
from .character_llm_integration import CharacterLLMIntegration
from .character_creation import CharacterCreation
from .nco_dice_system import NCODiceSystem
from .check_manager import CheckManager
from .game_state_manager import GameStateManager
from .character_creation_ui import CharacterCreationUI
from .character_display import CharacterDisplay

# Then define what should be exported
__all__ = [
    'Trademark', 'Edge', 'Flaw', 'Drive', 'Item', 'CharacterInterface', 
    'DiceResult', 'DiceSystemInterface', 'DatabaseInterface',
    'SessionHandler',
    # Add other classes you want to export here
]

# Optionally, you can conditionally import the implementations,
# but this is cleaner to manage in each file that needs these classes