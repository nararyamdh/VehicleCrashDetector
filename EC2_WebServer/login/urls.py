from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view, name="login"),
    path('mfa/', views.MFA, name="mfa"),
    path('begin-login/', views.begin_login, name="begin_login"),
    path('finish-login/', views.finish_login, name="finish_login"),
]