# Fence Street
A New York Stock Exchange app using Django and IEX Cloud.

## Requirements
 :warning: To be able to use Fence Street you must have an [IEX Cloud](https://iexcloud.io/) API key and an [Alpha Vantage](https://www.alphavantage.co/support/#api-key) API key. 

Your tokens will need to be placed directly inside a file named `keys.py` that will look like this:

    TOKEN_SANDBOX = 'Tpk_123456' # IEX Cloud sandbox token (for tests)
    TOKEN_PROD = 'pk_123456'  # IEX Cloud production token
    ALPHA_KEY = '123456'   # Alpha Vantage token

You will need to open your virtual env and install the required files in `requirements.txt` with pip3:

    pip3 install -r requirements.txt

## Starting the app
To start the app the **first time** you will need to apply migrations first:

    python3 manage.py migrate

You will then need to create a superuser (admin) to be able to use the admin dashboard (http://127.0.0.1:8000/admin/):
    
    python3 manage.py createsuperuser

Finally, to start the app:

    python3 manage.py runserver

## Credits
This app has been built with:
* `Python 3`
* `Django`
* `HTML/CSS/Javascript`
* `Bootstrap`
* `SQLite`
* `PyCharm`
* `Git/Github`
* `...`


