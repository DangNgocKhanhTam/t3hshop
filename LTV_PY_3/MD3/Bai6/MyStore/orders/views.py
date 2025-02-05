from django.shortcuts import render
from cart.cart import Cart  # Import Cart class
from .models import OrderItem, Order  # Import models
from .forms import OrderCreateForm  # Import OrderCreateForm
from store import models  # Import store models if needed
from django.core.mail import EmailMultiAlternatives  # Import email sending tools
from MyStore.settings import EMAIL_HOST_USER  # Import email host settings

subcategory_list = models.SubCategory.objects.all()

def order_create(request):
    cart = Cart(request)
    username = request.session.get('username', 0)

    if username:
        user = models.User.objects.get(username=username)
        user_profile = models.UserProfileInfo.objects.get(user=user)
        order = Order()
        order.username = user.username
        order.first_name = user.first_name
        order.last_name = user.last_name
        order.email = user.email
        order.phone = user_profile.phone
        order.address = user_profile.address
    else:
        order = Order()

    if request.method == 'POST':
        form = OrderCreateForm(request.POST, cart=cart)
        if form.is_valid():
            order = form.save()
            # Save each item in the cart as OrderItem
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Tạo danh sách chi tiết đơn hàng để gửi trong email
            order_items = ''
            total_cost = 0
            for item in order.items.all():
                order_items += f"{item.quantity} x {item.product.name} - {item.price} d\n"
                total_cost += item.quantity * item.price

            # Gửi email xác nhận đơn hàng
            email_address = form.cleaned_data['email']
            subject = 'Xác nhận đơn hàng ' + str(order.id)
            message = f"""
            Cảm ơn quý khách {order.first_name} {order.last_name} đã đặt hàng tại Eshop.
            
            Thông tin đơn hàng:
            Đơn hàng ID: {order.id}
            Phone: {order.phone}
            Email: {order.email}
            Địa chỉ giao hàng: {order.address}
            
            Chi tiết đơn hàng:
            {order_items}
            
            Tổng đơn hàng: {total_cost} d
            Trân trọng, Eshop.
            """

            # Tạo email
            reciepient = str(email_address)
            msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [reciepient])
            msg.send()

            # Xóa giỏ hàng sau khi đặt
            cart.clear()

            return render(request, 'orders/order/create.html', {'order': order, 'subcategories': subcategory_list, 'username': username, 'cart': cart, 'form': form})

    else:
        form = OrderCreateForm(cart=cart)

    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form, 'subcategories': subcategory_list, 'username': username})
