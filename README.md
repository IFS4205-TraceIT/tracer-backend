# tracer-backend

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
5. Run `poetry run manage.py makemigrations` and `poetry run manage.py migrate` to migrate the database.
6. Run `poetry run manage.py runserver` to start the server.

