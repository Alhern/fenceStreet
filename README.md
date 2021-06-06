# Fence Street
[FR version](README_FR.md)

A New York Stock Exchange simulator app using Django and IEX Cloud.

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

## How to contribute?
You can check ['Issues'](https://github.com/Alhern/fenceStreet/issues) to contribute to the project, issues tagged with `TODO` are tasks to work on, if you want to work on one of them leave a comment to let others know that you're working on it. 

Once you're done, you can do a Pull Request mentioning which Issue you solved (ex : *Historique des transactions #2*...)

### Pull requests
 :warning: Don't forget to keep your repo up-to-date (`git pull` locally) to prevent conflicts.

Short version:

1. Fork.
1. Clone.
1. `git check out -b [name-of-your-feature]`
1. Write your code.
1. `git commit -a -m [your-commit-message]`
1. `git push --set-upstream origin [name-of-your-feature]`

Long version:

[Contributing to a project](http://git-scm.com/book/en/v2/GitHub-Contributing-to-a-Project)

Visual:

![img](https://res.cloudinary.com/takeout/image/upload/v1622997074/git-fork-clone-flow_w6x3an.png "https://www.earthdatascience.org/courses/intro-to-earth-data-science/git-github/github-collaboration/update-github-repositories-with-changes-by-others/")

### Problems, suggestions, etc

Feel free to make suggestions, if you encounter a bug or any issue that you can't fix, you can create an Issue (['Create an issue'](https://github.com/Alhern/fenceStreet/issues))

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


