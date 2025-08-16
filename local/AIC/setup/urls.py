from django.urls import path

from . import views

urlpatterns = [
    path('', views.setup, name="setup"),
    path('success/', views.success, name="success"),
    path('failed/', views.failed, name="failed"),
]