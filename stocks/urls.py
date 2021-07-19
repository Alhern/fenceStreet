from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('simulator', views.simulator, name="simulator"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('delete/<id>', views.delete, name="delete"),
    path('register', views.register, name="register"),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('profile', views.profile, name="profile"),
    path('sell_all/<id>', views.sell_all, name="sell_all"),
    path('sell', views.sell, name="sell"),
]

#Pour afficher les statics pendant la phase de dev (pour les images de profile)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
