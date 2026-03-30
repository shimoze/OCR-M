# Сборка образа
build:
	docker build -t ocr_module .

# Запуск обработки данных
run:
	docker run --rm \
		-v $(shell pwd)/data/input:/app/data/input \
		-v $(shell pwd)/data/output:/app/data/output \
		ocr_module

# Зайти внутрь контейнера
shell:
	docker run -it --rm ocr_module /bin/bash