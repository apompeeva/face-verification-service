FROM python:3.12-slim

WORKDIR /face_verification

ENV POETRY_VERSION=1.8.3

RUN apt-get update && apt-get -y upgrade && pip install "poetry==${POETRY_VERSION}" \
    && apt-get install -y gcc pkg-config libhdf5-hl-100 libhdf5-dev ffmpeg libsm6 libxext6 \
    && apt-get -y install kafkacat
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY ./src/app ./app

EXPOSE 8000

COPY ./alembic.ini  .
COPY ./src/migration ./src/migration

ENTRYPOINT [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
