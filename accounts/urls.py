from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('verify/', views.UserVerifyCode.as_view(), name='verify_code'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('edit_profile/', views.UserProfileEdit.as_view(), name='edit-profile')
]