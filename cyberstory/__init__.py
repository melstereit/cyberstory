# Import only the necessary interfaces and base classes first
from mechanics.interfaces import (
    Trademark, Edge, Flaw, Drive, Item, 
    CharacterInterface, DiceResult, DiceSystemInterface
)
from .data.data_interfaces import DatabaseInterface
from .data.session_handler import SessionHandler
from .data.config_handler import ConfigHandler
from .ui.terminal import TerminalUI
from .ai.llm_interface import LLMInterface
from .character.manager import CharacterManager
from .character.templates import TemplateManager
from .character.gear_manager import GearManager
from .character.llm_integration import CharacterLLMIntegration
from .character.creation import CharacterCreation
from .mechanics.nco_dice_system import NCODiceSystem
from .mechanics.check_manager import CheckManager
from .data.game_state import GameStateManager
from .ui.character_creation_ui import CharacterCreationUI
from .ui.character_display import CharacterDisplay

# Then define what should be exported
__all__ = [
    'Trademark', 'Edge', 'Flaw', 'Drive', 'Item', 'CharacterInterface', 
    'DiceResult', 'DiceSystemInterface', 'DatabaseInterface',
    'SessionHandler', 'ConfigHandler', 'TerminalUI', 'LLMInterface',
    'CharacterManager', 'TemplateManager', 'GearManager',
    'CharacterLLMIntegration', 'CharacterCreation', 'NCODiceSystem',
    'CheckManager', 'GameStateManager', 'CharacterCreationUI', 'CharacterDisplay'
]

# Optionally, you can conditionally import the implementations,
# but this is cleaner to manage in each file that needs these classes