"""
Pemini Girl 9.5.2 - Lumina
Trilingual AI Code Assistant
"""

__version__ = "9.5.2"
__codename__ = "Lumina"
__author__ = "Moon-carag Team"
__license__ = "MIT"

from .config import MODEL_CONFIG, PERFORMANCE_CONFIG, API_CONFIG
from .auth_system import AuthenticationManager, UserRole, AuthProvider, UserProfile
from .version_switcher import VersionManager, PeminiVersion, VersionFeatures
from .code_engine import CodeIntelligenceEngine, CodeResult, TaskType
from .language_router import LanguageRouter, Language
from .llm_integration import LLMIntegrationEngine, LLMProvider, GenerationConfig, GenerationResult
from .database_manager import DatabaseManager
from .main import PeminiGirlLauncher
