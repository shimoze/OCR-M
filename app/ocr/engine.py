from paddleocr import PaddleOCR

def init_ocr(lang='ru', use_orientation=True, show_log=False):
    return PaddleOCR(
        use_textline_orientation=use_orientation,
        lang=lang,
        show_log=show_log,
    )

def run_ocr(ocr, image):
    return ocr.ocr(image, cls=False)