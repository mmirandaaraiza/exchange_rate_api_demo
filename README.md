Demo api that shows the current exchange rate USD to MXN from a few sources

# Instructions

## Installing dependencies
Dependencies were locked using pipenv and python 3.8

- pipenv install
- pipenv shell

## Modify the tokens
- Banxico's API needs a token which can be obtained from: https://www.banxico.org.mx/SieAPIRest/service/v1/token
- Fixer's API needs a token which can be obtained from: https://fixer.io/signup/free

Please modify the values for *BANXICO_TOKEN* and *FIXER_TOKEN* in the project's settings which are located in config > settings.

If the tokens aren't set in the project's settings, the only source used will be the Diario Oficial de la Federación

## Testing
- python manage.py test

## Usage

### Create database
Database will use sqlite3

- python manage.py makemigrations
- python manage.py migrate

### Create user(s)
- python manage.py createsuperuser

### Run the development server
- python manage.py runserver

### Examples
This API uses JWT for access.

Examples of usage are provided with curl.

**Get access token**

curl -d '{"username": "*USERNAME*", "password": "*PASSWORD*"}' -H 'Content-Type: application/json' -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/api/token/

**Get the rates**

curl -H 'Accept: application/json; indent=4' -H 'Authorization: Bearer *ACCESS_TOKEN*' http://127.0.0.1:8000/api/rates/

## Limitations
Fixer's API has a default base currency of EUR. This value cannot be changed with a free token.

If you have a paid token then please modify the value for FIXER_DEFAULT_CURRENCY in the project's settings which are located in config > settings. If this value is left blank, then the default currency will be used in order to provide a fallback value.
