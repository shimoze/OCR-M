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

    if("гарантировать" in result_string):test_score+=1
    if("контроль" in result_string.lower()):test_score+=1
    if("OCR" in result_string.upper()):test_score+=1

    if(len(result_text) > 10):test_score+=1

    if(test_score>=3):
        print("TEST SUCCESS")
    else:
        print("TEST FAILED") 