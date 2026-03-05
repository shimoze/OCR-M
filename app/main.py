import cv2
from ocr.engine import init_ocr, run_ocr
from ocr.postprocess import postprocess
from ocr.layout import sort_boxes, group_lines

from text.normalizer import TextNormalizer
from text.dictionary_loader import load_dictionary

from utils.paths import RAW_DIR, PROCESSED_DIR

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
normalizer = TextNormalizer()
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

