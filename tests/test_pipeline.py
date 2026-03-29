import os 
import cv2

from app.ocr.pipeline import OCRPipeline
from app.ocr import engine

def test_full_pipeline():
    test_score=0
    image_path = os.path.join("tests", "test_data", "test_image.jpg")
    image = cv2.imread(image_path)

    assert image is not None, "test image is not found"

    ocr = engine.init_ocr('paddle')
    pipeline = OCRPipeline(ocr=ocr)

    result_text = pipeline.run(image)
    result_string = str(result_text).lower()

    if "гарантировать" in result_string:
        test_score += 1
    if "контроль" in result_string:
        test_score += 1
    if "ocr" in result_string:
        test_score += 1
    if len(result_string.strip()) > 0:
        test_score += 1

    assert test_score >= 3, f"OCR quality too low: score={test_score}, text={result_string}"