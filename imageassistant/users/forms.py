from users.models import CustomUser
from django import forms
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
import re


class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'confirm_password', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs['class'] = 'mt-1 block text-[#202943]  w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-color focus:border-primary-color sm:text-sm'

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            self.add_error('email', 'Email already exists')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
        return super().clean()
    
    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        labels = {
            'email': 'Email Address',
            'password': 'Password'
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs['class'] = 'mt-1 block text-[#202943]  w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-color focus:border-primary-color sm:text-sm'


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField()

    class Meta:
        labels = {
            'email': 'Email Address',
        }

    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs['class'] = 'mt-1 block text-[#202943]  w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-color focus:border-primary-color sm:text-sm'
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email does not exist')
        return email



class CustomPasswordResetConfirmForm(SetPasswordForm):

    def __init__(self, user, *args, **kwargs):
        super(CustomPasswordResetConfirmForm, self).__init__(user, *args, **kwargs)
        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs['class'] = 'mt-1 block text-[#202943]  w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-color focus:border-primary-color sm:text-sm'