import cv2
import os
import time
import numpy

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
    
    def save_boxes(self, image, boxes, color=(0, 255, 0), thickness=2):
        """Сохраняет изображение с нарисованными bounding boxes"""
        if not DEBUG:
            return
        
        img_copy = image.copy()
        for box in boxes:
            if isinstance(box, numpy.ndarray):
                box = box.astype(int)
            if len(box) == 4:
                x1, y1, x2, y2 = box
                cv2.rectangle(img_copy, (x1, y1), (x2, y2), color, thickness)
        self.save("boxes", img_copy)
    
    def show_grid(self, cols=3, window_name="OCR Debug Grid"):
        """Показывает grid из всех сохранённых этапов"""
        if not DEBUG or len(self.steps) == 0:
            return
        
        images = [cv2.imread(str(f[1])) for f in self.steps]
        names = [f[0] for f in self.steps]

        #resize к одному размеру
        h_min = min(img.shape[0] for img in images)
        w_min = min(img.shape[1] for img in images)
        images_resized = [cv2.resize(img, (w_min, h_min)) for img in images]

        # формируем grid
        rows = (len(images) + cols - 1) // cols
        blank = numpy.zeros_like(images_resized[0])
        grid = []

        for r in range(rows):
            row_imgs = []
            for c in range(cols):
                idx = r * cols + c
                if idx < len(images_resized):
                    row_imgs.append(images_resized[idx])
                else:
                    row_imgs.append(blank)
            grid.append(numpy.hstack(row_imgs))

        final_grid = numpy.vstack(grid)
        cv2.imshow(window_name, final_grid)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
