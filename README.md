# tracer-backend [![Tracer Backend CI](https://github.com/IFS4205-TraceIT/tracer-backend/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/IFS4205-TraceIT/tracer-backend/actions/workflows/ci.yml) [![Semgrep](https://github.com/IFS4205-TraceIT/tracer-backend/actions/workflows/semgrep.yml/badge.svg?branch=main)](https://github.com/IFS4205-TraceIT/tracer-backend/actions/workflows/semgrep.yml)

## Setting up for local development

> Do view the settings file in `tracer_backend/settings.py` to modify any settings before starting.

1. Ensure you have the following installed:
    * Python: `3.10` or above
    * Docker: `20.10.18` or above
    * Docker Compose:  `2.10.2` or above
2. Setup the required services using the `docker-compose.yml` file:
    ```bash
    docker-compose up
    ```
3. Installing dependencies:
    1. Install poetry on your machine: https://python-poetry.org/
    2. Run `poetry install` to install the required dependencies.
4. Set and export the required environment variables:
    ```bash
    export DJANGO_SECRET_KEY="test" \
        DJANGO_DEBUG="True" \
        VAULT_ADDR="http://127.0.0.1:8200" \
        VAULT_TOKEN="dev-only-token" \
        POSTGRES_HOST="127.0.0.1" \
        POSTGRES_AUTH_HOST="127.0.0.1" \
        POSTGRES_RESEARCH_HOST="127.0.0.1" \
        POSTGRES_PORT="5432" \
        POSTGRES_AUTH_PORT="5432" \
        POSTGRES_RESEARCH_PORT="5432" \
        POSTGRES_DB="test1" \
        POSTGRES_RESEARCH_DB="test2" \
        POSTGRES_AUTH_DB="test3" \
        POSTGRES_USER="test" \
        POSTGRES_RESEARCH_USER="test" \
        POSTGRES_AUTH_USER="test" \
        POSTGRES_PASSWORD="test" \
        POSTGRES_RESEARCH_PASSWORD="test" \
        POSTGRES_AUTH_PASSWORD="test" \
        POSTGRES_SUPER_USER="test" \
        POSTGRES_SUPER_PASSWORD="test"
    ```

5. Run `poetry run python manage.py makemigrations` and `poetry run python manage.py migrate` to migrate the database.
6. Run `poetry run python manage.py runserver` to start the server.

