FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev \
    libpq-dev \
    nmap

ADD pyproject.toml /app

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi


COPY alembic.ini /app/
COPY /migrations/ /app/migrations/
COPY /src/ /app/src/
COPY .env /app/
COPY entrypoint.sh /app/

RUN chmod a+x entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
