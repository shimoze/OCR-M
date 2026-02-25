from ocr.text.normalizer import TextNormalizer

#Фильтр по confidence
def filter_by_score(text, score, min_score=0.6):
    if score < min_score:
        return None
    return text

#Фильтр шума
def filter_noise(text, min_len=2):
    if len(text.strip()) < min_len:
        return None
    return text

def filter_small_boxes(box, min_height=10):
    ys = [p[1] for p in box]
    return (max(ys) - min(ys)) >= min_height

def postprocess(text, score, box, normalizer):
    
    if filter_by_score(text, score) is None:
        return None

    text = filter_noise(text)

    if text is None:
        return None

    clean_text = normalizer.process(text)

    return clean_text
