import streamlit as st
import cv2
import numpy as np

from app.ocr import engine
from app.ocr.pipeline import OCRPipeline
from app.utils.visualization import OCRVisualizer

# --- Инициализация (Кэшируем, чтобы не грузить модель постоянно) ---
@st.cache_resource
def get_ocr_system():
    ocr_model = engine.init_ocr('paddle')
    return OCRPipeline(ocr=ocr_model)

st.set_page_config(layout="wide", page_title="OCR Debug Dashboard")

st.title("🔍 OCR Pipeline Debugger")

# --- Настройки в Sidebar ---
st.sidebar.header("Параметры")
# Здесь можно добавить слайдеры для порогов, если прокинуть их в pipeline
det_db_thresh = st.sidebar.slider("DB Thresh", 0.1, 0.9, 0.3)

# --- Загрузка файла ---
uploaded_file = st.sidebar.file_uploader("Загрузите изображение", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Конвертация в формат OpenCV
    file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
    img_original = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    pipeline = get_ocr_system()
    viz = OCRVisualizer(steps_dir=None) # Нам не нужен путь для UI

    # --- ЗАПУСК PIPELINE ПО ШАГАМ ---
    with st.status("Обработка...") as status:
        st.write("Препроцессинг...")
        img_pre = pipeline.preprocess(img_original)
        
        st.write("Поиск текста...")
        items = pipeline.run_ocr(img_pre)
        
        st.write("Группировка слов и строк...")
        words = pipeline.to_words(items)
        words = pipeline.sort(words)
        lines = pipeline.group(words)
        
        st.write("Постобработка текста...")
        final_text = pipeline.postprocess(lines)
        status.update(label="Готово!", state="complete")

    # --- ВИЗУАЛИЗАЦИЯ В СЕТКЕ ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(img_original, caption="Оригинал", channels="BGR")
        
    with col2:
        st.image(img_pre, caption="Препроцессинг (Ч/Б)", channels="BGR")

    st.divider()

    col3, col4 = st.columns(2)
    
    with col3:
        # Рисуем слова
        img_words = viz.draw_onto_image(img_pre, words, color=(0, 255, 0))
        st.image(img_words, caption="Детекция слов (Words)", channels="BGR")
        
    with col4:
        # Рисуем линии
        img_lines = viz.draw_onto_image(img_pre, lines, color=(255, 0, 0))
        st.image(img_lines, caption="Группировка строк (Lines)", channels="BGR")

    st.divider()

    # --- ВЫВОД ТЕКСТА ---
    st.subheader("📝 Итоговый текст:")
    st.text_area(label="Результат после Spellcheck", value=final_text, height=300)

else:
    st.info("Загрузите изображение в боковой панели, чтобы начать.")