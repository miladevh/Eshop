from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

# دسته بندی محصولات
class Categoty(models.Model):
    name = models.CharField(max_length= 200)
    slug = models.SlugField(max_length= 200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    # ساخت اسلاگ برای هر کتگوری
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)
    # ساخت url
    def get_absolute_url(self):
        return reverse('home:one-category', args=[self.slug,])

    def __str__(self):
        return self.name
    
# محصولات
class Product(models.Model):
    category = models.ForeignKey(Categoty, on_delete= models.CASCADE, related_name= 'products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length= 200, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/')
    disription = models.TextField()
    price = models.BigIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.BigIntegerField(default=0)

    class Meta:
        ordering = ('name',)
    # ساخت اسلاگ برای هر محصول
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    # ساخت url
    def get_absolute_url(self):
        return reverse('home:product-details', args=[self.slug,])