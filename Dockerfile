FROM python:3.11

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
	cd /usr/local/bin && \
	ln -s /opt/poetry/bin/poetry && \
	poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

ENV PYTHONPATH=/app

COPY ./app /app/app

# Copy the alembic.ini file
COPY ./alembic.ini /app/

# Copy the alembic folder, excluding the versions folder content
COPY ./alembic/env.py /app/alembic/
COPY ./alembic/script.py.mako /app/alembic/
COPY ./alembic/README /app/alembic/

# For local database
COPY ./alembic/versions/* /app/alembic/versions/

# Create the versions folder if it doesn't exist, without copying its contents
RUN mkdir -p /app/alembic/versions

COPY ./start.sh /app/

EXPOSE 8000

CMD ["sh", "/app/start.sh"]
