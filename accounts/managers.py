from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    # ساخت یوزر معمولی
    def create_user(self, email,phone_number, full_name, password):
        # بررسی شماره و ایمیل
        if not phone_number:
            raise ValueError('شماره تلفن تکراری است')
        
        if not email:
            raise ValueError('ایمیل تکراری است')
        
        # ساخت یوزر
        user = self.model(email= self.normalize_email(email), phone_number= phone_number, full_name= full_name)
        user.set_password(password)
        user.save(using= self._db)
        return user

    # ساخت سوپر یوزر - ادمین
    def create_superuser(self, email, phone_number, full_name, password):
        user = self.create_user(email, phone_number, full_name, password)
        user.is_admin = True
        user.save(using= self._db)
        return user