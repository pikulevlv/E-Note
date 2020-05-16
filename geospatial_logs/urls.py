from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'homepage'

urlpatterns = [
	# Домашняя страница
	url(r'^$', views.index, name='index'),
	# Страница со списком тем
	url(r'^topics/$', views.topics, name='topics'),
	# Страница с выводом информации по отдельнйой теме
	url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
	# Страница для добавления новой темы
	url(r'^new_topic/$', views.new_topic, name='new_topic'),
	# Страница для добавления новой записи
	url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
	# Страница для редактирования записи
	url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
]
