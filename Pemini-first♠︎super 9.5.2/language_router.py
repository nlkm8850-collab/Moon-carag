"""
Pemini Girl 9.5.2 - Language Router
"""

import re
from typing import Tuple, Optional
from enum import Enum

class Language(Enum):
    ARABIC = "ar"
    CHINESE = "zh"
    ENGLISH = "en"
    MIXED = "mixed"
    UNKNOWN = "unknown"

class LanguageRouter:
    ARABIC_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F]')
    CHINESE_PATTERN = re.compile(r'[\u4E00-\u9FFF\u3400-\u4DBF]')
    ENGLISH_PATTERN = re.compile(r'[a-zA-Z]')

    def detect_language(self, text: str):
        if not text or not text.strip():
            return Language.UNKNOWN, 0.0
        text = text.strip()
        arabic_count = len(self.ARABIC_PATTERN.findall(text))
        chinese_count = len(self.CHINESE_PATTERN.findall(text))
        english_count = len(self.ENGLISH_PATTERN.findall(text))
        total_chars = len(text.replace(' ', '').replace('\n', ''))
        if total_chars == 0:
            return Language.UNKNOWN, 0.0
        scores = {Language.ARABIC: arabic_count/total_chars,
                  Language.CHINESE: chinese_count/total_chars,
                  Language.ENGLISH: english_count/total_chars}
        max_lang = max(scores, key=scores.get)
        return max_lang, min(scores[max_lang] * 2, 1.0)

    def is_code_request(self, text: str):
        indicators = ['code', 'python', 'function', 'write', 'create', 'generate']
        return any(ind in text.lower() for ind in indicators)
