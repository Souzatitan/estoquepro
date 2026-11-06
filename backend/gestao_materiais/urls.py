from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path(
        "estoque/",
        views.lista_estoque,
        name="lista_estoque",
    ),
    path(
        "exportar/csv/",
        views.exportar_estoque_csv,
        name="exportar_estoque_csv",
    ),
]