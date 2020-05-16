from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def check_topic_owner(topic, request):
    if topic.owner != request.user:
        raise Http404

def index(request):
	"""Домашняя страница приложения geospatial_log"""
	return render(request, 'geospatial_logs/index.html')

@login_required
def topics(request):
    """Выводит список тем"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'geospatial_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Выводит одну тему и все ее записи"""
    topic = Topic.objects.get(id=topic_id)
    # Проверка принадлежности темы текущему пользователю
    # if topic.owner != request.user:
    #     raise Http404
    check_topic_owner(topic, request)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'geospatial_logs/topic.html', context)

@login_required
def new_topic(request):
    """Определяет новую тему"""
    if request.method != 'POST':
        # Данные не отправлялись - создается пустая форма.
        form = TopicForm()
    else:
        # Отправлены данные POST - надо обработать.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('geospatial_logs:topics'))
    context = {'form':form}
    return render(request, 'geospatial_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Добавляет новую запись по выбранной теме"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # Данные не отправлялись - создается пустая форма.
        form = EntryForm()        
    else:
        # Отправлены данные POST - надо обработать.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            check_topic_owner(topic, request)
            new_entry.save()
            return HttpResponseRedirect(reverse('geospatial_logs:topic',
                                        args=[topic_id]))
    
    context = {'topic': topic, 'form': form}
    return render(request, 'geospatial_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # Проверка принадлежности темы текущему пользователю
    # if topic.owner != request.user:
    #     raise Http404
    check_topic_owner(topic, request)
    if request.method != 'POST':
        # Исходный запрос. Форма заполняется текущими данными записи.
        form = EntryForm(instance=entry)
    else:
        # Отправлены данные POST - надо обработать.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('geospatial_logs:topic', args=[topic.id]))
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'geospatial_logs/edit_entry.html', context)