import cv2

from app.ocr.engine import init_ocr, run_ocr
from app.ocr.postprocess import postprocess
from app.ocr.layout import sort_boxes, group_lines

from app.text.normalizer import TextNormalizer

from app.utils.paths import RAW_DIR, PROCESSED_DIR

# путь к изображению
img_path = RAW_DIR / "test_image.jpg"

if not img_path.exists():
    raise FileNotFoundError(f"Файл не найден: {img_path}")

img = cv2.imread(str(img_path))

if img is None:
    raise ValueError(f"Не удалось прочитать изображение: {img_path}")


ocr = init_ocr()

results = run_ocr(ocr, img)


normalizer = TextNormalizer()
all_pairs = []

for page in results:
    for box, (text, score) in page:
        clean = postprocess(text, score, box, normalizer)
        if clean:
            all_pairs.append((box, clean))


pairs_sorted = sort_boxes(all_pairs)
lines = group_lines(pairs_sorted)

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
output_file = PROCESSED_DIR / "output.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for line in lines:
        print(line, file=f)

