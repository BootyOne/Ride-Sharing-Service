FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

# Копируем все остальные файлы
COPY . /app/

# Запуск сервера
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
