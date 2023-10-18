FROM python:3.11-alpine

EXPOSE 8000

WORKDIR /app

RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry

COPY . /app

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without tests

CMD ["poetry", "run", "uvicorn", "molgan.main:app", "--host", "0.0.0.0", "--port", "8000"]