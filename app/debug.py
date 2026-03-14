import cv2
from datetime import datetime

from utils.visualization import OCRVisualizer
from utils.paths import DEBUG_DIR, RAW_DIR
from utils.logger import OCRLogger

from ocr.engine import init_ocr, run_ocr
from ocr.layout import sort_boxes, group_lines
from ocr.postprocess import postprocess
from ocr.preprocessing import soft_preprocess

"""
    Подготовка папки
"""

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
run_dir = DEBUG_DIR / timestamp
run_dir.mkdir(parents=True, exist_ok=True)

steps_dir = run_dir / "steps_dir"
steps_dir.mkdir(parents=True, exist_ok=True)

"""
    Реализация логгера 
"""
img_path = RAW_DIR / "test_image.jpg"

img = cv2.imread(str(img_path))

logger = OCRLogger(run_dir, total_steps=6)
logger.setup()

with logger.log_step("preprocess"):
    img = soft_preprocess(img)

with logger.log_step("init ocr"):
    ocr = init_ocr()

with logger.log_step("run ocr"):
    items = run_ocr(ocr, img)

with logger.log_step("sort boxes"):
    items = sort_boxes(items)

with logger.log_step("group lines"):
    lines = group_lines(items)

with logger.log_step("postprocess"):
    text = postprocess(lines)

"""Часть с визуализатором"""
viz = OCRVisualizer(steps_dir)

img = cv2.imread(RAW_DIR / "test_image.jpg")
viz.save("original", img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
viz.save("gray", gray)

denoise = cv2.fastNlMeansDenoising(gray, h=10)
viz.save("denoise", denoise)

_, thresh = cv2.threshold(denoise, 127, 255, cv2.THRESH_BINARY)
viz.save("threshold", thresh)

# пример морфологии
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
viz.save("morph", morph)

# пример boxes
boxes = [[50,50,150,100], [200,80,300,130]]  # пример bbox
viz.save_boxes(morph, boxes)

# показать grid
viz.show_grid(cols=3)

