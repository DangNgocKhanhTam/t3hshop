"""MyStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from store import views
from orders import views as orders_views

router = routers.DefaultRouter()
router.register(r'store', views.ProductViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('order/create/', orders_views.order_create, name='order_create'),
    path('order/', include('orders.urls', namespace='orders')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    path('dashboard/', include('dashboard.urls')),
    path('analysis/', include('analysis.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)