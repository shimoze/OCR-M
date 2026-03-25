from app.ocr.preprocessing import soft_preprocess
from app.ocr.engine import run_ocr
from app.ocr.postprocess import postprocess
from app.ocr.layout import sort_boxes, group_lines
from app.utils.structures import OCRWord

class OCRPipeline:
    def __init__(self, ocr):
        self.ocr = ocr
        
    def preprocess(self, img):
        return soft_preprocess(img)
    
    def run_ocr(self, img):
        return run_ocr(self.ocr, img)
    
    def to_words(self, items):
        words = []
        for box, (text, score) in items:
            words.append(OCRWord(
                text=text,
                score=score,
                box=box
            ))
        return words

    def sort(self, items):
        return sort_boxes(items)

    def group(self, items):
        return group_lines(items)

    def postprocess(self, lines):
        return postprocess(lines)

    def run(self, img):
        img = self.preprocess(img)
        items = self.run_ocr(img)
        words = self.to_words(items)
        words = self.sort(words)
        lines = self.group(words)
        text = self.postprocess(lines)

        return text