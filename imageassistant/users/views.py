from django.shortcuts import render, redirect

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.views.generic import FormView
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from users.models import CustomUser, BaredUser, Credit
from users.forms import (
    CustomUserForm, LoginForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm,
    AddCreditForm
)
from users.tasks import send_email_task
import stripe
import logging
import requests
import json
logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

def privacy_policy(request):
    """
        Render the privacy policy page
    """
    return render(request, 'users/privacy_policy.html')


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
    return render(request, 'users/signup.html', {
        'form': CustomUserForm(),
        'GOOGLE_LOGIN_REDIRECT_URI': settings.GOOGLE_LOGIN_REDIRECT_URI,
        'google_client_id': settings.GOOGLE_CLIENT_ID
    })


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = authenticate(
            request, email=form.data['email'], password=form.data['password']
        )
        if user is not None:
            # check if the user has been banned
            if BaredUser.objects.filter(user=user).exists():
                form.add_error("email", 'Your account has been banned, contact us for more information')
                for field, _ in form.errors.items():
                    form.fields[field].widget.attrs['class'] += ' border-red-500'
                return render(
                    request, 'users/login.html#login-form', {'form': form}, status=400
                )
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
    return render(request, 'users/login.html', {
        'form': LoginForm()
    })


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
                    'target': '#change-password-form-container',
                    'success': False
                }
            )
    print("GET request to change password")
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


@csrf_exempt
def google_login(request):
    """
        Handle Google Sign-In callback
    """
    if request.method != 'POST':
        logger.error("Google login endpoint hit with non-POST method")
        return redirect('users:login')
    else:

        # Get the credential from the POST data
        credential = request.POST.get('credential')

        if not credential:
            logger.error("No credential found in request")
            return redirect('users:login')
        try:
            # Verify the token with Google
            response = requests.get(
                f'https://oauth2.googleapis.com/tokeninfo?id_token={credential}'
            )

            if response.status_code != 200:
                logger.error(f"Failed to verify token: {response.status_code} - {response.text}")
                return redirect('users:login')

            # Extract user info from the token
            user_data = response.json()
            
            # Check if required fields exist
            email = user_data.get('email')
            if not email or not user_data.get('email_verified'):
                logger.error("Email not verified or not provided")
                return redirect('custom_users:login')
            
            # Check if user exists or create new user
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                # Create a new user
                user = CustomUser.objects.create_user(
                    email=email,
                    first_name=user_data.get('given_name', ''),
                    last_name=user_data.get('family_name', ''),
                    # Set unusable password as user will login via Google
                    password=None
                )
                user.set_unusable_password()
                user.save()
                logger.info(f"Created new user with email: {email}")
            # check if the user has been banned
            if BaredUser.objects.filter(user=user).exists():
                messages.error(request, 'Your account has been banned')
                logger.warning(f"User {user.email} attempted to login but is banned.")
                return redirect('users:login')
            auth_login(request, user)
            logger.info(f"User {email} logged in via Google")

            # Redirect to dashboard
            return redirect('images:dashboard')
        except Exception as e:
            logger.exception(f"Error in Google login: {str(e)}")
            return redirect('custom_users:login')
        

class DeleteUserView(DeleteView):
    """
        View to handle user deletion
    """
    model = CustomUser
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        """
            Handle GET request to delete user
        """
        user = self.get_object()
        if user == request.user:
            # log user out
            auth_logout(request)
            user.delete()
            messages.success(request, "Your account has been deleted successfully. All your data has been removed from our servers.")
            return redirect('base')
        else:
            messages.error(request, "You cannot delete this account.")
            return redirect('base')


class AddCreditView(FormView):
    """
        View to handle adding credit to a user
    """
    success_url = reverse_lazy('users:add-credit')
    template_name = 'users/add_credit.html'
    form_class = AddCreditForm

    def form_valid(self, form):
        """
            Handle valid form submission
        """
        user = self.request.user
        amount = form.cleaned_data['amount']
        payment_intent_id = self.request.GET.get('payment_intent_id')
        payment_intent_created = self.request.GET.get('payment_intent_created')
        print( payment_intent_id)
        # Add credit to user's account
        # credits purchased
        print("Trying to set credits")
        total_credits = int(settings.CREDIT_SETTINGS * amount)
        credit, created = Credit.objects.get_or_create(user=user, defaults={'total':total_credits})
        if not created:
            credit.total += total_credits
            credit.save()
        
        messages.success(self.request, f"${total_credits} credit added successfully.")
        send_email_task.delay(
            user_id=user.id,
            amount=form.cleaned_data['amount'],
            credits_received=total_credits,
            payment_intent_id=payment_intent_id,
            payment_intent_created=payment_intent_created
        )
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        context['credit_multiplier'] = settings.CREDIT_SETTINGS
        return context
    
    # def post(self, request, *args, **kwargs):
    #     # Check if this is a payment success callback
    #     payment_intent_id = request.POST.get('payment_intent_id')
    #     payment_status = request.POST.get('payment_status')
        
    #     if payment_intent_id and payment_status == 'succeeded':
    #         return self.handle_payment_success(request, payment_intent_id)
        
    #     return super().post(request, *args, **kwargs)

    # def handle_payment_success(self, request, payment_intent_id):
    #     try:
    #         # Verify payment with Stripe
    #         payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
    #         if payment_intent.status == 'succeeded':
    #             user = request.user
    #             amount = float(payment_intent.metadata.get('credit_amount', 0))
                
    #             # Add credits to user account
    #             credit_amount = int(settings.CREDIT_SETTINGS * amount)
    #             credit, created = Credit.objects.get_or_create(
    #                 user=user, 
    #                 defaults={'total': credit_amount}
    #             )
    #             if not created:
    #                 credit.total += credit_amount
    #                 credit.save()
                
    #             # Send receipt email
    #             self.send_receipt_email(user, amount, credit_amount, payment_intent)
                
    #             messages.success(request, f"${amount} credit added successfully! You received {credit_amount} credits.")
    #             return JsonResponse({'success': True, 'redirect_url': str(self.success_url)})
    #         else:
    #             return JsonResponse({'success': False, 'error': 'Payment verification failed'}, status=400)
                
    #     except stripe.error.StripeError as e:
    #         logger.error(f"Stripe error: {str(e)}")
    #         return JsonResponse({'success': False, 'error': 'Payment verification failed'}, status=400)

    # def send_receipt_email(self, user, amount, credits_received, payment_intent):
    #     """Send receipt email to user"""
    #     try:
    #         # Prepare email context
    #         context = {
    #             'user': user,
    #             'amount': amount,
    #             'credits_received': credits_received,
    #             'transaction_id': payment_intent.id,
    #             'transaction_date': datetime.fromtimestamp(payment_intent.created),
    #             'payment_method': self.get_payment_method_info(payment_intent),
    #             'company_name': 'ImageAssistant.io',
    #             'support_email': 'support@imageassistant.io',
    #         }
            
    #         # Render email templates
    #         html_message = render_to_string('users/emails/receipt.html', context)
    #         plain_message = strip_tags(html_message)
            
    #         # Send email
    #         send_mail(
    #             subject=f'Receipt for your ImageAssistant.io credit purchase - ${amount}',
    #             message=plain_message,
    #             from_email=settings.DEFAULT_FROM_EMAIL,
    #             recipient_list=[user.email],
    #             html_message=html_message,
    #             fail_silently=False,
    #         )
            
    #         logger.info(f"Receipt email sent to {user.email} for transaction {payment_intent.id}")
            
    #     except Exception as e:
    #         logger.error(f"Failed to send receipt email: {str(e)}")



@method_decorator(csrf_exempt, name='dispatch')
class CreatePaymentIntentView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            amount = float(data.get('amount', 0))
            
            if amount < 1:
                return JsonResponse({'error': 'Minimum amount is $1'}, status=400)
            
            # Convert to cents for Stripe
            amount_cents = int(amount * 100)
            
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency='usd',
                metadata={
                    'user_id': request.user.id,
                    'credit_amount': amount,
                }
            )
            
            return JsonResponse({
                'client_secret': intent.client_secret
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
