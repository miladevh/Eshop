from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # User manager
    objects = UserManager()

    # for login field
    USERNAME_FIELD = 'email'
    # for createsuperuser
    REQUIRED_FIELDS = ['phone_number', 'full_name']

    def __str__(self):
        return self.email
    
    # user permission
    def has_perm(self, perm, obj=None):
        return True
    
    # user have permissions to view the app
    def has_module_perms(self, app_label):
        return True
    
    # user is admin
    @property
    def is_staff(self):
        return self.is_admin
    


# ذخیره کد یکبارمصرف
class OtpCode(models.Model):
    phone_number = models.CharField(max_length= 11)
    code = models.PositiveBigIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.TextField(null=True, blank=True)
    balance = models.BigIntegerField(default=10000)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(receiver=create_profile, sender=User )