import re
from .char_map import LATIN_TO_CYRILLIC
from .spell_corrector import SpellCorrector

class TextNormalizer:
    def __init__(self, dictionary: set[str] | None = None):
        self.dictionary = dictionary
        self.corrector = SpellCorrector(dictionary) if dictionary else None

    def process(self, text: str) -> str:
        text = self._normalize_chars(text)
        text = self._fix_line_breaks(text)
        text = self._normalize_spaces(text)
        text = self._correct_spelling(text)
        return text
    
    # 1. Замена латиницы
    def _normalize_chars(self, text:str) -> str:
        return "".join(LATIN_TO_CYRILLIC.get(ch, ch) for ch in text)
    
    # 2. Склейка переносов
    def _fix_line_breaks(self, text: str) -> str:
        text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
        text = text.replace("\n", " ")
        return text
    
    # 3. Удаление лишних пробелов
    def _normalize_spaces(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()
    
    # 4. Исправление слов
    def _correct_spelling(self, text: str) -> str:
        if not self.corrector:
            return text
        
        words = text.split()
        corrected = [self.corrector.correct_word(w) for w in words]
        return " ".join(corrected)