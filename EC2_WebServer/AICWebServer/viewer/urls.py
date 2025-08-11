from django.urls import path

from . import views

urlpatterns = [
    path('', views.viewer, name="viewer"),
    path('captures/', views.captures, name="captures"),
    path('recognized/', views.recognized, name="recognized"),
    path('alarm/', views.alarm, name="alarm"),
]