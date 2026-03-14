import logging
import time
from datetime import datetime
from contextlib import contextmanager


class OCRLogger:
    def __init__(self, log_dir, total_steps):
        self.log_dir = log_dir
        self.total_steps = total_steps
        self.step_counter = 0
        self.logger = None
        self.setup()

    def setup(self):
        self.log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = self.log_dir / f"ocr_{timestamp}.log"

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

        self.logger = logger

    @contextmanager
    def log_step(self, name: str):

        self.step_counter += 1
        start = time.perf_counter()

        yield

        elapsed = (time.perf_counter() - start) * 1000
        dots = "." * max(1, 20 - len(name))

        self.logger.info(
            "[%d/%d] %s %s %.0f ms",
            self.step_counter,
            self.total_steps,
            name,
            dots,
            elapsed,
        )
