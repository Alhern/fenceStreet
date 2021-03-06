from django.shortcuts import render, redirect

from .models import Stock, Portfolio, Wallet, History
from .forms import StockForm, RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm

from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from alpha_vantage.timeseries import TimeSeries

import plotly.graph_objs as go
from plotly.offline import plot

import requests
import json


#################################
#           API KEYS            #
#################################

# /!\ Laisser keys.py dans .gitignore
from .keys import *

# Token sandbox IEX à utiliser lors des tests
TOKEN_S = TOKEN_SANDBOX

# Token de production IEX
TOKEN_P = TOKEN_PROD

# Pour les graphiques d'Alpha Vantage
TOKEN_ALPHA = ALPHA_KEY

# Utiliser la sandbox pour tous les tests (évite les limitations d'appels vers l'API)
SANDBOX_URL = 'https://sandbox.iexapis.com/stable'
PROD_URL = 'https://cloud.iexapis.com/stable'

# Switch ici entre la sandbox et la prod
# (/!\ SANDBOX_URL avec TOKEN_S, PROD_URL avec TOKEN_P)
BASE_URL = PROD_URL
BASE_TOKEN = TOKEN_P

#################################

# get_all_tickers() nous permet de récupérer tous les symboles de l'API, on l'utilise pour connaître toutes les sociétés cotées au NYSE
# elle permet de vérifier que l'utilisateur entre un symbole/ticker qui existe réellement.
def get_all_tickers():
    all_tickers = []
    try:
        data = requests.get(f'{BASE_URL}/ref-data/symbols?token={BASE_TOKEN}')
    except requests.exceptions.HTTPError as e:
        print("An HTTP error occurred: the API is temporarily unavailable.")
        print(e)
    try:
        raw_tickers = json.loads(data.content)
        for i in raw_tickers:
            all_tickers.append(i["symbol"])
    except Exception as e:
        print(e)
    return all_tickers


# on appelle directement la fonction et on récupère notre liste de tickers ici pour pouvoir s'en servir plus tard
ALL_TICKERS = get_all_tickers()

# on récupère ici un symbole entré par l'utilisateur et on récupère les informations de l'entreprise via 3 requêtes (quote, company, news)
def home(req):

    if len(ALL_TICKERS) == 0:
        messages.error(req, ("The API is temporarily down. We\'re very sorry for the inconvenience!"))
        return render(req, 'home.html', {'ticker': 'Please try again later.'})

    if req.method == 'POST':
        ticker = req.POST['ticker']

        if ticker.upper() in ALL_TICKERS:
            # on initialise TimeSeries pour pouvoir réaliser 2 graphiques concernant l'entreprise demandée via des appels aux fonctions candlestick() et scatter()
            ts = TimeSeries(key=TOKEN_ALPHA, output_format='pandas')

            # si on utilise pandas pour les graphiques, on utilise un format JSON pour récupérer des infos sur AV
            # on récupère ici via AV des infos concernant "open", "high", "low", et "volume". Ces informations ne
            # sont plus librement disponibles au public via IEX Cloud donc voici une parade
            ts_json = TimeSeries(key=TOKEN_ALPHA)

            try:
                alpha_data, meta_data = ts_json.get_quote_endpoint(ticker)
            except ValueError as e:
                print(e)
                alpha_data = 404

            session = requests.Session()

            stock_data = session.get(f'{BASE_URL}/stock/{ticker}/quote?token={BASE_TOKEN}')
            company_data = session.get(f'{BASE_URL}/stock/{ticker}/company?token={BASE_TOKEN}')
            news_data = session.get(f'{BASE_URL}/stock/{ticker}/news/last/3?token={BASE_TOKEN}')

            try:
                stock = json.loads(stock_data.content)

            # TODO: les exceptions sont trop générales ici, reprendre le modèle de la fonction simulator() pour avoir des exceptions précises
            except Exception as e:
                print(e)
                stock = 404

            try:
                company = json.loads(company_data.content)
            except Exception as e:
                print(e)
                company = 404

            try:
                news = json.loads(news_data.content)
            except Exception as e:
                print(e)
                news = 404

            return render(req, 'home.html',
                      {'alpha_data': alpha_data,
                       'stock': stock,
                       'news': news,
                       'company': company,
                       'candlestick': candlestick(ticker, ts),
                       'scatter': scatter(ticker, ts)})
        else:
            messages.error(req, ("The ticker you entered does not exist. Try again."))
            return render(req, 'home.html', {'ticker': 'Please enter a valid ticker.'})

    else:
        return render(req, 'home.html', {'ticker': 'Enter a ticker please.\nEx: GME, AMC, TSLA...'})


# une simple view d'exemple, on n'a rien sur cette page pour le moment
def about(req):
    return render(req, 'about.html', {})


#################################
#################################
##     S I M U L A T E U R     ##
#################################
#################################

# Affichage du portfolio + fonction d'achat de stocks intégrée
def simulator(req):
    # on commence par récupérer le wallet de l'utilisateur
    user_wallet = Wallet.objects.get(user=req.user)
    # on le converti en float pour pouvoir réaliser nos calculs
    wallet = float(user_wallet.wallet)
    # on récupère le portfolio de l'utilisateur
    portfolio = Portfolio.objects.filter(user=req.user)
    history = History.objects.filter(user=req.user)

    # on va utiliser plusieurs listes pour récupérer des données du Portfolio
    # + prix actuels issus de l'API + différences, totaux, et on va zipper le tout
    # pour pouvoir réutiliser ces infos dans le template simulator.html
    portfolio_id = []
    portfolio_tickers = []
    portfolio_prices = []
    portfolio_quantity = []
    portfolio_change = []
    portfolio_total = []

    current_prices = []

    bought_and_current = None

    # cette boucle nous permet de récupérer toutes les infos du Portfolio de l'utilisateur pour les placer dans des listes
    for i in portfolio:
        portfolio_id.append(i.id)
        portfolio_tickers.append(i.symbol)
        portfolio_prices.append(i.price)
        portfolio_quantity.append(i.quantity)

    # s'il y a au moins une entreprise dans le portfolio, on affiche ses infos
    if len(portfolio_tickers) != 0:

        session = requests.Session()  # on créé une connexion persistante réutilisable, chaque requête sera plus rapide

        for item in portfolio_tickers:
            try:
                data = session.get(f'{BASE_URL}/stock/{item}/quote?token={BASE_TOKEN}')
                data.raise_for_status()
                stock = json.loads(data.content)
                # après un appel vers l'API on récupère le prix actuel de l'action/stock et on le range dans la liste current_prices
                current_prices.append(stock['latestPrice'])
            except requests.exceptions.ConnectionError as e:
                messages.error(req, "Failed to establish a connection.")
                print(e)
                break
            except requests.exceptions.HTTPError as e:
                messages.error(req, "An HTTP error occurred: the API is temporarily unavailable.")
                print(e)
                stock = 404

        # on calcule ici les différences entre les prix actuels (current_prices) et les prix d'achat (portfolio_prices)
        # on range la différence dans portfolio_total et portfolio_change (pourcentage de différence positif ou négatif)
        for y in range(len(portfolio_prices)):
            diff = round(float(current_prices[y]) - float(portfolio_prices[y]), 2)
            percentage = round(diff / float(portfolio_prices[y]) * 100, 2)
            portfolio_total.append(round(float(current_prices[y]) * int(portfolio_quantity[y]), 2))
            portfolio_change.append(percentage)

        # ce zip va permettre de créer un tableau contenant toutes les infos qui nous intéressent
        bought_and_current = zip(portfolio_id,
                                 portfolio_tickers,
                                 portfolio_quantity,
                                 portfolio_prices,
                                 current_prices,
                                 portfolio_change,
                                 portfolio_total)

    # l'utilisateur va acheter ses actions ici, en entrant un ticker/symbole et une quantité
    if req.method == 'POST':
        ticker = req.POST['ticker']

        # si le ticker existe réellement, on envoie une requête à l'API
        if ticker.upper() in ALL_TICKERS:

            stock_data = requests.get(f'{BASE_URL}/stock/{ticker}/quote?token={BASE_TOKEN}')

            try:
                stock = json.loads(stock_data.content)

            except Exception as e:
                print(e)
                stock = 404

            price = float(stock['latestPrice'])

            if req.POST['quantity'] == '':  # si on met rien dans le champ, défaut = 0
                quantity = 0
            else:
                try:
                    quantity = int(req.POST['quantity'])
                except ValueError as e:
                    print(e)
                    messages.error(req, ("Please enter a valid quantity using numbers only."))
                    return redirect('simulator')

            if quantity <= 0:
                messages.error(req, ("Please buy at least 1 share."))
                return redirect('simulator')
            else:
                total_price = price * quantity

                if total_price > wallet:
                    messages.error(req, ("Sorry but you're broke, try buying less or cheaper shares."))
                    return redirect('simulator')
                else:
                    # on fait la mise à jour du wallet ici, après l'achat en faisant la différence
                    new_wallet = wallet - total_price
                    user_wallet.wallet = new_wallet
                    user_wallet.save()
                    wallet = float(user_wallet.wallet)   # permet de mettre à jour le wallet sur la page quand on achète (ça ne marche pas ici parce que je ne fais pas de retour du wallet...)
                    updated_portfolio = Portfolio(user=req.user, symbol=ticker, quantity=quantity, price=price)
                    updated_portfolio.save()
                    updated_history = History(user=req.user, symbol=ticker, quantity=quantity, price=total_price, transaction="BUY", date=timezone.now())
                    updated_history.save()
                    messages.success(req, ("Successfully bought!"))

            return redirect(simulator)

        else:
            messages.error(req, ("Stock can't be displayed. Make sure the ticker exists."))
            return redirect('simulator')
    else:
        return render(req, 'simulator.html', {'wallet': wallet,
                                              'portfolio': portfolio,
                                              'bought_and_current': bought_and_current,
                                              'history': history})


# Fonction de vente de tous les stocks sélectionnés
# UPDATE : le 25/06/21, refonte de la fonction qui avait une sacré vulnérabilité,
# illustration : sell_all/18/4/205.83/204.2 envoie les informations suivantes à la fonction :
# vendre 4 actions du #18 achetées à 205.83 et qui coûtent maintenant 204.2, absolument rien n'empêchait
# un utilisateur de tricher en changeant les informations du lien pour se faire beaucoup plus d'argent :)
def sell_all(req, id):
    user_wallet = Wallet.objects.get(user=req.user)
    wallet = float(user_wallet.wallet)
    sold_stock = Portfolio.objects.get(id=id, user=req.user)
    bought_price = float(sold_stock.price)
    original_qty = sold_stock.quantity
    ticker = sold_stock.symbol

    session = requests.Session()

    stock_data = session.get(f'{BASE_URL}/stock/{ticker}/quote?token={BASE_TOKEN}')

    try:
        stock = json.loads(stock_data.content)

    except Exception as e:
        print(e)
        stock = 404

    current_price = float(stock['latestPrice'])

    # on fait les totaux ici concernant le montant que l'on a payé le jour de l'achat et le montant que l'on va recevoir si on vend maintenant
    total_original = float(bought_price) * original_qty
    total_current = float(current_price) * original_qty
    change = float(total_current) - float(total_original)

    # si on ajoute un système de points, définir les scores ici (-perte ou +profit)
    if change < 0:
        #print("sold at a loss")
        messages.warning(req, "You've sold at a loss...")
    else:
        #print("You've sold for a profit!")
        messages.success(req, "You've sold for a profit!")

    # on a tout vendu, on peut supprimer le stock (pour tester on se contente juste d'un print pour le moment)
    sold_stock.delete()

    # on met le wallet à jour avec ce qu'on vient de gagner ou perdre
    print(f"Ajout de ${total_current} à notre wallet de {wallet}")
    new_wallet = wallet + total_current
    user_wallet.wallet = new_wallet
    user_wallet.save()

    updated_history = History(user=req.user, symbol=ticker, quantity=original_qty, price=total_current, transaction="SELL", date=timezone.now())
    updated_history.save()

    return redirect(simulator)


# Fonction de vente des stocks suivant la quantité et l'ID entrées par l'utilisateur
def sell(req):
    # on commence par récupérer le wallet de l'utilisateur
    user_wallet = Wallet.objects.get(user=req.user)
    # on le converti en float pour pouvoir réaliser nos calculs
    wallet = float(user_wallet.wallet)

    if req.method == 'POST':

        stock_id = req.POST['stock_id']

        try:
            sold_stock = Portfolio.objects.get(id=stock_id, user=req.user)
            original_qty = sold_stock.quantity
        except Exception as e:
            messages.error(req, "This stock ID doesn't exist")
            return redirect(simulator)

        qty = int(req.POST['quantity'])

        if qty > original_qty:
            messages.error(req, "You can't sell more than what you own.")
            return redirect(simulator)

        ticker = Portfolio.objects.get(id=stock_id, user=req.user).symbol

        stock_data = requests.get(f'{BASE_URL}/stock/{ticker}/quote?token={BASE_TOKEN}')

        try:
            stock = json.loads(stock_data.content)

        except Exception as e:
            print(e)
            stock = 404

        current_price = float(stock['latestPrice'])
        bought_price = float(Portfolio.objects.get(id=stock_id, user=req.user).price)

        # on fait les totaux ici concernant le montant que l'on a payé le jour de l'achat et le montant que l'on va recevoir si on vend maintenant
        total_original = float(bought_price) * qty
        total_current = float(current_price) * qty
        change = float(total_current) - float(total_original)

        if change < 0:
            #print("sold at a loss")
            messages.error(req, "You've sold at a loss...")
        else:
            #print("You've sold for a profit!")
            messages.success(req, "You've sold for a profit!")

        # on a tout vendu, on peut supprimer le stock (pour tester on se contente juste d'un print pour le moment)
        if qty == original_qty:
            #print("Needs to be deleted due to quantity sold")
            sold_stock.delete()
        else:
        # sinon on soustrait la quantité vendue à la quantité totale
            original_qty -= qty
            #print("new qty =", original_qty)
            sold_stock.quantity = original_qty
            sold_stock.save()  # on enregistre la nouvelle quantité dans la BDD

        # on met le wallet à jour avec ce qu'on vient de gagner ou perdre
        #print(f"Ajout de ${total_current} à notre wallet de {wallet}")
        new_wallet = wallet + total_current
        user_wallet.wallet = new_wallet
        user_wallet.save()

        updated_history = History(user=req.user, symbol=ticker, quantity=qty, price=total_current, transaction="SELL", date=timezone.now())
        updated_history.save()

    return redirect(simulator)

###################################
# fin des fonctions du simulateur #
###################################


# La watchlist permet de surveiller des entreprises sélectionnées, on peut les ajouter et les supprimer (à l'aide de la fonction delete()) d'un tableau
def watchlist(req):
    if req.method == 'POST':
        if req.user.is_authenticated:  # faut être identifié pour ajouter une entreprise à la watchlist
            form = StockForm(req.POST)
            if form.is_valid() and form.cleaned_data['symbol'].upper() in ALL_TICKERS: # si l'entrée est valide ET que le ticker existe vraiment...
                instance = form.save(commit=False)
                instance.user = req.user
                if Stock.objects.filter(symbol=instance.symbol, user=req.user).exists(): # si on a déjà ajouté l'entreprise dans la watchlist on ne la rajoute pas
                    messages.error(req, ("This stock is already in your watchlist."))
                    return redirect('watchlist')
                else:  # si on a pas déjà ajouté le stock, c'est bon on l'ajoute à la liste
                    form.save(commit=True)
                    messages.success(req, ("Stock has been added succesfully."))
                    return redirect('watchlist')
            else:  # si l'entrée est invalide, erreur
                messages.error(req, ("Stock can't be added. Make sure the ticker exists."))
                return redirect('watchlist')
        else:  # il faut être identifié pour utiliser la watchlist sinon on redirige vers login.html
            messages.error(req, ("You are not logged in"))
            return redirect('login')
    else:  # sinon si l'utilisateur ouvre simplement la page...
        if not req.user.is_authenticated: # on affiche un message d'erreur si l'utilisateur n'est pas identifié et accède à la page
            messages.error(req, ("You are not logged in"))
            return redirect('login')
        symbol = Stock.objects.filter(user=req.user) # on récupère les entreprises de sa watchlist
        full_data = []

        session = requests.Session()

        for item in symbol: # pour chaque entreprise dans sa liste, on va récupérer ses infos via l'API
            try:
                data = session.get(f'{BASE_URL}/stock/{item}/quote?token={BASE_TOKEN}')
                data.raise_for_status()
                stock = json.loads(data.content)
                full_data.append(stock)
            except requests.exceptions.ConnectionError as e:
                messages.error(req, "Failed to establish a connection.")
                print(e)
                break
            except requests.exceptions.HTTPError as e:
                messages.error(req, "An HTTP error occurred: the API is temporarily unavailable.")
                print(e)
            except requests.exceptions.Timeout as e:
                messages.error(req, "The request timed out.")
                print(e)
            except requests.exceptions.RequestException as e:
                messages.error(req, "There was an ambiguous exception that occurred while handling your request.")
                print(e)

        return render(req, 'watchlist.html',
                      {'symbol': symbol,
                       'full_data': full_data,
                       })


# Permet de supprimer les tickers de la watchlist.
def delete(req, id):
    ticker = Stock.objects.get(symbol=id, user=req.user)
    item = Stock.objects.get(pk=ticker.id, user=req.user)
    item.delete()
    messages.success(req, ("Stock succesfully deleted."))
    return redirect(watchlist)


# Permet de réaliser le premier graphique Intraday qui va s'afficher dans home.html
def candlestick(ticker, ts):
    ticker = ticker.upper()
    try:
        data, meta_data = ts.get_intraday(ticker, interval='5min', outputsize='compact')
    except ValueError as e:
        print(e)
        return "Candlestick chart can't be displayed\n."

    fig = go.Figure(data = [go.Candlestick(x=data.index,
                                           open=data['1. open'],
                                           high=data['2. high'],
                                           low=data['3. low'],
                                           close=data['4. close'],
                                           name = 'Candlestick')])
    fig.layout.update(title=f'Intraday Time Series of {ticker}',)
    candle = plot(fig, output_type='div')
    return candle


# Réalisation du 2e graphique "Closed prices" dans home.html
def scatter(ticker, ts):
    ticker = ticker.upper()
    try:
        data, meta_data = ts.get_daily(ticker, outputsize='compact')
    except ValueError as e:
        print(e)
        return "Scatter chart can't be displayed.\n"
    fig = go.Figure(data = [go.Scatter(x=data.index,
                                       y=data['4. close'],
                                       name='Close price',
                                       line=dict(color='#566fff'))])
    fig.add_trace(go.Scatter(x=data.index,
                             y=data['1. open'],
                             name='Open price',
                             line=dict(color='#f4b684')))
    fig.layout.update(title=f'Opening & Closing prices for {ticker}', autosize=True,)
    fig.update_xaxes(rangeslider_visible=False,)
    scatter = plot(fig, output_type='div')
    return scatter


# Pour que l'utilisateur enregistre son compte sur le site
def register(req):
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)  # on hash le mdp
            user.save()
            user = authenticate(username=username, password=raw_password)
            login(req, user)
            wallet = Wallet(wallet=25000, user=req.user)  # on a un wallet de 25k quand on s'enregistre
            wallet.save()
            messages.success(req, ("Account created succesfully.\nYou're now logged in."))
            return redirect(home)
    else:
        form = RegisterForm()
    return render(req, 'register.html', {'form': form})


# View d'identification
def user_login(req):
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            clean_un = form.cleaned_data['username']
            clean_pw = form.cleaned_data['password']
            user = authenticate(req, username=clean_un,
                                password=clean_pw)
            if user is not None:  # si l'utilisateur existe bien...
                if user.is_active:
                    login(req, user)
                    messages.success(req, "Logged in successfully.")
                    return redirect(home)
                else:
                    messages.error(req, "Account is disabled")
                    return redirect(home)
            else:   # si l'utilisateur n'existe pas...
                messages.error(req, "Invalid login")
                return redirect(user_login)
    else:
        form = LoginForm()
    return render(req, 'login.html', {'form': form})


# View pour se déconnecter
def user_logout(req):
    logout(req)
    messages.success(req, "Logged out successfully!")
    return render(req, 'logged_out.html', {})

#View pour afficher le profile (ne s'affiche que si on est connecté)
@login_required
def profile(req):
    if req.method == 'POST':
        user_form = UpdateUserForm(req.POST, instance=req.user)
        profile_form = UpdateProfileForm(req.POST, req.FILES, instance=req.user.profile)
        change_pswd_form = PasswordChangeForm(req.user, req.POST)
            
        #Soit on update l'email, le nom d'utilisateur et la photo
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(req, "Profile updated succesfully!")
            return redirect(profile)
        #soit on update le password 
        elif change_pswd_form.is_valid():
            user = change_pswd_form.save()
            update_session_auth_hash(req, user)
            messages.success(req, "Password updated succesfully!")
            return redirect(profile)
        else:
            messages.error(req, "Something went wrong!")
            
    else:
        user_form = UpdateUserForm(instance=req.user)
        profile_form = UpdateProfileForm(instance=req.user.profile)
        change_pswd_form = PasswordChangeForm(req.user)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'change_pswd_form': change_pswd_form
    }
    
    return render(req, 'profile.html', context)

