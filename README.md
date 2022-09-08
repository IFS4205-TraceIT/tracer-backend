# tracer-backend

## Setting up for local development

> Do view the settings file in `tracer_backend/settings.py` to modify any settings before starting.

1. Ensure you have Python 3.10 or above and Vault installed on your machine.
2. Configure Vault:
    1. Start Vault with the following command: `vault server -dev -dev-root-token-id="dev-only-token"`
    2. On a separate terminal, run `vault secrets enable totp` to enable TOTP function.
3. Installing dependencies:
    1. Install poetry on your machine: https://python-poetry.org/
    2. Run `poetry install` to install the required dependencies.
5. Run `poetry run manage.py makemigrations` and `poetry run manage.py migrate` to migrate the database.
6. Run `poetry run manage.py runserver` to start the server.

