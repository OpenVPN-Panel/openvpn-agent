FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* README.md ./
COPY src ./src

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev

EXPOSE 8000

CMD ["uvicorn", "src.presentation.main:app", "--host", "0.0.0.0", "--port", "8000"]
