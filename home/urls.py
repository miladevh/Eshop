from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('<slug:slug>', views.ProductDetailsView.as_view(), name='product-details'),
    path('category/<slug:cat_slug>', views.HomePageView.as_view(), name='one-category'),
    path('searchitem/', views.SearchItemView.as_view(), name='search-item'),
]