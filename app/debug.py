from utils.visualization import OCRVisualizer
from utils.paths import RAW_DIR
import cv2

viz = OCRVisualizer()

img = cv2.imread(RAW_DIR / "test_image.jpg")
viz.save("original", img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
viz.save("gray", gray)

denoise = cv2.fastNlMeansDenoising(gray, h=10)
viz.save("denoise", denoise)

_, thresh = cv2.threshold(denoise, 127, 255, cv2.THRESH_BINARY)
viz.save("threshold", thresh)

# пример морфологии
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
viz.save("morph", morph)

# пример boxes
boxes = [[50,50,150,100], [200,80,300,130]]  # пример bbox
viz.save_boxes(morph, boxes)

# показать grid
viz.show_grid(cols=3)

# вывести тайминги
viz.print_timings()