from paddleocr import PaddleOCR
from .preprocessing import soft_preprocess

def init_ocr(lang='cyrillic', use_orientation=True, show_log=False):
    return PaddleOCR(
        use_angle_cls = use_orientation,
        lang=lang,
        show_log=show_log,
        rec_batch_num=16,
        det_db_thresh=0.3,
        det_db_box_thresh=0.5,
        use_gpu= False,
    )

def run_ocr(ocr, image, preprocess=True):
    if isinstance(image, str) and preprocess:
        img = soft_preprocess(image)
    else:
        img = image
    
    return ocr.ocr(image, cls=False)