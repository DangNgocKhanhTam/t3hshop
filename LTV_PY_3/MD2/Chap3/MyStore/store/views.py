import datetime

from . import models
import re
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, F, Value
from .forms import FormSearch


# Create your views here.
from django.http import HttpResponse

subcategory_list = models.SubCategory.objects.all()

def index(request):
    tbgd = models.SubCategory.objects.filter(category=1)
    ddnb = models.SubCategory.objects.filter(category=2)
    product_list = models.Product.objects.order_by("-public_day")
    most_viewed_list = models.Product.objects.order_by("-viewed")[:3]
    newest = product_list[0]
    twenty_newest = product_list[:20]

    return render(request, "store/index.html",
                  {'newest': newest,
                   'twenty_newest': twenty_newest,
                   'most_viewed_list': most_viewed_list,
                   'subcategories': subcategory_list,
                   'tbgd': tbgd,
                   'ddnb': ddnb
                   })


def shop(request, pk):
    product_list = []
    subcategory_name = ''
    if pk != 0:
        product_list = models.Product.objects.filter(
            subcategory=pk).order_by("-public_day")
        selected_sub = models.SubCategory.objects.get(pk = pk)
        subcategory_name = selected_sub.name
    else:
        product_list = models.Product.objects.order_by("-public_day")

    three_newest = product_list[:3]

    page = request.GET.get('page', 1)  # trang bat dau
    paginator = Paginator(product_list, 9)  # so product/trang

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, "store/shop.html",
                  {'three_newest': three_newest,
                   'subcategories': subcategory_list,
                   'products': products,
                   'pk': pk,
                   'subcategories': subcategory_list,
                   'subcategory_name': subcategory_name,
                   })


def product_detail(request, pk):
    product_select = models.Product.objects.get(pk=pk)
    # khi người dùng chọn xem 1 sản phẩm > tăng view của sản phẩm thêm 1
    models.Product.objects.filter(pk=product_select.pk).update(viewed=F('viewed') + 1)
    product_select.refresh_from_db()
    return render(request, "store/product.html",
                  {'product': product_select,
                   'subcategories': subcategory_list,
                   })


def cart(request):
    return render(request, 'store/cart.html',
                  {'subcategories': subcategory_list,
                   })


def checkout(request):
    return render(request, 'store/checkout.html',
                  {'subcategories': subcategory_list,
                   })


def contact(request):
    return render(request, 'store/contact.html',
                  {'subcategories': subcategory_list, }
                  )

def show_base(request):
    return render(request, 'store/base.html'
                  )

def search_form(request):
    global subcategory
    global search_str
    product_items = 0
    three_newest = models.Product.objects.all().order_by("-public_day")[:3]
    product_list = []

    if request.method == 'GET':
        form =FormSearch(request.GET)
        if form.is_valid():
            subcategory = form.cleaned_data['subcategory_id']
            search_str = form.cleaned_data['name']
            if subcategory != 0:
                product_list = models.Product.objects.filter(
                    subcategory=subcategory, name__contains=search_str
                ).order_by("-public_day")
            else:
                product_list = models.Product.objects.filter(
                    name__contains=search_str
                ).order_by("-public_day")
            product_items = len(product_list)

            page = request.GET.get('page', 1)
            paginator = Paginator(product_list, 9)  # 9 products per page

            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)

            return render(request, "store/shop.html", {
                'three_newest': three_newest,
                'subcategories': subcategory_list,
                'products': products,
                'pk': subcategory,
                'product_items': product_items,
                'subcategory': subcategory,
                'search_str': search_str,
            })
        