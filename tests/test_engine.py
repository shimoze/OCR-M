import os
from app.ocr import engine

def test_engine_loads_local_models():
    try:
        ocr = engine.init_ocr('paddle')
        assert ocr is not None
        print("TEST SUCCESS")
    except Exception as e:
        assert False, f"Движок не загрузился из-за ошибки: {e}"