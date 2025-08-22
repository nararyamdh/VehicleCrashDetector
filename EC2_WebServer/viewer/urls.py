from django.urls import path

from . import views

urlpatterns = [
    path('<int:id_x>/', views.viewer, name="viewer"),
    path('<int:id_x>/captures/', views.captures, name="captures"),
    path('<int:id_x>/manual/', views.manual, name="manual"),
    path('<int:id_x>/metrics/', views.metrics, name="metrics"),
    path('<int:id_x>/alarm/', views.alarm, name="alarm"),
]