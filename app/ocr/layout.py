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
    if not boxes:
        return []

    # Сортируем все боксы сначала по Y (центру), чтобы идти сверху вниз
    boxes.sort(key=lambda b: (min(p[1] for p in b[0]) + max(p[1] for p in b[0])) / 2)

    median_h = median_text_height(boxes)
    y_threshold = int(median_h * 0.5) # Немного уменьшим порог для точности

    lines = []
    current_line_boxes = []
    
    if boxes:
        # Берем центр первого бокса как эталон для первой строки
        first_box = boxes[0][0]
        current_y_center = (min(p[1] for p in first_box) + max(p[1] for p in first_box)) / 2
        
        for box, text in boxes:
            box_y_center = (min(p[1] for p in box) + max(p[1] for p in box)) / 2
            
            if abs(box_y_center - current_y_center) <= y_threshold:
                current_line_boxes.append((box, text))
            else:
                # Сортируем накопленную строку по X (слева направо)
                current_line_boxes.sort(key=lambda b: min(p[0] for p in b[0]))
                lines.append(" ".join(t for _, t in current_line_boxes))
                
                # Переходим к новой строке
                current_line_boxes = [(box, text)]
                current_y_center = box_y_center

        # Не забываем последнюю строку
        if current_line_boxes:
            current_line_boxes.sort(key=lambda b: min(p[0] for p in b[0]))
            lines.append(" ".join(t for _, t in current_line_boxes))

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