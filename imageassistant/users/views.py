from django.shortcuts import render, redirect
from users.forms import CustomUserForm, LoginForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.urls import reverse, reverse_lazy



def signup(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return render(
                request, 'users/signup.html#signup-success', {'success': True}
            )
        else:
            for field, _ in form.errors.items():
                form.fields[field].widget.attrs['class'] += ' border-red-500'
            return render(
                request, 'users/signup.html#signup-form', {'form': form},
                status=400
            )
    return render(request, 'users/signup.html', {'form': CustomUserForm()})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form.data)
        user = authenticate(
            request, email=form.data['email'], password=form.data['password']
        )
        print(user)
        if user is not None:
            auth_login(request, user)
            return render(request, 'users/login.html#login-form', {
                'form': LoginForm(), 'target': '#login-container',
                'redirect': True
            })
        else:
            form.add_error("email", 'Invalid email or password')
            for field, _ in form.errors.items():
                form.fields[field].widget.attrs['class'] += ' border-red-500'
            return render(
                request, 'users/login.html#login-form', {'form': form}, status=400
            )
    return render(request, 'users/login.html', {'form': LoginForm()})


def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                domain_override=settings.EMAIL_DOMAIN, from_email="no-reply@imageassistant.io",
                email_template_name="users/password_reset_email.html",
            )
            return render(
                request, 'users/change_password.html#password-reset-form',{
                    'form': CustomPasswordResetForm(),
                    'target': '#change-password-form-container',
                    'success': True
                }
            )
        else:
            for field, _ in form.errors.items():
                form.fields[field].widget.attrs['class'] += ' border-red-500'
            return render(
                request, 'users/change_password.html#password-reset-form', {
                    'form': form,
                    'target': '#change-password-form-container'
                }
            )
    return render(request, 'users/change_password.html', {'form': CustomPasswordResetForm()})


class PasswordResetCustomConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    form_class = CustomPasswordResetConfirmForm
    domain_override = settings.EMAIL_DOMAIN
    success_url = reverse_lazy("users:password-reset-complete")
    template_name = "users/password_reset_confirm.html"


class PasswordResetCustomCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = reverse('users:login')
        return context