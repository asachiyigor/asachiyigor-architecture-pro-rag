FROM python:3.11-slim

WORKDIR /app

# Копируем requirements
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY src/ src/
COPY data/ data/
COPY knowledge_base/ knowledge_base/
COPY scripts/ scripts/
COPY tests/ tests/

# Создаем директорию для логов
RUN mkdir -p logs

# Переменные окружения
ENV PYTHONUNBUFFERED=1

# Запускаем бота
CMD ["python", "src/rag_bot.py"]
