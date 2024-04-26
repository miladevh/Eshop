from django.db import models
from home.models import Product
from django.contrib.auth import get_user_model


class Orders(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    send = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('send', '-updated')

    def __str__(self):
        return f'{self.user} - {self.id}'
    
    def get_total_price(self):
        return sum(item.get_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quty = models.IntegerField(default=1)
    
    def __str__(self):
        return self.id
    
    def get_price(self):
        return self.price * self.quty