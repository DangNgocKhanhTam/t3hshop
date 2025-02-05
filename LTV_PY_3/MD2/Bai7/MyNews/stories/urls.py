from django.urls import path
from . import views
app_name = 'stories'
urlpatterns = [
    path('', views.index, name='index'),
    path('category.html', views.category, name='category.html'),
    path('story.html', views.story, name='story.html'),
    path('contact.html', views.contact, name='contact.html'),
]
