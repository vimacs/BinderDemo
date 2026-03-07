"""
OTP-based authentication views - v2.0
Updated to return multi-role data on login.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random

from .models import User, LoginHistory
from .serializers import LoginSerializer, UserDetailSerializer
from .views import get_tokens_for_user, get_client_ip, log_audit


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(user, otp):
    subject = 'Binder Login OTP'
    message = f"""
    Hi {user.get_full_name()},

    Your OTP for Binder login is: {otp}

    This OTP will expire in 10 minutes.

    If you didn't request this, please ignore this email.

    Best regards,
    Binder Team
    """

    if settings.DEBUG:
        print(f"\n{'='*60}")
        print(f"OTP EMAIL  To: {user.email}  OTP: {otp}")
        print(f"{'='*60}\n")

    try:
        send_mail(
            subject, message, settings.DEFAULT_FROM_EMAIL,
            [user.email], fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending OTP email: {e}")
        return False


@api_view(['POST'])
@permission_classes([AllowAny])
def login_request_otp(request):
    """
    Step 1: Validate credentials and send OTP
    POST /api/auth/login/request-otp/
    """
    serializer = LoginSerializer(data=request.data, context={'request': request})
    if not serializer.is_valid():
        return Response({
            'status': 'error', 'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.validated_data['user']

    otp = generate_otp()
    user.email_otp = otp
    user.email_otp_created_at = timezone.now()
    user.email_otp_verified = False
    user.save()

    send_otp_email(user, otp)

    return Response({
        'status': 'success',
        'message': 'OTP sent to your email',
        'data': {
            'email': user.email,
            'otp_expires_in': 600,
        }
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def login_verify_otp(request):
    """
    Step 2: Verify OTP and complete login (v2: returns multi-role data)
    POST /api/auth/login/verify-otp/
    """
    email = request.data.get('email')
    otp = request.data.get('otp')

    if not email or not otp:
        return Response({
            'status': 'error', 'message': 'Email and OTP are required'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email, email_verified=True, is_active=True)
    except User.DoesNotExist:
        return Response({
            'status': 'error', 'message': 'Invalid credentials'
        }, status=status.HTTP_400_BAD_REQUEST)

    if not user.email_otp:
        return Response({
            'status': 'error', 'message': 'No OTP found. Please request a new one.'
        }, status=status.HTTP_400_BAD_REQUEST)

    if user.email_otp_created_at:
        time_diff = timezone.now() - user.email_otp_created_at
        if time_diff.total_seconds() > 600:
            return Response({
                'status': 'error', 'message': 'OTP expired. Please request a new one.'
            }, status=status.HTTP_400_BAD_REQUEST)

    if user.email_otp != otp:
        return Response({
            'status': 'error', 'message': 'Invalid OTP'
        }, status=status.HTTP_400_BAD_REQUEST)

    # OTP verified
    user.email_otp = None
    user.email_otp_created_at = None
    user.email_otp_verified = True
    user.last_login = timezone.now()
    user.save()

    # Ensure highest_role is computed
    user.compute_highest_role()

    LoginHistory.objects.create(
        user=user,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        login_successful=True,
        active_role=user.highest_role,
    )

    log_audit(
        user, 'login',
        active_role=user.highest_role,
        ip_address=get_client_ip(request),
        details={'method': 'otp'},
    )

    tokens = get_tokens_for_user(user)
    user_data = UserDetailSerializer(user).data

    return Response({
        'status': 'success',
        'message': 'Login successful',
        'data': {
            'user': user_data,
            'tokens': tokens,
        }
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def set_password(request):
    """
    Set new password (for first-time users via welcome link)
    POST /api/auth/set-password/
    """
    token = request.data.get('token')
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')

    if not all([token, password, password_confirm]):
        return Response({
            'status': 'error', 'message': 'All fields are required'
        }, status=status.HTTP_400_BAD_REQUEST)

    if password != password_confirm:
        return Response({
            'status': 'error', 'message': 'Passwords do not match'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(password_reset_token=token)

        if user.password_reset_sent_at:
            time_diff = timezone.now() - user.password_reset_sent_at
            if time_diff.total_seconds() > 172800:  # 48 hours (v2 spec)
                return Response({
                    'status': 'error', 'message': 'Link expired'
                }, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.password_reset_token = None
        user.password_reset_sent_at = None
        user.email_verified = True
        user.save()

        return Response({
            'status': 'success', 'message': 'Password set successfully. You can now login.'
        })

    except User.DoesNotExist:
        return Response({
            'status': 'error', 'message': 'Invalid or expired link'
        }, status=status.HTTP_400_BAD_REQUEST)
