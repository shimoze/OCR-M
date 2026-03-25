from dataclasses import dataclass
from typing import List, Tuple

Point = Tuple[int, int]

@dataclass
class OCRWord:
    text: str
    score:float
    box: List[Point]

@dataclass
class OCRLine:
    words: List[OCRWord]
    text: str
    score: float
    box: List[Point]

@dataclass
class OCRBlock:
    lines: List[OCRLine]
    box: List[Point]

@dataclass
class OCRPage:
    blocks: List[OCRBlock]
    width: int
    height: int