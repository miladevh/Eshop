from django.shortcuts import render, redirect
from django.views import View
from .forms import ProfileEditForm
from .models import OtpCode, User
from random import randint
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


# کلاس ثبت نام کاربر
class UserSignupView(View):
    def get(self, request):
        # نمایش فرم ثبت نام به کاربر
        return render(request, 'apps/accounts/signup.html', {})

    def post(self, request):
        # دریافت اطلاعات کاربر
        if request.method == 'POST':
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            full_name = request.POST['full_name']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            # بررسی تکراری نبودن ایمیل وارد شده
            if User.objects.filter(email= email).exists():
                messages.error(request, 'ایمیل قبلا استفاده شده است. ایمیل دیگری وارد کنید')
                return redirect('accounts:signup')
            # بررسی تکراری نبودن شماره تلفن وارد شده
            if User.objects.filter(phone_number= phone_number).exists():
                messages.error(request, 'شماره وارد شده قبلا استفاده شده است. شماره دیگری وارد کنید')
                return redirect ('accounts:signup')
            # بررسی یکسان بودن رمز اول و دوم
            if password1 and password2 and password1 != password2 :
                messages.error(request, 'رمز خود را درست وارد کنید')
                return redirect('accounts:signup')
            # تولید وریفای کد 
            random_code = randint(100000, 999999)
            # ذخیره کد در پایگاه داده
            OtpCode.objects.create(phone_number= phone_number, code= random_code)
            # ذخیره اطلاعات کاربر در سیشن ها
            request.session['user_info'] = {
                'email':email,
                'phone_number':phone_number,
                'full_name':full_name,
                'password':password2
            }
            messages.success(request, 'کد ارسال شد')
            return redirect('accounts:verify_code')
        
        messages.error(request, 'اطلاعات خود را درست وارد کنید')
        return render(request, 'apps/accounts/signup.html', {})
    


# کلاس دریافت کد تایید و ساخت کاربر
class UserVerifyCode(View):
    def get(self, request):
        # نمایش فرم دریافت کد
        return render(request, 'apps/accounts/verify_code.html', {})

    def post(self, request):
        # دریافت اطلاعات کاربر از سیشن
        user_session = request.session['user_info']
        # دریافت کد تایید متناظر با شماره تلفن وارد شده
        verify_code = OtpCode.objects.get(phone_number= user_session['phone_number'])
        # بررسی درست بودن کد. اگر کد درست بود کاربر ایجاد میشه
        if request.method == 'POST':
            code = request.POST['code']
            if int(code) == verify_code.code:
                User.objects.create_user(
                    user_session['email'],
                    user_session['phone_number'],
                    user_session['full_name'],
                    user_session['password'],
                )
                verify_code.delete()
                messages.success(request, 'شما ثبت نام شدید')
                return redirect('home:home')
            else:
                messages.error(request, 'کد را درست وارد کنید ')
                return redirect('accounts:verify_code')
        return redirect('home:home')



# کلاس ورود کاربر
class UserLoginView(View):
    def get(self, request):
        # نمایش فرم تاگین
        return render(request, 'apps/accounts/login.html', {})

    def post(self, request):
        # دریافت اطلاعات از کاربر
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            # بررسی وجود کاربر با اطلاعات وارد شده
            user = authenticate(request, email= email, password= password) #اگر کاربر وجود نداشته باشه مقدادNoneرو برمیگردونه
            if user is not None:
                login(request, user)
                messages.success(request, 'باموفقیت وارد شدید')
                return redirect('home:home')
            else:
                messages.error(request, 'اطلاعات خود را صحیح وارد کنید')
                return redirect('accounts:login')
        else:
            return render(request, 'apps/accounts/login.html', {})



# کلاس خروج کاربر
class UserLogoutView(View, LoginRequiredMixin):
    def get(self, request):
        logout(request)
        messages.success(request, 'با موفقیت خارج شدید')
        return redirect('home:home')


# نمایش پروفایل
class UserProfileView(View, LoginRequiredMixin):
    def get(self, request):
        # گرفتن اطلاعات یوزری که الان لاگین هست
        user = request.user.profile
        return render(request, 'apps/accounts/profile.html', {'profile':user})


# ویرایش پروفایل
class UserProfileEdit(View, LoginRequiredMixin):
    form = ProfileEditForm
    def get(self, request):
        # نمایش فرم ویرایش به همراه اطلاعاتی که در حال حاظر وجود دارند
        edit_form = self.form(instance=request.user.profile, initial={'full_name':request.user.full_name, 'phone_number':request.user.phone_number})
        return render(request, 'apps/accounts/editprofile.html', {'form':edit_form})

    def post(self, request):
        # ذخیره اطلاعات مدل پروفایل
        form = self.form(request.POST, instance=request.user.profile)
        if form.is_valid:
            form.save()
            # ذخیره اطلاعاتی که در مدل پروفایل به ان دسترسی نداریم
            request.user.full_name = form.cleaned_data['full_name']
            request.user.phone_number = form.cleaned_data['phone_number']
            request.user.save()
            return redirect('accounts:user-profile')
            








