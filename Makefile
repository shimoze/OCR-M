# Сборка образа
build:
	docker build -t ocr_module .

# Запуск UI версии
run-ui:
	docker run --rm -p 8501:8501 \
		-v $(CURDIR)/models:/app/models \
		ocr_module

# Зайти внутрь контейнера
shell:
	docker run -it --rm ocr_module /bin/bash