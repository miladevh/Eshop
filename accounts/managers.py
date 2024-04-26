from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    # create normal users
    def create_user(self, email,phone_number, full_name, password):
        # check phone_number and email
        if not phone_number:
            raise ValueError('شماره تلفن تکراری است')
        
        if not email:
            raise ValueError('ایمیل تکراری است')
        
        # create user
        user = self.model(email= self.normalize_email(email), phone_number= phone_number, full_name= full_name)
        user.set_password(password)
        user.save(using= self._db)
        return user

    # create superuser(admin)
    def create_superuser(self, email, phone_number, full_name, password):
        user = self.create_user(email, phone_number, full_name, password)
        user.is_admin = True
        user.save(using= self._db)
        return user