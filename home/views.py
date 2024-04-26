from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Product, Categoty


class HomePageView(View):
    def get(self, request, cat_slug=None):
        all_product = Product.objects.filter(available=True)
        all_category = Categoty.objects.all()
        sale_product = Product.objects.filter(available=True, is_sale=True)[:7]
        if cat_slug:
            category = Categoty.objects.get(slug=cat_slug)
            all_product = all_product.filter(category=category)
        return render(request, 'apps/home/home.html', {'products': all_product, 'all_category': all_category, 'sale_product': sale_product})


class ProductDetailsView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'apps/home/product-details.html', {'product': product})


class SearchItemView(View):
    def post(self, request):
        phrase = request.POST['search_input']
        if phrase:
            results = Product.objects.filter(available=True, disription__contains= phrase)
            return render(request, 'apps/home/search_items.html', {'products':results})
        return redirect('home:home')