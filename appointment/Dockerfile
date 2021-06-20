FROM python:3.8.10-alpine as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN apk update \
 && apk add gcc musl-dev postgresql-dev python3-dev && \
 PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

COPY . .

RUN apk --no-cache add libpq
ENTRYPOINT ["python", "server.py"]
