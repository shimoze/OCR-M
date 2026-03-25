import cv2

def soft_preprocess(img, clip_limit=2.0, denoise_strength=10):

    # 1. Перевод в ч/б
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. CLAHE
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)

    # 3. Denoise
    denoised = cv2.fastNlMeansDenoising(enhanced, None, denoise_strength, 7, 21)

    # PaddleOCR ждёт 3 канала
    return cv2.cvtColor(denoised, cv2.COLOR_GRAY2BGR)