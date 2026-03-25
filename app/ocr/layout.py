import statistics
from app.utils.structures import OCRLine, OCRWord

def box_height(box):
    ys = [p[1] for p in box]
    return max(ys) - min(ys)

def median_text_height(words):
    heights = [box_height(w.box) for w in words]
    return statistics.median(heights)

def sort_boxes(words):
    def box_key(w):
        y = min(p[1] for p in w.box)
        x = min(p[0] for p in w.box)
        return (y, x)
    return sorted(words, key=box_key)

def group_lines(words: list[OCRWord]) -> list[OCRLine]:
    """
    Группирует OCRWord в OCRLine
    """
    if not words:
        return []

    # сортируем по центру Y
    words.sort(key=lambda w: (min(p[1] for p in w.box) + max(p[1] for p in w.box)) / 2)
    median_h = median_text_height(words)
    y_threshold = int(median_h * 0.5)

    lines = []
    current_line = []
    current_y_center = (min(p[1] for p in words[0].box) + max(p[1] for p in words[0].box)) / 2

    for word in words:
        word_y_center = (min(p[1] for p in word.box) + max(p[1] for p in word.box)) / 2

        if abs(word_y_center - current_y_center) <= y_threshold:
            current_line.append(word)
        else:
            # сортируем слова по X
            current_line.sort(key=lambda w: min(p[0] for p in w.box))

            line_text = " ".join(w.text for w in current_line)
            line_score = sum(w.score for w in current_line) / len(current_line)
            line_box = [p for w in current_line for p in w.box]

            lines.append(
                OCRLine(
                    text=line_text,
                    score=line_score,
                    box=line_box,
                    words=current_line.copy(),  # сохраняем слова в линии
                )
            )

            current_line = [word]
            current_y_center = word_y_center

    # последняя линия
    if current_line:
        current_line.sort(key=lambda w: min(p[0] for p in w.box))
        line_text = " ".join(w.text for w in current_line)
        line_score = sum(w.score for w in current_line) / len(current_line)
        line_box = [p for w in current_line for p in w.box]
        lines.append(
            OCRLine(
                text=line_text,
                score=line_score,
                box=line_box,
                words=current_line.copy(),
            )
        )

    return lines

def group_paragraphs(lines, line_spacing_threshold=20):
    """
    lines: List[OCRLine]
    Возвращает List[str] — текст абзацев
    """
    paragraphs = []
    paragraph = []

    for line in lines:
        if not line.text.strip():
            if paragraph:
                paragraphs.append(" ".join(paragraph))
                paragraph = []
        else:
            paragraph.append(line.text)
    if paragraph:
        paragraphs.append(" ".join(paragraph))
    
    return paragraphs