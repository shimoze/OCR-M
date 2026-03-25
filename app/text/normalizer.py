import re
from app.text.char_map import LATIN_TO_CYRILLIC
from app.text.spell_corrector import SpellCorrector
from app.utils.structures import OCRLine, OCRWord

class TextNormalizer:
    def __init__(self, dictionary: set[str] | None = None, correct_spelling= False):
        self.dictionary = dictionary
        self.corrector = SpellCorrector(dictionary) if dictionary and correct_spelling else None

    def process_line(self, line: OCRLine) -> OCRLine:
        text = self._normalize_chars(line.text)
        text = self._fix_line_breaks(text)
        text = self._normalize_spaces(text)
        
        words = []
    
        for word in line.words:
            w_text = self._normalize_chars(word.text)
            if self.corrector:
                w_text = self.corrector.correct_word(w_text)
            words.append(OCRWord(
                text=w_text,
                score=word.score,
                box=word.box,
            ))

        return OCRLine(
            text=text,
            score=line.score,
            box=line.box,
            words=words,
        )


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
    
