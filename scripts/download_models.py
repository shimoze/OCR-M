import os
import sys
from paddleocr import PaddleOCR

from app.utils.paths import BASE_DIR
from scripts.model_config import MODELS_CONFIG


def resolve_model_config(cfg):
    version = cfg["version"]
    model_type = cfg["type"]
    lang = cfg["lang"]

    model_block = MODELS_CONFIG[version][model_type]

    det_lang = model_block["det"]["default"]

    rec_lang_map = model_block["rec"]
    rec_lang = rec_lang_map.get(lang, "ch")  # fallback

    return {
        "det_lang": det_lang,
        "rec_lang": rec_lang
    }
            
def build_paths(cfg, lang):
    base = BASE_DIR / "models" / "paddleocr" / "ocr"
    version = cfg["version"]
    model_type = cfg["type"]

    return {
        "det_dir": f"{base}/{version}/det/{model_type}",
        "rec_dir": f"{base}/{version}/rec/{model_type}/{lang}",
    }

def create_ocr(cfg):
    resolved = resolve_model_config(cfg)
    paths = build_paths(cfg, resolved["rec_lang"])

    ocr = PaddleOCR(
        lang=resolved["rec_lang"],   # ключевой момент
        det_model_dir=paths["det_dir"],
        rec_model_dir=paths["rec_dir"],
        use_gpu=False,
        show_log= False,
    )

    return ocr


def process_single_config(ver, t, l):
    """Вспомогательная функция, чтобы не дублировать код"""
    cfg = {"version": ver, "type": t, "lang": l}
    resolved = resolve_model_config(cfg)
    paths = build_paths(cfg, resolved["rec_lang"])

    if os.path.exists(paths["rec_dir"]):
        print(f"SKIPPING: Модель для {l} уже скачана в {paths['rec_dir']}")
        return

    print(f"DOWNLOADING: {ver} | {t} | {l}...")
    
    try:
        create_ocr(cfg)
        print(f"SUCCESS: {l} готов.")
    except Exception as e:
        print(f"ERROR: Не удалось загрузить {l}: {e}")

def main():
    
    if len(sys.argv) < 2:
        print("Использования: python -m scripts.download_models <version> <type> <language>")
        return

    mode = sys.argv[1]

    if mode == 'all':
        for version, types in MODELS_CONFIG.items():
            for m_type, components in types.items():
                for lang in components["rec"].keys():
                    process_single_config(version, m_type, lang)

    elif len(sys.argv) >= 4:
        ver, t, l = sys.argv[1], sys.argv[2], sys.argv[3]

        try:
            if l in MODELS_CONFIG[ver][t]["rec"]:
                process_single_config(ver, t, l)
            else:
                print(f"Язык {l} не найден в {ver}/{t}")
        except KeyError:
            print(f"Ошибка: Комбинация {ver}/{t} не найдена в конфиге.")
    else:
        print("Недостаточно аргументов для запуска.")

if __name__ == "__main__":
    main()
