import cv2
from datetime import datetime

from app.utils.visualization import OCRVisualizer
from app.utils.paths import DEBUG_DIR, RAW_DIR
from app.utils.logger import OCRLogger

from app.ocr import engine
from app.ocr.pipeline import OCRPipeline

"""
    Подготовка директории
"""

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
run_dir = DEBUG_DIR / timestamp
run_dir.mkdir(parents=True, exist_ok=True)

steps_dir = run_dir / "steps_dir"
steps_dir.mkdir(parents=True, exist_ok=True)

#    ---Загрузка изображения---

img_path = RAW_DIR / "test_image.jpg"
img = cv2.imread(str(img_path))

if img is None:
    raise ValueError(f"Не удалось прочитать изображение: {img_path}")

#   ---инициализация---

logger = OCRLogger(run_dir, total_steps=6)
logger.setup()

ocr = engine.init_ocr('paddle')
pipeline = OCRPipeline(ocr=ocr)

img_original=img

#   ---pipeline с контролем---
with logger.log_step("preprocess"):
    img = pipeline.preprocess(img)
    img_pre=img

with logger.log_step("run ocr"):
    items = pipeline.run_ocr(img)

with logger.log_step("to words"):
    words = pipeline.to_words(items)

with logger.log_step("sort boxes"):
    words = pipeline.sort(words)

with logger.log_step("group lines"):
    lines = pipeline.group(words)

with logger.log_step("postprocess"):
    text = pipeline.postprocess(lines)

# --- визуализация bbox (реальная, не фейковая) ---

viz = OCRVisualizer(steps_dir)
viz.save_pipeline_steps(original=img_original, preprocessed=img_pre, words=words, lines=lines)


viz.show_grid(cols=3)