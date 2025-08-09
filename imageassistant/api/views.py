from api.serializers import UserSerializer, ResetPasswordSerializer, ContactSerializer
from django.conf import settings
from users.forms import CustomPasswordResetForm
from users.models import Credit, FeatureFlag, CustomUser, BaredUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.mail import EmailMessage, get_connection
from rest_framework.pagination import PageNumberPagination
from images.models import Image, Service
from images.serializers import ImageSerializer
from images.tasks import (
    create_image_from_prompt, remove_background, create_greyscale, 
    create_image_outline_task, send_credit_purchase_email
)
import stripe
import requests
from datetime import datetime
stripe.api_key = settings.STRIPE_SECRET_KEY


class PublicConfigView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access
    
    def get(self, request):
        """Return public configuration values needed by the frontend"""
        return Response({
            'GOOGLE_CLIENT_ID': settings.GOOGLE_CLIENT_ID,
            'GOOGLE_LOGIN_REDIRECT_URI': settings.GOOGLE_LOGIN_REDIRECT_URI,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
            'CREDIT_MULTIPLIER': settings.CREDIT_SETTINGS,
            'DEV_MODE': settings.DEBUG,  # Include debug mode status
            # Add other public config values as needed
        })
    

class ImageListUpdate(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def put(self, request, image_id):
        image = self.queryset.get(pk=image_id)
        name = request.data.get('name', None)
        url = request.data.get('url', None)
        if name is None:
            return Response(
                {'name': 'This field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        image.image.name = name
        # since background removal process writes to another bucket, we need to update the alternate_url
        if url is not None:
            image.alternate_url = url
        image.processed = True
        image.save()
        serializer = ImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
class CustomTokenObtainView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Check for honeypot field (bot protection)
        if 'website' in request.data and request.data['website']:
            return Response(
                {"detail": "Error Occurred."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Additional input validation
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '')
        
        if not email or not password:
            return Response(
                {"detail": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Basic email format validation
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return Response(
                {"detail": "Invalid email format."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check for banned users
        try:
            from users.models import BaredUser, CustomUser
            user = CustomUser.objects.get(email=email)
            if BaredUser.objects.filter(user=user).exists():
                return Response(
                    {"detail": "Account is suspended."},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        return super().post(request, *args, **kwargs)
    

class UserInformationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {'detail': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UserSerializer(user)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

class AddCreditsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {'detail': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        credits = request.data.get('credits', 0)
        if credits <= 0:
            return Response(
                {'detail': 'Invalid credits amount.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Add credits to the user's account
        user.credit.total += credits
        user.credit.save()
        send_credit_purchase_email.delay(
            user.email, credits
        )
        return Response(
            {'detail': 'Credits added successfully.'},
            status=status.HTTP_200_OK
        )

class SignUpView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        # Check for honeypot field
        if 'website' in request.data and request.data['website']:
            return Response(
                {"detail": "Error Occurred."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            if serializer.is_valid():
                user = serializer.create(serializer.validated_data)
                user.set_password(self.request.data['password'])
                user.save()
                Credit.objects.create(user=user, total=100)  # Give initial credits
                FeatureFlag.objects.get_or_create(name='show_credits')[0].users.add(user)
                return Response(
                    {'detail': 'User created successfully.'},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'detail': 'An error occurred while creating the user.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





class GoogleLoginView(APIView):
    """
        Handle Google Sign-In callback
    """
    permission_classes = []
    def post(self, request):
        credential = self.request.data.get('credential', None)
        if not credential:
            return Response(
                {'detail': 'Credential not provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # Verify the token with Google
            response = requests.get(
                f'https://oauth2.googleapis.com/tokeninfo?id_token={credential}'
            )
            if response.status_code != 200:
                print(f"Failed to verify token: {response.status_code} - {response.text}")
                return response(
                    {'detail': 'Failed to verify token.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Extract user info from the token
            user_data = response.json()
            
            # Check if required fields exist
            email = user_data.get('email')
            if not email or not user_data.get('email_verified'):
                pass
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
                Credit.objects.create(user=user, total=100)  # Give initial credits
                FeatureFlag.objects.get_or_create(name='show_credits')[0].users.add(user)
                user.save()
                print(f"Created new user with email: {email}")
            # check if the user has been banned
            if BaredUser.objects.filter(user=user).exists():
                return Response(
                    {'detail': 'Your account has been banned.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            # return the jwt token 
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
            

        except Exception as e:
            print(f"Error during Google login: {e}")
            return Response(
                {'detail': 'An error occurred during Google login.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class ChangePasswordView(APIView):
    """
        Handle password change requests
    """
    permission_classes = []

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        form_data = {'email': request.data.get('email')}
        form = CustomPasswordResetForm(form_data)
        if serializer.is_valid() and form.is_valid():
            form.save(
                domain_override=settings.EMAIL_DOMAIN, from_email="no-reply@imageassistant.io",
                email_template_name="users/password_reset_email.html",
            )
            return Response(
                {'detail': 'Password reset email sent successfully.'},
                status=status.HTTP_200_OK
            )
        else:
            print(form.errors)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class PasswordRestConfirmView(APIView):
    """
        Handle password reset confirmation
    """
    permission_classes = []

    def post(self, request):
        from django.utils.http import urlsafe_base64_decode
        from django.contrib.auth.tokens import default_token_generator
        from users.models import CustomUser

        try:
            uidb64 = request.data.get('uidb64')
            token = request.data.get('token')
            print(token, uidb64)
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
            valid = default_token_generator.check_token(user, token)
            print(user, token, valid)
            if not valid:
                return Response(
                    {'detail': 'Invalid token.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            new_password = request.data.get('new_password')
            if not new_password:
                return Response(
                    {'detail': 'New password is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(new_password)
            user.save()
            return Response(
                {'detail': 'Password reset successfully.'},
                status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                {'detail': 'User does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )

class CreateImageFromPromptView(APIView):
    """
        Handle image creation from prompt
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        prompt = request.data.get('prompt', None)
        aspect_ratio = request.data.get('aspect_ratio', '16:9')  # Default aspect ratio if not provided
        if not prompt:
            return Response(
                {'detail': 'Prompt is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        image, _ = Image.objects.get_or_create(
            image='dummy.png', user=request.user,
            aspect_ratio=aspect_ratio,
            defaults={
                'created': datetime.now(),
                'processed': False,
                'aspect_ratio': aspect_ratio,
            }

        )
        print("Hello")
        create_image_from_prompt.delay(image.id, prompt)
        return Response({'detail': image.id}, status=status.HTTP_202_ACCEPTED)


class ImageStatusView(APIView):
    """
        Check the status of an image creation task
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, image_id):
        try:
            image = Image.objects.get(pk=image_id, user=request.user)
            if not image.processed:
                return Response(
                    {'detail': 'Image is still being processed.'},
                    status=status.HTTP_202_ACCEPTED
                )
            serializer = ImageSerializer(image)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Image.DoesNotExist:
            return Response(
                {'detail': 'Image not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class ProcessImageView(APIView):
    """
    Base class for image processing operations
    """
    permission_classes = [IsAuthenticated]
    
    def validate_image_upload(self, request):
        """Validate image upload and return image object"""
        if 'image' not in request.FILES:
            return None, Response(
                {'detail': 'Image file is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image_file = request.FILES['image']
        
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if image_file.size > max_size:
            return None, Response(
                {'detail': 'Image file too large. Maximum size is 10MB.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file type - be strict about content types
        allowed_types = ['image/jpeg', 'image/png', 'image/webp']
        if image_file.content_type not in allowed_types:
            return None, Response(
                {'detail': 'Invalid file type. Only JPEG, PNG, and WebP are allowed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Basic filename validation (Django handles most security concerns)
        import os
        filename = os.path.basename(image_file.name)
        
        # Ensure we have a valid filename (Django already prevents empty names)
        if not filename:
            return None, Response(
                {'detail': 'Invalid filename.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file extension matches content type
        allowed_extensions = {
            'image/jpeg': ['.jpg', '.jpeg'],
            'image/png': ['.png'],
            'image/webp': ['.webp']
        }
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in allowed_extensions.get(image_file.content_type, []):
            return None, Response(
                {'detail': 'File extension does not match content type.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Create image record
            image = Image.objects.create(
                image=image_file,
                user=request.user,
                processed=False
            )
            return image, None
        except Exception as e:
            return None, Response(
                {'detail': 'Failed to process image upload.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def check_user_credits(self, user, required_credits):
        """Check if user has sufficient credits"""
        if not hasattr(user, 'credit'):
            return False
        return user.credit.total >= required_credits


class RemoveBackgroundView(ProcessImageView):
    """
    Remove background from uploaded image
    """
    def post(self, request):
        image, error_response = self.validate_image_upload(request)
        if error_response:
            return error_response
            
        # Check if user has enough credits
        try:
            service = Service.objects.get(code=2)  # Remove Background service
            if not self.check_user_credits(request.user, service.tokens):
                return Response(
                    {'detail': 'Insufficient credits.'},
                    status=status.HTTP_402_PAYMENT_REQUIRED
                )
        except Service.DoesNotExist:
            return Response(
                {'detail': 'Service not available.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Queue background removal task
        remove_background.delay(image.id)
        
        return Response({
            'detail': 'Background removal started.',
            'image_id': image.id
        }, status=status.HTTP_202_ACCEPTED)


class CreateGrayscaleView(ProcessImageView):
    """
    Convert uploaded image to grayscale
    """
    def post(self, request):
        image, error_response = self.validate_image_upload(request)
        if error_response:
            return error_response
            
        # Check if user has enough credits
        try:
            service = Service.objects.get(code=1)  # Greyscale service
            if not self.check_user_credits(request.user, service.tokens):
                return Response(
                    {'detail': 'Insufficient credits.'},
                    status=status.HTTP_402_PAYMENT_REQUIRED
                )
        except Service.DoesNotExist:
            return Response(
                {'detail': 'Service not available.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Queue grayscale conversion task
        create_greyscale.delay(image.id)
        
        return Response({
            'detail': 'Grayscale conversion started.',
            'image_id': image.id
        }, status=status.HTTP_202_ACCEPTED)


class CreateOutlineView(ProcessImageView):
    """
    Create outline from uploaded image
    """
    def post(self, request):
        image, error_response = self.validate_image_upload(request)
        if error_response:
            return error_response
            
        # Check if user has enough credits
        try:
            service = Service.objects.get(code=8)  # Outline service
            if not self.check_user_credits(request.user, service.tokens):
                return Response(
                    {'detail': 'Insufficient credits.'},
                    status=status.HTTP_402_PAYMENT_REQUIRED
                )
        except Service.DoesNotExist:
            return Response(
                {'detail': 'Service not available.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Queue outline creation task
        create_image_outline_task.delay(image.id)
        
        return Response({
            'detail': 'Outline creation started.',
            'image_id': image.id
        }, status=status.HTTP_202_ACCEPTED)


class UserImagesPagination(PageNumberPagination):
    """Custom pagination for user images"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class UserImagesView(APIView):
    """
    Get paginated list of current user's images
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get user's images, ordered by most recent first
        user_images = Image.objects.filter(
            user=request.user,
            processed=True  # Only show processed images
        ).order_by('-created')
        
        # Apply pagination
        paginator = UserImagesPagination()
        page = paginator.paginate_queryset(user_images, request)
        
        if page is not None:
            serializer = ImageSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # Fallback if pagination fails
        serializer = ImageSerializer(user_images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactView(APIView):
    """
    Handle contact form submissions
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        
        if serializer.is_valid():
            # Extract validated data
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            
            # Format the email
            email_subject = f"ImageAssistant.io - {subject} from {name} ({email})"
            email_body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}"
            recipient_list = ["cormackandy@hotmail.com"]
            from_email = "no-reply@imageassistant.io"
            
            try:
                # Send email using the same configuration as the Django view
                with get_connection(
                    host=settings.MAILERSEND_SMTP_HOST,
                    port=settings.MAILERSEND_SMTP_PORT,
                    username=settings.MAILERSEND_SMTP_USERNAME,
                    password=settings.MAILERSEND_SMTP_PASSWORD,
                    use_tls=True,
                ) as connection:
                    EmailMessage(
                        subject=email_subject,
                        body=email_body,
                        to=recipient_list,
                        from_email=from_email,
                        connection=connection
                    ).send()
                
                return Response(
                    {"success": True, "message": "Your message has been sent successfully."},
                    status=status.HTTP_200_OK
                )
                
            except Exception as e:
                return Response(
                    {"success": False, "message": "Failed to send message. Please try again later."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# stripe endpoints
class StripePaymentIntentView(APIView):
    """
    API endpoint to create a Stripe payment intent
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            amount = float(data.get('amount', 0))
            
            if amount < 10:
                return Response({
                    'error': 'Minimum amount is $10.00'
                }, status=400)

            # Convert to cents for Stripe
            amount_cents = int(amount * 100)
            
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency='usd',
                receipt_email=request.user.email,
                metadata={
                    'user_id': request.user.id,
                    'credit_amount': amount,
                }
            )

            return Response({
                'client_secret': intent.client_secret
            })

        except Exception as e:
            return Response({
                'error': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)