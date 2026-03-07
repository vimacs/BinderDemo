"""
Auth Service URLs - v2.0
Includes role switching, permission requests, and audit log endpoints.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, VerifyEmailView, LoginView, LogoutView,
    CurrentUserView, MemberViewSet, TenantViewSet,
    toggle_permission, resend_verification_email, get_all_permissions,
    switch_role,
    PermissionRequestViewSet, AuditLogViewSet,
)
from .views_otp import login_request_otp, login_verify_otp, set_password

router = DefaultRouter()
router.register(r'members', MemberViewSet, basename='member')
router.register(r'tenants', TenantViewSet, basename='tenant')
router.register(r'permission-requests', PermissionRequestViewSet, basename='permission-request')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/', resend_verification_email, name='resend-verification'),

    # Login (legacy direct + OTP 2-step)
    path('login/', LoginView.as_view(), name='login'),
    path('login/request-otp/', login_request_otp, name='login-request-otp'),
    path('login/verify-otp/', login_verify_otp, name='login-verify-otp'),

    # Password management
    path('set-password/', set_password, name='set-password'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Current user
    path('me/', CurrentUserView.as_view(), name='current-user'),

    # v2: Role switching
    path('switch-role/', switch_role, name='switch-role'),

    # Permissions (legacy toggle)
    path('members/<uuid:user_id>/permissions/<uuid:permission_id>/toggle/',
         toggle_permission, name='toggle-permission'),
    path('permissions/', get_all_permissions, name='get-all-permissions'),

    # Router URLs (members, tenants, permission-requests, audit-logs)
    path('', include(router.urls)),
]
