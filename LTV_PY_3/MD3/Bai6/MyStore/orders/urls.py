# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders'  # Đảm bảo khai báo app_name

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    # Các URL khác của ứng dụng orders
]
