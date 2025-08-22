from django.urls import path

from . import views

urlpatterns = [
    path('', views.signup, name="signup"),
    path('mfa/', views.MFA_su, name="mfa_su"),
    path('permission/', views.permission, name="permission"),
    path('begin-register', views.begin_register),
    path('finish-register', views.finish_register),
]