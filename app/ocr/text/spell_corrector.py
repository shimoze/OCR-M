# spell_corrector.py
from symspellpy import SymSpell, Verbosity

class SpellCorrector:
    def __init__(self, dictionary: set[str], max_edit_distance=2):
        # Создаём объект SymSpell
        self.spell = SymSpell(max_dictionary_edit_distance=max_edit_distance, prefix_length=7)

        # Сохраняем словарь в нижнем регистре для быстрой проверки "уже верное слово"
        self.dictionary = {word.lower() for word in dictionary}

        # Загружаем слова в SymSpell
        # SymSpell требует метод create_dictionary_entry(word, count) по одному слову
        for word in self.dictionary:
            self.spell.create_dictionary_entry(word, 1)

    def correct_word(self, word: str) -> str:
        word_lower = word.lower()

        # 1. Если слово уже верное
        if word_lower in self.dictionary:
            return word

        # 2. Если слово слишком короткое
        if len(word) <= 2:
            return word

        # 3. Исправление через SymSpell
        suggestions = self.spell.lookup(word_lower, Verbosity.CLOSEST, max_edit_distance=2)

        if suggestions:
            # Возвращаем первый лучший вариант, сохраняя регистр исходного слова
            corrected = suggestions[0].term
            if word[0].isupper():
                corrected = corrected.capitalize()
            return corrected
        else:
            return word