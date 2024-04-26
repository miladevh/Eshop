from django import forms
from .models import  UserProfile


class ProfileEditForm(forms.ModelForm):
    full_name = forms.CharField()
    phone_number = forms.CharField()
    class Meta:
        model = UserProfile
        fields = ('address',)