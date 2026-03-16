from dataclasses import dataclass
from typing import List, Tuple

Point = Tuple[int, int]

@dataclass
class OCRLine:
    text: str
    score: float
    box: List[Point]