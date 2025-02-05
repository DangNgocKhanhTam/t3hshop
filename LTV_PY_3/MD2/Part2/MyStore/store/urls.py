from django.urls import path
from . import views
app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('', views.category, name='category.html'),
    # # path('story.html', views.story, name='story.html'),
    # path('story.html/<int:a>/', views.story, name='story.html'),
    # path('contact.html', views.contact, name='contact.html'),
]
