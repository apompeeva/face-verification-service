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

COPY ./entrypoint.sh .
RUN chmod +x /face_verification/entrypoint.sh

ENTRYPOINT ["sh", "/face_verification/entrypoint.sh"]
