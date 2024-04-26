from django.contrib import admin
from .models import OrderItem, Orders


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'updated', 'send')
    list_filter = ('send',)
    inlines = (OrderItemInline,)
