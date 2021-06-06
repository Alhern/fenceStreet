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

## Comment contribuer ?
Vous pouvez consulter les ['Issues'](https://github.com/Alhern/fenceStreet/issues) pour contribuer au projet, les issues avec le tag `TODO` sont des missions à réaliser (si vous l'acceptez), si vous souhaiter répondre à une de ces missions laissez un commentaire pour signaler aux autres que vous vous en occupez. 

Quand vous avez terminé, vous pouvez faire une Pull Request en indiquant quelle Issue/problème vous avez résolu (ex : *Historique des transactions #2*...)

### Pull requests
N'oubliez pas de garder à jour votre repo (`git pull` en local) pour éviter les conflits.

Version courte :

1. Fork le projet.
1. Clone le projet.
1. `git check out -b [nom-de-ta-fonctionnalité]`
1. Écris ton code.
1. `git commit -a -m [ton-message-de-commit]`
1. `git push --set-upstream origin [nom-de-ta-fonctionnalité]`

Version longue :

[Contribution à un projet](http://git-scm.com/book/fr/v2/GitHub-Contribution-%C3%A0-un-projet)

Schema explicatif :

![img](https://res.cloudinary.com/takeout/image/upload/v1622997074/git-fork-clone-flow_w6x3an.png "https://www.earthdatascience.org/courses/intro-to-earth-data-science/git-github/github-collaboration/update-github-repositories-with-changes-by-others/")

### Problèmes, suggestions, etc

N'hésitez pas à faire des suggestions, si vous avez un bug ou un problème que vous n'arrivez pas à résoudre vous pouvez créer une "issue" (['Create an issue'](https://github.com/Alhern/fenceStreet/issues))


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


