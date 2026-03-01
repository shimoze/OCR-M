import cv2
import numpy as np

def soft_preprocess(img_path, clip_limit=2.0, denoise_strength=10):
    img = cv2.imread(img_path)
    # 1. Перевод в ч/б (но оставляем 256 оттенков серого)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. CLAHE (Contrast Limited Adaptive Histogram Equalization)
    # Это "умное" повышение контраста: оно не выжигает пиксели, а делает текст четче
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # 3. Де noise (убираем мелкую "соль-перец", не размывая буквы)
    denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
    
    # Возвращаем 3 канала, как хочет Paddle
    return cv2.cvtColor(denoised, cv2.COLOR_GRAY2BGR)