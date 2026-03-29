import cv2

from app.ocr import engine
from app.ocr.pipeline import OCRPipeline
from app.ocr.postprocess import postprocess
from app.ocr.layout import sort_boxes, group_lines

from app.text.normalizer import TextNormalizer

from app.utils.paths import RAW_DIR, PROCESSED_DIR
from app.utils.structures import OCRWord

# путь к изображению
img_path = RAW_DIR / "test_image.jpg"

if not img_path.exists():
    raise FileNotFoundError(f"Файл не найден: {img_path}")

img = cv2.imread(str(img_path))

ocr = engine.init_ocr('paddle')
pipeline = OCRPipeline(ocr=ocr)

text = pipeline.run(img)

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
output_file = PROCESSED_DIR / "output.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for line in text:
        f.write(line.text + "\n")
