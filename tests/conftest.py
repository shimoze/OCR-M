import pytest
from app.ocr import engine

@pytest.fixture(scope="session")
def loaded_ocr_engine():
    print("\nЗагрузка моделей для тестов...")
    return engine.init_ocr('paddle')