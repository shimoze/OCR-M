from text.normalizer import TextNormalizer


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
        text = line["text"]
        score = line["score"]
        box = line["box"]

        if not filter_by_score(score):
            continue

        if not filter_noise(text):
            continue

        if not filter_small_boxes(box):
            continue

        clean_text = normalizer.process(text)

        results.append(clean_text)

    return "\n".join(results)
