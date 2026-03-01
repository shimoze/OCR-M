"""
import cv2
from ocr.engine import init_ocr, run_ocr
from ocr.postprocess import postprocess
from ocr.layout import sort_boxes, group_lines

from ocr.text.normalizer import TextNormalizer
from ocr.text.dictionary_loader import load_dictionary

from utils.paths import RAW_DIR, PROCESSED_DIR

#my_dict = load_dictionary("russian.txt")
#normalizer = TextNormalizer(dictionary=my_dict)

#Для навигации файла  
img_path = RAW_DIR / "test_image.jpg"

print("Файл существует:", img_path.exists())
if not img_path.exists():
    raise FileNotFoundError(f"Файл не найден: {img_path}")

img = cv2.imread(str(img_path))
if img is None:
    raise  ValueError(f"Не удалось прочитать изображение: {img_path}")

ocr = init_ocr()

print("Начинаю распознавание...")
results = run_ocr(ocr, img)

all_pairs = []

for page in results:
    for box, (text, score) in page:
        clean = postprocess(text, score, box, normalizer)
        if clean:
            all_pairs.append((box, clean))
    
pairs_sorted = sort_boxes(all_pairs)

lines = group_lines(pairs_sorted)

for line in lines:
    print(line)

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

output_file = PROCESSED_DIR / "output.txt"

#Вывод текста в файл
with open(output_file, "w", encoding="utf-8") as f:
    for line in lines:
        print(line, file=f)

"""
import cv2
import re


def smart_preprocess(image_path):
    """
    Адаптивная подготовка:
    - усиливает слабый контраст
    - минимально трогает чистые скрины
    """

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Не удалось прочитать изображение: {image_path}")

    # Проверка контраста (если уже хороший — почти не трогаем)
    std = img.std()

    if std < 40:  # низкий контраст → усиливаем
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img = clahe.apply(img)

    # Лёгкое шумоподавление (очень мягкое)
    img = cv2.medianBlur(img, 3)

    return img


def hard_postprocess(text):
    """
    Умеренная нормализация текста.
    Без агрессивного ломания латиницы.
    """

    # --- 1. Замена безопасных гомоглифов ---
    # Только те, которые 100% визуально идентичны
    safe_homoglyphs = {
        'A': 'А', 'a': 'а',
        'B': 'В',
        'E': 'Е', 'e': 'е',
        'K': 'К',
        'M': 'М',
        'H': 'Н',
        'O': 'О', 'o': 'о',
        'P': 'Р', 'p': 'р',
        'C': 'С', 'c': 'с',
        'T': 'Т',
        'X': 'Х', 'x': 'х',
        'y': 'у'
    }

    # Меняем только если текст в основном кириллица
    cyr_count = len(re.findall(r'[а-яА-Я]', text))
    lat_count = len(re.findall(r'[a-zA-Z]', text))

    if cyr_count > lat_count:
        for bad, good in safe_homoglyphs.items():
            text = text.replace(bad, good)

    # --- 2. Исправление частой ошибки Paddle: Н вместо И в конце ---
    text = re.sub(r'([а-яА-Я]+)[нН]\b', r'\1и', text)

    # --- 3. Чистка пробелов ---
    text = re.sub(r'\s+', ' ', text).strip()

    # --- 4. Аккуратная нормализация регистра ---
    # НЕ убиваем весь регистр.
    # Только если текст полностью хаотичный (больше 60% заглавных)

    upper_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)

    if upper_ratio > 0.6:
        text = text.lower()
        sentences = re.split(r'([.!?]\s*)', text)
        text = ''.join(
            s.capitalize() if i % 2 == 0 else s
            for i, s in enumerate(sentences)
        )

    return text


# --- ПРИМЕР ---
raw_text = "полНтчЕСкНх Н правовых ин СТитуТОВ... СМbСЛ... SКОНОМIКу"

final_text = hard_postprocess(raw_text)

print(final_text)