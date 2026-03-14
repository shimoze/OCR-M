import statistics

#Измеряем высоту бокса
def box_height(box):
    ys = [p[1] for p in box]
    return max(ys) - min(ys)

#Средняя высота строки
def median_text_height(boxes):
    heights = [box_height(box) for box, _, _ in boxes]
    return statistics.median(heights)

def sort_boxes(boxes):
    """
    boxes: list of (box, text)
    box: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
    """
    def box_key(item):
        box, _, _ = item
        y = min(p[1] for p in box)
        x = min(p[0] for p in box)
        return (y, x)

    return sorted(boxes, key=box_key)

def group_lines(boxes):
    if not boxes:
        return []

    # Сортируем все боксы сначала по Y (центру), чтобы идти сверху вниз
    boxes.sort(key=lambda b: (min(p[1] for p in b[0]) + max(p[1] for p in b[0])) / 2)

    median_h = median_text_height(boxes)
    y_threshold = int(median_h * 0.5) # Немного уменьшим порог для точности

    lines = []
    current_line = []

    first_box = boxes[0][0]
    current_y_center = (min(p[1] for p in first_box) + max(p[1] for p in first_box)) / 2

    for box, text, score in boxes:

        box_y_center = (min(p[1] for p in box) + max(p[1] for p in box)) / 2

        if abs(box_y_center - current_y_center) <= y_threshold:
            current_line.append((box, text, score))
        else:

            current_line.sort(key=lambda b: min(p[0] for p in b[0]))

            line_text = " ".join(t for _, t, _ in current_line)
            line_score = sum(s for _, _, s in current_line) / len(current_line)
            line_box = [p for box, _, _ in current_line for p in box]

            lines.append({
                "text": line_text,
                "score":line_score,
                "box": line_box,
            })

            current_line = [(box, text, score)]
            current_y_center = box_y_center

    if current_line:
        current_line.sort(key=lambda b: min(p[0] for p in b[0]))

        line_text =" ".join(t for _, t, _ in current_line)
        line_score = sum(s for _, _, s in current_line) / len(current_line)
        line_box = [p for box, _, _ in current_line for p in box]

        lines.append({
            "text": line_text,
            "score": line_score,
            "box": line_box
        })

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