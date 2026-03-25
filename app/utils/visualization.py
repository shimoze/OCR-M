import cv2
import os
import time
import numpy as np
from app.utils.structures import OCRBlock, OCRLine, OCRWord

DEBUG = True

class OCRVisualizer:
    def __init__(self, steps_dir):
        self.steps_dir = steps_dir
        self.steps = []
        self.start_times = {}
        self.counter = 0

    def save(self, name, image):
        """Сохраняет изображение на диск и отмечает время"""
        if not DEBUG:
            return
        
        self.counter += 1
        filename = self.steps_dir / f"{self.counter:03d}_{name}.png"
        cv2.imwrite(str(filename), image)
        self.steps.append((name, filename))
        self.start_times[name] = time.time()

    def save_boxes(self, image, items, name="boxes", color=(0, 255, 0), thickness=2):
        """
        Сохраняет изображение с нарисованными bounding boxes.
        items может быть списком OCRWord, OCRLine или OCRBlock.
        """
        if not DEBUG:
            return
        
        img_copy = image.copy()
        for item in items:
            box = getattr(item, "box", None)
            if box is None:
                continue

            pts = np.array(box, np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(img_copy, [pts], isClosed=True, color=color, thickness=thickness)

        self.save(name, img_copy)

    def save_pipeline_steps(self, original, preprocessed=None, words=None, lines=None, blocks=None):
        """
        Сохраняет ключевые шаги pipeline:
        - original: исходное изображение
        - preprocessed: после фильтров (threshold/morph)
        - words: OCRWord
        - lines: OCRLine
        - blocks: OCRBlock
        """
        self.save("original", original)
        if preprocessed is not None:
            self.save("preprocessed", preprocessed)
        if words is not None:
            self.save_boxes(preprocessed if preprocessed is not None else original, words, name="words")
        if lines is not None:
            self.save_boxes(preprocessed if preprocessed is not None else original, lines, name="lines", color=(255, 0, 0))
        if blocks is not None:
            self.save_boxes(preprocessed if preprocessed is not None else original, blocks, name="blocks", color=(0, 0, 255))

    def show_grid(self, cols=3, window_name="OCR Debug Grid"):
        """Показывает grid из всех сохранённых этапов"""
        if not DEBUG or len(self.steps) == 0:
            return
        
        images = [cv2.imread(str(f[1])) for f in self.steps]
        names = [f[0] for f in self.steps]

        # resize к одному размеру
        h_min = min(img.shape[0] for img in images)
        w_min = min(img.shape[1] for img in images)
        images_resized = [cv2.resize(img, (w_min, h_min)) for img in images]

        # формируем grid
        rows = (len(images) + cols - 1) // cols
        blank = np.zeros_like(images_resized[0])
        grid = []

        for r in range(rows):
            row_imgs = []
            for c in range(cols):
                idx = r * cols + c
                if idx < len(images_resized):
                    row_imgs.append(images_resized[idx])
                else:
                    row_imgs.append(blank)
            grid.append(np.hstack(row_imgs))

        final_grid = np.vstack(grid)
        cv2.imshow(window_name, final_grid)
        cv2.waitKey(0)
        cv2.destroyAllWindows()