from abc import ABC, abstractmethod
from paddleocr import PaddleOCR

from app.config import USE_GPU, det_model_dir, rec_model_dir
from app.ocr.preprocessing import soft_preprocess

# --- 1. Базовый интерфейс ---
class BaseOCREngine(ABC):
    @abstractmethod
    def run(self, image, preprocess=True):
        pass

# --- 2. PaddleOCR для обычного текста ---

class PaddleEngine(BaseOCREngine):
    def __init__(self, use_orientation=True, show_log=False):
        self.engine = PaddleOCR(
            det_model_dir=det_model_dir,
            rec_model_dir=rec_model_dir,
            lang="ru",
            use_angle_cls=use_orientation,
            show_log=show_log,
            rec_batch_num=16,
            det_db_thresh=0.3,            
            det_db_box_thresh=0.5,
            use_gpu=USE_GPU,
        )

    def run(self, image, preprocess=True):
        if isinstance(image, str) and preprocess:
            img = soft_preprocess(image)
        else:
            img = image
        
        result = self.engine.ocr(img, cls=False)
        if not result or not result[0]:
            return

        items = []

        for item in result[0]:
            box = item[0]
            text = item[1][0]
            score = item[1][1]

            items.append((box, (text , score)))

        return items
    
def init_ocr(engine_type='paddle', **kwargs):
    engines = {
        'paddle':PaddleEngine,
        #'paddle-vl':PaddleVLEngine,
    }
    engine_cls = engines.get(engine_type.lower())
    if not engine_cls:
        raise ValueError(f"Unknown OCR engine: {engine_type}")
    
    return engine_cls(**kwargs)