import cv2
import logging

from ocr.engine import init_ocr, run_ocr
from ocr.postprocess import postprocess
from ocr.layout import sort_boxes, group_lines

from text.normalizer import TextNormalizer

from utils.paths import RAW_DIR, PROCESSED_DIR
from utils.logger import setup_logger, log_step

setup_logger(total_steps=6)

# путь к изображению
img_path = RAW_DIR / "test_image.jpg"

if not img_path.exists():
    raise FileNotFoundError(f"Файл не найден: {img_path}")


with log_step("load image"):
    img = cv2.imread(str(img_path))

if img is None:
    raise ValueError(f"Не удалось прочитать изображение: {img_path}")


with log_step("init ocr"):
    ocr = init_ocr()


with log_step("run_ocr"):
    results = run_ocr(ocr, img)


with log_step("postprocess"):
    all_pairs = []
    normalizer = TextNormalizer()

    for page in results:
        for box, (text, score) in page:
            clean = postprocess(text, score, box, normalizer)
            if clean:
                all_pairs.append((box, clean))


with log_step("layout"):
    pairs_sorted = sort_boxes(all_pairs)
    lines = group_lines(pairs_sorted)


with log_step("save result"):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_file = PROCESSED_DIR / "output.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        for line in lines:
            print(line, file=f)

