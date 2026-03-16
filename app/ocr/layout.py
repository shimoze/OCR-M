import statistics

from app.utils.structures import OCRLine

#Измеряем высоту бокса
def box_height(box):
    ys = [p[1] for p in box]
    return max(ys) - min(ys)

#Средняя высота строки
def median_text_height(boxes):
    heights = [box_height(line.box) for line in boxes]
    return statistics.median(heights)

def sort_boxes(boxes):
    """
    boxes: list of (box, text)
    box: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
    """
    def box_key(line):
        y = min(p[1] for p in line.box)
        x = min(p[0] for p in line.box)
        return (y, x)

    return sorted(boxes, key=box_key)

def group_lines(boxes):
    if not boxes:
        return []

    # Сортируем все боксы сначала по Y (центру), чтобы идти сверху вниз
    boxes.sort(
        key=lambda line: (
            (min(p[1] for p in line.box) + 
             max(p[1] for p in line.box)
             ) / 2)
    )
    median_h = median_text_height(boxes)
    y_threshold = int(median_h * 0.5) # Немного уменьшим порог для точности

    lines = []
    current_line = []

    first_box = boxes[0].box
    current_y_center = (min(p[1] for p in first_box) + max(p[1] for p in first_box)) / 2

    for line in boxes:
        box_y_center = (min(p[1] for p in line.box) + max(p[1] for p in line.box)) / 2

        if abs(box_y_center - current_y_center) <= y_threshold:
            current_line.append(line)
        else:
            current_line.sort(key=lambda l: min(p[0] for p in l.box))

            line_text = " ".join(l.text for l in current_line)
            line_score = sum(l.score for l in current_line) / len(current_line)
            line_box = [p for l in current_line for p in l.box]

            lines.append(
                OCRLine(
                    text=line_text,
                    score=line_score,
                    box= line_box,
                )
            )

            current_line = [line]
            current_y_center = box_y_center

    if current_line:
        current_line.sort(key=lambda l: min(p[0] for p in l.box))

        line_text =" ".join(l.text for l in current_line)
        line_score = sum(l.score for l in current_line) / len(current_line)
        line_box = [p for l in current_line for p in l.box]
        lines.append(OCRLine(
            text= line_text,
            score= line_score,
            box= line_box,
        ))

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