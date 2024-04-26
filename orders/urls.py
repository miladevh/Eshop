from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart_add/', views.CartAddView.as_view(), name='cart-add'),
    path('cart_remove/<int:product_id>', views.CartRemoveView.as_view(), name='cart-remove'),
]