import statistics

#Измеряем высоту бокса
def box_height(box):
    ys = [p[1] for p in box]
    return max(ys) - min(ys)

#Средняя высота строки
def median_text_height(boxes):
    heights = [box_height(box) for box, _ in boxes]
    return statistics.median(heights)

def sort_boxes(boxes):
    """
    boxes: list of (box, text)
    box: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
    """
    def box_key(item):
        box, _ = item
        y = min(p[1] for p in box)
        x = min(p[0] for p in box)
        return (y, x)

    return sorted(boxes, key=box_key)

def group_lines(boxes):
    """
    boxes: list of (box, text), уже отсортированы по y
    Возвращает список строк (каждая строка — объединённый текст)
    """
    if not boxes:
        return []

    median_h = median_text_height(boxes)
    y_threshold = int(median_h * 0.6)

    lines = []
    current = []

    for box, text in boxes:
        y_top = min(p[1] for p in box)
        
        if not current:
            current = [(box, text)]
            current_y = y_top
            continue

        if abs(y_top - current_y) <= y_threshold:
            current.append((box, text))
        else:
            current_sorted = sorted(
                current,
                key=lambda it: min(p[0] for p in it[0])
            )

            lines.append(" ".join(t for _, t in current_sorted))
            current = [(box, text)]
            current_y = y_top

    if current:
        current_sorted = sorted(
            current,
            key = lambda it: min(p[0] for p in it[0])
        )
        lines.append(" ".join(t for _, t in current_sorted))        

    return lines

def group_paragraphs(lines, line_spacing_threshold=20):
    """
    lines: список строк
    Возвращает список абзацев
    """
    paragraphs = []
    paragraph = []

    for line in lines:
        if line.strip() == "":
            if paragraph:
                paragraphs.append(" ".join(paragraph))
                paragraph = []
        else:
            paragraph.append(line)
    if paragraph:
        paragraphs.append(" ".join(paragraph))
    
    return paragraphs