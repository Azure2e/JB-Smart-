from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.lista, name="lista"),
    path("carrinho/", views.carrinho_view, name="carrinho"),
    path("carrinho/adicionar/<int:pk>/", views.adicionar, name="adicionar"),
    path("carrinho/atualizar/<int:pk>/", views.atualizar, name="atualizar"),
    path("carrinho/remover/<int:pk>/", views.remover, name="remover"),
    path("checkout/", views.checkout, name="checkout"),
    path("encomenda/<int:pk>/", views.encomenda_ok, name="encomenda_ok"),
    path("encomendas/", views.encomendas, name="encomendas"),
    path("registo/", views.registo, name="registo"),
    path("entrar/", auth_views.LoginView.as_view(), name="login"),
    path("sair/", auth_views.LogoutView.as_view(), name="logout"),
    path("manifest.json", views.manifest, name="manifest"),
    path("sw.js", views.service_worker, name="sw"),
    path("offline/", views.offline, name="offline"),
    path("dias-d/", views.dias_d, name="dias_d"),
]
