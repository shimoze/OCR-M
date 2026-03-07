import logging
import time
from datetime import datetime
from contextlib import contextmanager
from .paths import LOG_DIR

_step_counter = 0
_total_steps = 0


def setup_logger(total_steps: int):
    global _step_counter, _total_steps

    LOG_DIR.mkdir(exist_ok=True)

    _step_counter = 0
    _total_steps = total_steps

    # уникальное имя файла
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = LOG_DIR / f"ocr_{timestamp}.log"

    logger = logging.getLogger("pipeline")
    logger.setLevel(logging.INFO)

    logger.handlers.clear()
    logger.propagate = False

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(message)s")

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


@contextmanager
def log_step(name: str):
    global _step_counter

    logger = logging.getLogger("pipeline")

    _step_counter += 1
    start = time.perf_counter()

    yield

    elapsed = (time.perf_counter() - start) * 1000
    dots = "." * max(1, 20 - len(name))

    logger.info(
        "[%d/%d] %s %s %.0f ms",
        _step_counter,
        _total_steps,
        name,
        dots,
        elapsed,
    )