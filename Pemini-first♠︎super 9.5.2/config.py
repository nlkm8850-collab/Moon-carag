"""
Pemini Girl 9.5.2 - Configuration
"""

from dataclasses import dataclass
from typing import List

@dataclass
class ModelConfig:
    name: str = "Pemini-Girl-9.5.2"
    codename: str = "Lumina"
    version: str = "9.5.2"
    max_tokens: int = 4096
    temperature: float = 0.3
    top_p: float = 0.95
    top_k: int = 50
    use_cache: bool = True
    cache_size: int = 1000
    streaming: bool = True

    def __post_init__(self):
        self.supported_natural_languages = ["ar", "zh", "en"]
        self.supported_programming_languages = [
            "python", "javascript", "typescript", "java", "c", "cpp", "csharp",
            "go", "rust", "ruby", "php", "swift", "kotlin", "dart", "r",
            "sql", "html", "css", "bash", "lua", "perl", "scala",
            "matlab", "assembly", "objective-c", "haskell", "elixir"
        ]

@dataclass
class PerformanceConfig:
    target_latency_short_ms: int = 500
    target_latency_medium_ms: int = 2000
    target_latency_large_ms: int = 5000
    target_tokens_per_second: int = 120
    target_syntax_accuracy: float = 0.98
    target_logic_accuracy: float = 0.92
    target_language_detection: float = 0.99
    target_translation_accuracy: float = 0.95

@dataclass
class APIConfig:
    host: str = "0.0.0.0"
    port: int = 8080
    workers: int = 4
    max_request_size: int = 10 * 1024 * 1024
    timeout: int = 60
    rate_limit_requests: int = 100
    rate_limit_window: int = 60

MODEL_CONFIG = ModelConfig()
PERFORMANCE_CONFIG = PerformanceConfig()
API_CONFIG = APIConfig()
