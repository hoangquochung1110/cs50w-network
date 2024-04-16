FROM python:3
ENV PYTHONUNBUFFERED 1

ENV POETRY_VERSION=1.6.1
ENV POETRY_HOME=/etc/poetry
ENV POETRY_VIRTUALENVS_CREATE=false
RUN curl -sSL https://install.python-poetry.org | python3 -

RUN mkdir /workspace
WORKDIR /workspace
COPY . /workspace/

COPY pyproject.toml poetry.lock ./
ARG POETRY_OPTIONS="--no-root --no-interaction --no-ansi"
ARG install_groups
RUN /etc/poetry/bin/poetry install --only $install_groups $POETRY_OPTIONS
