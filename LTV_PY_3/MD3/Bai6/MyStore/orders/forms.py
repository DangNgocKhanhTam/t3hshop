# orders/forms.py

from django import forms
from .models import Order
from cart.cart import Cart  # Import Cart to interact with cart data

class OrderCreateForm(forms.ModelForm):
    # Các trường nhập liệu thông thường
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    
    # Trường ẩn để lưu thông tin giỏ hàng
    cart_items = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        
    def __init__(self, *args, **kwargs):
        cart = kwargs.pop('cart', None)  # Get cart information
        super().__init__(*args, **kwargs)
        
        # Nếu giỏ hàng có sản phẩm, ta sẽ lưu thông tin vào trường 'cart_items'
        if cart:
            cart_data = []
            for item in cart:
                cart_data.append({
                    'product_name': item['product'].name,
                    'price': item['price'],
                    'quantity': item['quantity'],
                    'total_price': item['total_price']
                })
            self.fields['cart_items'].initial = str(cart_data)
    
    # Có thể bổ sung thêm các phương thức xử lý nếu cần
