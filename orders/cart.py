from home.models import Product



CART_SESSION_ID = 'cart'

class Cart:
    # ساخت یک سیشن برای کاربر
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    # اضافه کردن محصول به سیشن
    def add(self, product, qty):
        product_id = str(product.id)
        # اگر محصول در سیشن کاربر وجود نداشت اضافه میکنیم
        if product_id not in self.cart:
            self.cart[product_id] = {'price':str(product.price), 'qty':0}
        self.cart[product_id]['qty'] += int(qty)
        self.save()

    # ایتریبل کردن کلاس کارت برای حلقه فور زدن روش
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)
        cart = self.cart.copy()
        # در سیشن یک فیلد پروداکت اضافه کردم و برابر با اسم محصول قرار دادم
        for product in products:
            cart[str(product.id)]['product'] = product
        # جمع قیمت هر محصول
        for item in cart.values():
            item['total_price'] = int(item['price']) * item['qty']
            yield item
    # عمل سیو بر روی سیشن
    def save(self):
        self.session.modified = True
    # قیمت کل سفارشات
    def total_price(self):
        return sum(int(item['price']) * item['qty'] for item in self.cart.values())
    # حذف از سبد خرید
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    # تعداد محصولات موجود در سبد خرید
    def __len__(self):
        return sum( item['qty'] for item in self.cart.values())