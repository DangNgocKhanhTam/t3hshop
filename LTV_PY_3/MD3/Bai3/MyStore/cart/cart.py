from decimal import Decimal
from django.conf import settings
from store.models import Product

class Cart(object):
    def __init__(self, request):
        """Khởi tạo giỏ hàng từ session"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Thêm sản phẩm vào giỏ hàng hoặc cập nhật số lượng"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Đánh dấu session là đã thay đổi để lưu giỏ hàng"""
        self.session.modified = True

    def remove(self, product):
        """Xóa sản phẩm khỏi giỏ hàng"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Lặp qua các sản phẩm trong giỏ hàng và tính toán tổng giá trị"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Trả về tổng số lượng sản phẩm trong giỏ hàng"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Tính tổng giá trị của giỏ hàng"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Xóa giỏ hàng khỏi session"""
        del self.session[settings.CART_SESSION_ID]
        self.save()