from django.urls import path
from . import views

urlpatterns = [
    path('', views.work_with_series),
    path('dataframe', views.work_with_dataframe),   
    path('chart', views.work_with_chart_1),
]
