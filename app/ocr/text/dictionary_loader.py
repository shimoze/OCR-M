from utils.paths import APP_DIR

def load_dictionary(filename):
    path = APP_DIR / "ocr" / "text" / "dictionary" / filename

    with open(path, encoding="ANSI") as f:
        return set(
            word.strip().lower()
            for word in f
            if word.strip()
        )