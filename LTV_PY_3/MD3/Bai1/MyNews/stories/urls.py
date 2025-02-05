from django.urls import path
from . import views


app_name = 'stories' 

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/', views.detail, name='detail'), 
    path('category/', views.category, name='category'),
    path('contact/', views.contact, name = 'contact'), 
    path('story/', views.story, name = 'story')
]