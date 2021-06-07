from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('simulator', views.simulator, name="simulator"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('delete/<id>', views.delete, name="delete"),
    path('register', views.register, name="register"),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('sell_all/<id>/<int:qty>/<bought_price>/<current_price>', views.sell_all, name="sell_all"),
    path('sell', views.sell, name="sell"),
]
