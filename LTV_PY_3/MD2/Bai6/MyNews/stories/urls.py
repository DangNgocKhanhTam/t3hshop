from django.urls import path
from . import views
app_name = 'stories'
urlpatterns = [
    path('', views.index, name='index'),
    path('category.html/<int:pk>/', views.category, name='category.html'),
    # path('story.html', views.story, name='story.html'),
    path('story.html/<int:a>/', views.story, name='story.html'),
    path('contact.html', views.contact, name='contact.html'),
]
