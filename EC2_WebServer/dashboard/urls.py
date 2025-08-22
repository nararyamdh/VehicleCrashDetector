from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('iam/', views.iam, name="iam"),
    path('sos/', views.sos, name="sos"),
    path('ds/', views.ds, name="ds"),
]