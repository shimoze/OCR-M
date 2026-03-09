from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
APP_DIR = BASE_DIR / "app"
LOG_DIR = BASE_DIR / "logs"

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "input"
PROCESSED_DIR = DATA_DIR / "output"

DEBUG_DIR = BASE_DIR / "debug" / "ocr_steps"

OCR_DIR = APP_DIR / "ocr"
DICT_DIR = OCR_DIR / "text" / "dictionary"
