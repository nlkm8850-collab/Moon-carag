"""
Pemini Girl 9.5.2 - Version Switcher
"""

from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
import json
import time

class PeminiVersion(Enum):
    PRO_7_0 = "pemini_pro_7_0"
    GIRL_9_5_2 = "pemini_girl_9_5_2"

@dataclass
class VersionFeatures:
    name: str
    codename: str
    version_number: str
    description: str
    supported_languages: List[str]
    supported_code_languages: List[str]
    max_context_length: int
    supports_voice: bool
    supports_web_interface: bool
    supports_mobile: bool
    supports_collaboration: bool
    supports_advanced_analysis: bool
    supports_real_time: bool
    theme: str
    icon: str
    color_scheme: str

class VersionManager:
    VERSIONS = {
        PeminiVersion.PRO_7_0: VersionFeatures(
            name="Pemini Pro",
            codename="Classic",
            version_number="7.0",
            description="Classic version - Advanced code analysis tool",
            supported_languages=["ar", "en"],
            supported_code_languages=["python", "javascript", "java", "c", "cpp", "csharp", "php", "ruby"],
            max_context_length=2048,
            supports_voice=False,
            supports_web_interface=False,
            supports_mobile=False,
            supports_collaboration=False,
            supports_advanced_analysis=True,
            supports_real_time=False,
            theme="classic_dark",
            icon="🔧",
            color_scheme="blue_grey"
        ),
        PeminiVersion.GIRL_9_5_2: VersionFeatures(
            name="Pemini Girl",
            codename="Lumina",
            version_number="9.5.2",
            description="Advanced version - Trilingual AI assistant",
            supported_languages=["ar", "zh", "en"],
            supported_code_languages=[
                "python", "javascript", "typescript", "java", "c", "cpp", "csharp",
                "go", "rust", "ruby", "php", "swift", "kotlin", "dart", "r",
                "sql", "html", "css", "bash", "lua", "perl", "scala",
                "matlab", "assembly", "objective-c", "haskell", "elixir"
            ],
            max_context_length=8192,
            supports_voice=True,
            supports_web_interface=True,
            supports_mobile=True,
            supports_collaboration=True,
            supports_advanced_analysis=True,
            supports_real_time=True,
            theme="modern_dark",
            icon="🌟",
            color_scheme="purple_gold"
        )
    }

    def __init__(self, user_prefs_path: str = "version_prefs.json"):
        self.user_prefs_path = user_prefs_path
        self.current_version: PeminiVersion = PeminiVersion.GIRL_9_5_2
        self.user_settings: Dict = {}
        self.version_history: List[Dict] = []
        self.session_data: Dict = {}
        self._load_preferences()

    def _load_preferences(self):
        try:
            with open(self.user_prefs_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.user_settings = data.get("settings", {})
                self.version_history = data.get("history", [])
                saved_version = data.get("current_version", "pemini_girl_9_5_2")
                self.current_version = PeminiVersion(saved_version)
        except:
            self.current_version = PeminiVersion.GIRL_9_5_2

    def _save_preferences(self):
        data = {
            "current_version": self.current_version.value,
            "settings": self.user_settings,
            "history": self.version_history[-50:]
        }
        with open(self.user_prefs_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_current_version_info(self):
        return self.VERSIONS[self.current_version]

    def get_all_versions(self):
        return self.VERSIONS.copy()

    def switch_version(self, target_version: PeminiVersion, user_id: str = None):
        if target_version == self.current_version:
            return {"success": False, "message": "Already on this version"}

        previous_version = self.current_version
        previous_info = self.VERSIONS[previous_version]
        target_info = self.VERSIONS[target_version]

        self.session_data[previous_version.value] = {
            "timestamp": time.time(),
            "settings": self.user_settings.copy()
        }

        self.current_version = target_version

        history_entry = {
            "timestamp": time.time(),
            "from": previous_version.value,
            "to": target_version.value,
            "user_id": user_id
        }
        self.version_history.append(history_entry)

        if target_version.value in self.session_data:
            self.user_settings = self.session_data[target_version.value].get("settings", {}).copy()
        else:
            self.user_settings = {}

        self._save_preferences()

        notes = []
        if target_version == PeminiVersion.GIRL_9_5_2:
            notes.append("Added Chinese language support")
            notes.append(f"Increased code languages from {len(previous_info.supported_code_languages)} to {len(target_info.supported_code_languages)}")
            notes.append("Voice commands enabled")
            notes.append("Web interface available")
            notes.append("Mobile app support")
            notes.append("Real-time collaboration")
        else:
            notes.append("Classic mode - Advanced analysis tool")
            notes.append("Advanced code analysis available")

        return {
            "success": True,
            "message": f"Switched from {previous_info.name} to {target_info.name}!",
            "previous_version": {"id": previous_version.value, "name": previous_info.name},
            "current_version": {"id": target_version.value, "name": target_info.name},
            "migration_notes": notes
        }
