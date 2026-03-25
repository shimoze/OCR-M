from app.text.normalizer import TextNormalizer
from app.utils.structures import OCRLine

def filter_by_score(score, min_score=0.6):
    return score >= min_score


def filter_noise(text, min_len=2):
    return len(text.strip()) >= min_len


def filter_small_boxes(box, min_height=10):
    ys = [p[1] for p in box]
    return (max(ys) - min(ys)) >= min_height


def postprocess(lines, normalizer=None):

    if normalizer is None:
        normalizer = TextNormalizer()

    results = []

    for line in lines:

        if not filter_by_score(line.score):
            continue

        if not filter_noise(line.text):
            continue

        if not filter_small_boxes(line.box):
            continue

        normalized_line = normalizer.process_line(line)
        results.append(normalized_line)


    return results
