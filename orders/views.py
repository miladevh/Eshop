from django.shortcuts import render, redirect, get_object_or_404
from home.models import Product
from django.views import View
from .cart import Cart
from django.http import JsonResponse

class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'apps/orders/cart.html', {'cart':cart})



class CartAddView(View):
    def post(self, request):
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            product_id = request.POST.get('product_id')
            product_qty = request.POST.get('product_qty')
            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product, qty=product_qty)

            response = JsonResponse({'qty':product_qty})
            return response
        return redirect('orders:cart-add')
        

class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id= product_id)
        cart.remove(product=product)
        return redirect('orders:cart')