# Fence Street
[EN version](README.md)

Application de simulation pour la Bourse de New York utilisant Django et IEX Cloud.

## Prérequis
 :warning: Pour pouvoir utiliser Fence Street vous devez avoir une clé API [IEX Cloud](https://iexcloud.io/) et une clé API [Alpha Vantage](https://www.alphavantage.co/support/#api-key). 

Vos clés devront être placées directement dans un fichier nommé `keys.py` qui ressemblera à ceci :

    TOKEN_SANDBOX = 'Tpk_123456' # IEX Cloud sandbox token (for tests)
    TOKEN_PROD = 'pk_123456'  # IEX Cloud production token
    ALPHA_KEY = '123456'   # Alpha Vantage token

Vous devrez ouvrir votre environnement virtuel et installer les fichiers requis dans `requirements.txt` avec pip3 :

    pip3 install -r requirements.txt

## Démarrer l'app
Pour démarrer l'app la **première fois** vous devez d'abord appliquer les migrations :

    python3 manage.py migrate

Vous devrez ensuite créer un superuser (admin) pour pouvoir utiliser l'admin dashboard (http://127.0.0.1:8000/admin/) :
    
    python3 manage.py createsuperuser

Enfin, pour démarrer l'app :

    python3 manage.py runserver

## Crédits
Cette app a été réalisée avec :
* `Python 3`
* `Django`
* `HTML/CSS/Javascript`
* `Bootstrap`
* `SQLite`
* `PyCharm`
* `Git/Github`
* `...`


