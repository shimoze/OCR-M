from app.utils.paths import MODELS_OCR

USE_GPU= False

#models

det_model_dir= str(MODELS_OCR / "v4" / "det" / "mobile")
rec_model_dir= str(MODELS_OCR / "v4" / "rec" / "mobile" / "ru")
