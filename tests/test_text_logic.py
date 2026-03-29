from app.text.normalizer import TextNormalizer
from app.text.spell_corrector import SpellCorrector
from app.utils.structures import OCRLine
from app.utils.paths import TEST_DIR

def test_text_normalizer():
    raw_text = OCRLine(words=[], 
                       text="Пример  текста \n с     ошибками",
                       score=1.0,
                       box=[],
                       )
    excepted = "Пример текста с ошибками"

    normalizer = TextNormalizer()
    raw_text = normalizer.process_line(raw_text)
    
    if(raw_text == excepted):
        print("Test SUCCESS")
    else:
        print("Test FAILED")

def test_spell_corrector():
    bad_text = "Договор купли-прадажи"
    right_word = "продажи"

    dict_path = TEST_DIR / "test_dictionary" / "russian_test.txt"

    with open(dict_path, 'r', encoding='ANSI') as f:
        words = set(f.read().splitlines())

    spell = SpellCorrector(words)
    result = spell.correct_word(bad_text)


    if right_word in result.lower():
        print("TEST SUCCESS")
    else:
        print("TEST FAILED")
