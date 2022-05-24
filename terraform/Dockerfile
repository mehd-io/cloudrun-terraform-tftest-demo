FROM python:3.10


ENV PORT=8080
ENV APP_HOME /app

WORKDIR $APP_HOME

COPY ./hello_world_api poetry.lock pyproject.toml ./

RUN pip install poetry==1.1.13 --no-cache-dir \
    && poetry config virtualenvs.create false && poetry install --no-dev
    
CMD exec uvicorn --host 0.0.0.0 --port ${PORT} app:app
