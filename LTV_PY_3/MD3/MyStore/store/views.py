from django.http import HttpResponse
from . import forms
from . import models
from cart.forms import CartAddProductForm
import datetime
import re
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, F, Value

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


import logging
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import UserForm, UserProfileInfoForm
from .models import User, UserProfileInfo

# Create your views here.

subcategory_list = models.SubCategory.objects.all()
subcategory = 0
search_str = ''


def index(request):
    username = request.session.get('username', 0)
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
                   'ddnb': ddnb,
                   'username': username
                   })


def shop(request, pk):
    username = request.session.get('username', 0)
    subcategory = pk
    product_list = []
    subcategory_name = ''
    if pk != 0:
        product_list = models.Product.objects.filter(
            subcategory=pk).order_by("-public_day")
        selected_sub = models.SubCategory.objects.get(pk=pk)
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
                   'username': username
                   })


def product_detail(request, pk):
    username = request.session.get('username', 0)
    product_select = models.Product.objects.get(pk=pk)
    # khi người dùng chọn xem 1 sản phẩm > tăng view của sản phẩm thêm 1
    models.Product.objects.filter(
        pk=product_select.pk).update(viewed=F('viewed') + 1)
    product_select.refresh_from_db()
    cart_product_form = CartAddProductForm()
    return render(request, "store/product.html",
                  {'product': product_select,
                   'subcategories': subcategory_list,
                   'username': username,
                   'cart_product_form': cart_product_form,
                   })


def cart(request):
    username = request.session.get('username', 0)
    return render(request, 'store/cart.html',
                  {'subcategories': subcategory_list,
                   'username': username
                   })


def checkout(request):
    username = request.session.get('username', 0)
    return render(request, 'store/checkout.html',
                  {'subcategories': subcategory_list,
                   'username': username
                   })


def contact(request):
    username = request.session.get('username', 0)
    return render(request, 'store/contact.html',
                  {'subcategories': subcategory_list, 'username': username}
                  )


def search_form(request):
    username = request.session.get('username', 0)
    global subcategory
    global search_str
    product_items = 0
    three_newest = models.Product.objects.all().order_by("-public_day")[:3]
    product_list = []
    if request.method == 'GET':
        form = forms.FormSearch(request.GET, models.Product)

        if form.is_valid():
            subcategory = form.cleaned_data['subcategory_id']
            search_str = form.cleaned_data['name']
            if subcategory != 0:
                product_list = models.Product.objects.filter(
                    subcategory=subcategory, name__contains=search_str).order_by("-public_day")
            else:
                product_list = models.Product.objects.filter(
                    name__contains=search_str).order_by("-public_day")

        product_items = len(product_list)

        page = request.GET.get('page', 1)
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
                       'pk': subcategory,
                       'subcategories': subcategory_list,
                       'product_items': product_items,
                       'subcategory': subcategory,
                       'search_str': search_str,
                       'username': username
                       })


def filter_by_prices(request):
    username = request.session.get('username', 0)
    global subcategory
    global search_str
    product_items = 0
    # vào được đến đây
    product_list = models.Product.objects.all().order_by("price")
    ###
    result = "chua nhan gi ca"
    three_newest = models.Product.objects.all().order_by("-public_day")[:3]
    if request.method == 'GET':
        result = "da nhan GET"
        subcategory = request.GET.get('subcategory_id_1')
        x = 'yes'
        if request.GET.get('name_1'):
            search_str = request.GET.get('name_1')
        else:
            search_str = ''
            x = 'no'
        a = float(request.GET.get('price_from'))
        b = float(request.GET.get('price_to'))
        price_from = a
        price_to = b
        if(a > b):
            price_from = b
            price_to = a

        if subcategory != '0':
            result = " da nhan category " + \
                str(subcategory) + " - " + \
                str(price_from) + " - " + str(price_to)
            if(x != 'no'):
                product_list = models.Product.objects.filter(
                    name__contains=search_str, subcategory=subcategory).order_by("price")
            else:
                product_list = models.Product.objects.filter(
                    subcategory=subcategory).order_by("price")

        if subcategory == '0':
            result = " da nhan category = 0" + str(subcategory)
            if(x != 'no'):
                product_list = models.Product.objects.filter(
                    name__contains=search_str).order_by("price")

        product_list = [product for product in product_list if product.price >=
                        price_from and product.price <= price_to]

        product_items = len(product_list)

        result = 'từ ' + \
            '{:20,.0f}'.format(price_from) + ' đ đến ' + \
            '{:20,.0f}'.format(price_to) + ' đ'

        page = request.GET.get('page', 1)
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
                       'pk': subcategory,
                       'subcategories': subcategory_list,
                       'product_items': product_items,
                       'subcategory': subcategory,
                       'search_str': search_str,
                       'result': result,
                       'username': username
                       })


def sign_in(request):
    # registered = False
    # if request.method == "POST":
    #     form_cus = forms.FormCustumer(data=request.POST)
    #     if (form_cus.is_valid() and (form_cus.cleaned_data['password'] == form_cus.cleaned_data['confirm'])):
    #         user = form_cus.save()
    #         user.save()
    #         registered = True

    #     if (form_cus.cleaned_data['password'] != form_cus.cleaned_data['confirm']):
    #         form_cus.add_error('confirm', 'Password và confirm password khác nhau!!!')
    #         print(form_cus.errors)
    # else:
    #     form_cus = forms.FormCustumer()

    registered = False
    if request.method == "POST":
        form_user = forms.UserForm(data=request.POST)
        form_por = forms.UserProfileInfoForm(data=request.POST)
        if (form_user.is_valid() and form_por.is_valid() and form_user.cleaned_data['password'] == form_user.cleaned_data['confirm']):
            user = form_user.save()
            user.set_password(user.password)
            user.save()

            profile = form_por.save(commit=False)
            profile.user = user
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            profile.save()

            registered = True
        if form_user.cleaned_data['password'] != form_user.cleaned_data['confirm']:
            form_user.add_error(
                'confirm', 'Password và confirm password không giống nhau!')
            print(form_user.errors, form_por.errors)
    else:
        form_user = forms.UserForm()
        form_por = forms.UserProfileInfoForm()

    username = request.session.get('username', 0)
    return render(request, 'store/signin.html',
                  {'subcategories': subcategory_list,
                   'form_user': form_user,
                   'form_por': form_por,
                   'registered': registered,
                   'username': username}
                  )


def log_in(request):
    # if request.method == "POST":
    #     username = request.POST.get("username")
    #     password = request.POST.get("password")
    #     user = models.Customer.objects.filter(username=username, password=password)
    #     if user is not None:
    #         result = "Xin chào quý khách " + username
    #         request.session['username'] = username
    #         username = request.session.get('username', 0)
    #         return render(request, "store/login.html", {'login_result': result,
    #                                                       'username': username})
    #     else:
    #         login_result = "Username hoặc password không chính xác."
    #         return render(request, "store/login.html", {'login_result': login_result})
    # else:
    #     return render(request, "store/login.html")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            result = "Hello " + username
            request.session['username'] = username
            username = request.session.get('username', 0)
            return render(request, "store/login.html", {'login_result': result,
                                                        'username': username,
                                                        })
        else:
            print("You can't login.")
            print("Username: {} and password: {}".format(username, password))
            login_result = "Username hoặc password không chính xác!"
            return render(request, "store/login.html", {'login_result': login_result})
    else:
        return render(request, "store/login.html")


@login_required
def log_out(request):
    # try:
    #     del request.session['username']
    # except KeyError:
    #     pass
    # logout = "Quý khách đã logout. Quý khách có thể login trở lại"
    # return render(request, "store/login.html", {'logout': logout})
    logout(request)
    result = "Quý khách đã logout. Quý khách có thể login trở lại"
    return render(request, "store/login.html", {'logout_result': result})


logger = logging.getLogger(__name__)

def register(request):
    registered = False  # Biến này sẽ theo dõi trạng thái đăng ký

    # Kiểm tra xem request là POST không
    logger.debug("Register view called - Method: {}".format(request.method))

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST, request.FILES)

        # Kiểm tra xem form có hợp lệ không
        if user_form.is_valid() and profile_form.is_valid():
            logger.debug("Forms are valid. Saving data...")

            # Lưu thông tin người dùng
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Gửi email xác nhận đăng ký thành công
            subject = 'Chúc mừng bạn đã đăng ký thành công!'
            message = f'Xin chào {user.first_name},\n\nBạn đã đăng ký thành công tài khoản trên trang web của chúng tôi.'
            from_email = 'tamdangngoc0707@gmail.com'
            recipient_list = ['trangdangngoc0707@gmail.com']

            try:
                send_mail(subject, message, from_email, recipient_list)
                logger.debug("Email sent successfully.")
            except Exception as e:
                logger.error(f"Error sending email: {e}")

            registered = True  # Đánh dấu là đã đăng ký thành công

            # Chuyển hướng đến trang đăng nhập hoặc trang xác nhận
            return redirect('store:signin.html')

        else:
            # Nếu form không hợp lệ, log lỗi
            logger.error("Form is not valid. Errors: {}".format(user_form.errors))

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # Render lại trang với thông tin đã truyền vào
    return render(request, 'store/signin.html', {
        'form_user': user_form, 
        'form_por': profile_form, 
        'registered': registered  # Truyền biến registered vào template
    })



