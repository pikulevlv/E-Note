"""Определяет схемы URL для пользователей"""
from django.conf.urls import url
from django.contrib.auth import login

from django.contrib.auth.views import LoginView


from . import views

app_name = 'users'

urlpatterns = [
    # Страница входа.
    # url(r'^login/$', login, {'template_name': 'users/login.html'}, name='login')]
    url(r'^login/$', LoginView.as_view(template_name='users/login.html'), name='login'),
    # Страница выхода.
    url(r'^logout/$', views.logout_view, name='logout'),
    # Страница регистрации.
    url(r'^register/$', views.register, name='register'),

]