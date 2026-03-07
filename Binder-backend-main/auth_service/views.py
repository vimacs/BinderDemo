"""
Auth Service Views - v2.0
Multi-role login, role switching, permission requests, audit logging.
"""
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
import secrets

from .models import (
    Tenant, Permission, RolePermission, LoginHistory,
    UserRole, PermissionRequest, AuditLog, ROLE_HIERARCHY,
)
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    EmailVerificationSerializer, CreateMemberSerializer,
    UpdateMemberSerializer, TenantSerializer, UserDetailSerializer,
    RolePermissionSerializer, UserPermissionUpdateSerializer,
    TenantLogoSerializer, PermissionSerializer,
    UserRoleSerializer, UserRoleCreateSerializer,
    PermissionRequestSerializer, PermissionRequestCreateSerializer,
    PermissionRequestActionSerializer,
    AuditLogSerializer, RoleSwitchSerializer,
)
from .utils.email_verification import send_verification_email

User = get_user_model()


# ──────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def log_audit(user, action_type, active_role='', module='',
              record_id='', details=None, ip_address=None):
    """Create an audit log entry (v2)."""
    AuditLog.objects.create(
        user=user,
        organization=user.tenant,
        active_role=active_role or user.highest_role or user.role,
        action_type=action_type,
        module=module,
        record_id=record_id,
        details=details or {},
        ip_address=ip_address,
    )


# ──────────────────────────────────────────────────────
# AUTH VIEWS
# ──────────────────────────────────────────────────────
class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/"""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        user.email_verified = True
        user.email_verification_token = None
        user.save()

        return Response({
            'status': 'success',
            'message': 'Registration successful. Your account is ready to use.',
            'data': {
                'email': user.email,
                'id': str(user.id),
                'email_verified': True,
            }
        }, status=status.HTTP_201_CREATED)


class VerifyEmailView(generics.GenericAPIView):
    """POST /api/auth/verify-email/"""
    permission_classes = [AllowAny]
    serializer_class = EmailVerificationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        try:
            user = User.objects.get(email_verification_token=token)
            if user.email_verification_sent_at:
                time_diff = timezone.now() - user.email_verification_sent_at
                if time_diff.total_seconds() > 86400:
                    return Response({
                        'status': 'error',
                        'message': 'Verification link expired. Please request a new one.'
                    }, status=status.HTTP_400_BAD_REQUEST)

            user.email_verified = True
            user.email_verification_token = None
            user.save()
            return Response({'status': 'success', 'message': 'Email verified successfully.'})

        except User.DoesNotExist:
            return Response({
                'status': 'error', 'message': 'Invalid verification token.'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    """
    POST /api/auth/login/
    v2: Returns multi-role data, highest role, role switcher info.
    System auto-detects org from credentials (no org ID needed).
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user.last_login = timezone.now()
        user.save()

        # Ensure highest_role is computed
        user.compute_highest_role()

        # Login history with active role
        LoginHistory.objects.create(
            user=user,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            login_successful=True,
            active_role=user.highest_role,
        )

        # Audit log
        log_audit(
            user, 'login',
            active_role=user.highest_role,
            ip_address=get_client_ip(request),
            details={'method': 'password'},
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
        }, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    """POST /api/auth/logout/"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            last_login = LoginHistory.objects.filter(
                user=request.user, logout_at__isnull=True
            ).order_by('-login_at').first()
            if last_login:
                last_login.logout_at = timezone.now()
                last_login.save()

            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            log_audit(request.user, 'logout', ip_address=get_client_ip(request))

            return Response({'status': 'success', 'message': 'Logged out successfully'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(generics.RetrieveAPIView):
    """GET /api/auth/me/"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user


# ──────────────────────────────────────────────────────
# ROLE SWITCHING  (NEW in v2)
# ──────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def switch_role(request):
    """
    POST /api/auth/switch-role/
    Switch the active role context.
    Body: { "role": "admin", "department": "production" }
    """
    serializer = RoleSwitchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    role = serializer.validated_data['role']
    department = serializer.validated_data.get('department', None)

    # Check user actually has this role
    filter_kwargs = {'user': request.user, 'role': role}
    if department:
        filter_kwargs['department'] = department

    user_role = UserRole.objects.filter(**filter_kwargs).first()
    if not user_role:
        return Response({
            'status': 'error',
            'message': f'You do not have the "{role}" role assigned.'
        }, status=status.HTTP_403_FORBIDDEN)

    # Audit the role switch
    log_audit(
        request.user, 'role_switch',
        active_role=role,
        ip_address=get_client_ip(request),
        details={
            'switched_to': role,
            'department': department,
            'user_role_id': str(user_role.id),
        },
    )

    return Response({
        'status': 'success',
        'message': f'Switched to {role} role',
        'data': {
            'active_role': role,
            'department': department,
            'user_role_id': str(user_role.id),
        }
    })


# ──────────────────────────────────────────────────────
# MEMBER MANAGEMENT
# ──────────────────────────────────────────────────────
class MemberViewSet(viewsets.ModelViewSet):
    """
    GET    /api/auth/members/           - List members
    POST   /api/auth/members/           - Create member (with multi-role stacking)
    GET    /api/auth/members/{id}/      - Get member details
    PATCH  /api/auth/members/{id}/      - Update member
    DELETE /api/auth/members/{id}/      - Deactivate member
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateMemberSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateMemberSerializer
        return UserDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_master_admin:
            return User.objects.all()
        elif user.can_create_members and user.tenant:
            return User.objects.filter(tenant=user.tenant)
        else:
            return User.objects.filter(id=user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.save()

        member.email_verified = True
        member.save()

        log_audit(
            request.user, 'create', module='user_management',
            record_id=str(member.id),
            ip_address=get_client_ip(request),
            details={'created_user': member.email},
        )

        return Response({
            'status': 'success',
            'message': 'Member created successfully',
            'data': UserDetailSerializer(member).data,
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        log_audit(
            request.user, 'edit', module='user_management',
            record_id=str(instance.id),
            ip_address=get_client_ip(request),
        )

        return Response({
            'status': 'success',
            'message': 'Member updated successfully',
            'data': UserDetailSerializer(instance).data,
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # v2: Only Master Admin can delete users
        if not request.user.can_delete_members:
            return Response({
                'status': 'error',
                'message': 'Only Master Admin can delete users.'
            }, status=status.HTTP_403_FORBIDDEN)

        if instance.id == request.user.id:
            return Response({
                'status': 'error',
                'message': 'You cannot deactivate your own account'
            }, status=status.HTTP_400_BAD_REQUEST)

        instance.is_active = False
        instance.save()

        if instance.tenant:
            instance.tenant.decrement_user_count()

        log_audit(
            request.user, 'delete', module='user_management',
            record_id=str(instance.id),
            ip_address=get_client_ip(request),
            details={'deactivated_user': instance.email},
        )

        return Response({'status': 'success', 'message': 'Member deactivated successfully'})

    # ── Role stacking actions (v2) ──
    @action(detail=True, methods=['get'], url_path='roles')
    def list_roles(self, request, pk=None):
        """GET /api/auth/members/{id}/roles/ - list all roles for a user."""
        user = self.get_object()
        roles = user.user_roles.all()
        return Response({
            'status': 'success',
            'data': UserRoleSerializer(roles, many=True).data,
        })

    @action(detail=True, methods=['post'], url_path='assign-role')
    def assign_role(self, request, pk=None):
        """
        POST /api/auth/members/{id}/assign-role/
        Body: { "role": "supervisor", "department": "weaving", "is_default_role": false }
        """
        user = self.get_object()
        serializer = UserRoleCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        role_data = serializer.validated_data
        user_role, created = UserRole.objects.get_or_create(
            user=user,
            role=role_data['role'],
            department=role_data.get('department', None),
            defaults={
                'is_default_role': role_data.get('is_default_role', False),
                'assigned_by': request.user,
            }
        )

        if not created:
            return Response({
                'status': 'error',
                'message': 'This role is already assigned to the user.'
            }, status=status.HTTP_400_BAD_REQUEST)

        user.compute_highest_role()

        log_audit(
            request.user, 'create', module='user_management',
            record_id=str(user_role.id),
            ip_address=get_client_ip(request),
            details={
                'assigned_role': role_data['role'],
                'department': role_data.get('department'),
                'target_user': user.email,
            },
        )

        return Response({
            'status': 'success',
            'message': f"Role '{role_data['role']}' assigned successfully",
            'data': UserRoleSerializer(user_role).data,
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path='remove-role/(?P<role_id>[^/.]+)')
    def remove_role(self, request, pk=None, role_id=None):
        """DELETE /api/auth/members/{id}/remove-role/{role_id}/"""
        user = self.get_object()

        if not request.user.can_create_members:
            return Response({
                'status': 'error', 'message': 'Permission denied'
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            user_role = UserRole.objects.get(id=role_id, user=user)
        except UserRole.DoesNotExist:
            return Response({
                'status': 'error', 'message': 'Role not found'
            }, status=status.HTTP_404_NOT_FOUND)

        role_name = user_role.role
        user_role.delete()
        user.compute_highest_role()

        log_audit(
            request.user, 'delete', module='user_management',
            record_id=str(role_id),
            ip_address=get_client_ip(request),
            details={'removed_role': role_name, 'target_user': user.email},
        )

        return Response({'status': 'success', 'message': f"Role '{role_name}' removed"})

    # ── Permission actions (existing) ──
    @action(detail=True, methods=['post'], url_path='update-permissions')
    def update_permissions(self, request, pk=None):
        user = self.get_object()
        if not request.user.can_create_members:
            return Response({
                'status': 'error',
                'message': 'You do not have permission to manage user permissions'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = UserPermissionUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        permissions_data = serializer.validated_data['permissions']

        for perm_data in permissions_data:
            permission_id = perm_data.get('permission_id')
            permission_uuid = perm_data.get('id')
            is_enabled = perm_data.get('is_enabled', True)

            if permission_id:
                try:
                    rp = RolePermission.objects.get(id=permission_id, user=user)
                    rp.is_enabled = is_enabled
                    rp.granted_by = request.user
                    rp.save()
                    continue
                except RolePermission.DoesNotExist:
                    pass

            if permission_uuid:
                try:
                    perm = Permission.objects.get(id=permission_uuid)
                    rp, created = RolePermission.objects.get_or_create(
                        user=user, permission=perm,
                        defaults={'is_enabled': is_enabled, 'granted_by': request.user}
                    )
                    if not created:
                        rp.is_enabled = is_enabled
                        rp.granted_by = request.user
                        rp.save()
                except Permission.DoesNotExist:
                    continue

        return Response({
            'status': 'success',
            'message': 'Permissions updated successfully',
            'data': UserDetailSerializer(user).data,
        })

    @action(detail=True, methods=['get'], url_path='available-permissions')
    def available_permissions(self, request, pk=None):
        user = self.get_object()
        all_permissions = Permission.objects.all().order_by('category', 'resource', 'action')

        user_permissions = {
            str(rp.permission.id): {'permission_id': str(rp.id), 'is_enabled': rp.is_enabled}
            for rp in user.legacy_role_permissions.select_related('permission').all()
        }

        grouped = {}
        for perm in all_permissions:
            perm_id = str(perm.id)
            if perm.category not in grouped:
                grouped[perm.category] = []
            user_perm = user_permissions.get(perm_id)
            grouped[perm.category].append({
                'id': perm_id,
                'category': perm.category,
                'action': perm.action,
                'resource': perm.resource,
                'description': perm.description,
                'permission_id': user_perm['permission_id'] if user_perm else None,
                'is_enabled': user_perm['is_enabled'] if user_perm else False,
            })

        return Response({'status': 'success', 'data': grouped})


# ──────────────────────────────────────────────────────
# PERMISSION REQUEST  (NEW in v2)
# ──────────────────────────────────────────────────────
class PermissionRequestViewSet(viewsets.ModelViewSet):
    """
    GET    /api/auth/permission-requests/           - List requests
    POST   /api/auth/permission-requests/           - Create request
    POST   /api/auth/permission-requests/{id}/act/  - Approve / Reject
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PermissionRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_master_admin or user.is_admin:
            # Admins see all requests in their org
            if user.tenant:
                return PermissionRequest.objects.filter(requested_by__tenant=user.tenant)
            return PermissionRequest.objects.all()
        return PermissionRequest.objects.filter(requested_by=user)

    def create(self, request, *args, **kwargs):
        serializer = PermissionRequestCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        perm_request = PermissionRequest.objects.create(
            requested_by=request.user,
            **serializer.validated_data,
        )

        log_audit(
            request.user, 'create', module='permission_requests',
            record_id=str(perm_request.id),
            ip_address=get_client_ip(request),
            details={'module_requested': perm_request.module_requested},
        )

        return Response({
            'status': 'success',
            'message': 'Permission request submitted. Admin and Master Admin have been notified.',
            'data': PermissionRequestSerializer(perm_request).data,
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='act')
    def act(self, request, pk=None):
        """Approve or reject a permission request."""
        perm_request = self.get_object()

        if not (request.user.is_master_admin or request.user.is_admin):
            return Response({
                'status': 'error',
                'message': 'Only Admin or Master Admin can approve/reject requests.'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = PermissionRequestActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action_val = serializer.validated_data['action']
        expires_in = serializer.validated_data.get('expires_in_hours', 24)

        if action_val == 'approve':
            perm_request.status = 'approved'
            perm_request.approved_by = request.user
            perm_request.expires_at = timezone.now() + timedelta(hours=expires_in)
        else:
            perm_request.status = 'rejected'
            perm_request.approved_by = request.user

        perm_request.save()

        log_audit(
            request.user, 'approve' if action_val == 'approve' else 'edit',
            module='permission_requests',
            record_id=str(perm_request.id),
            ip_address=get_client_ip(request),
            details={
                'action': action_val,
                'module_requested': perm_request.module_requested,
                'requester': perm_request.requested_by.email,
            },
        )

        return Response({
            'status': 'success',
            'message': f'Request {action_val}d successfully',
            'data': PermissionRequestSerializer(perm_request).data,
        })


# ──────────────────────────────────────────────────────
# AUDIT LOG  (NEW in v2)
# ──────────────────────────────────────────────────────
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/auth/audit-logs/
    Read-only audit trail. Only Master Admin and Admin can view.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AuditLogSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_master_admin:
            if user.tenant:
                return AuditLog.objects.filter(organization=user.tenant)
            return AuditLog.objects.all()
        elif user.is_admin and user.tenant:
            return AuditLog.objects.filter(organization=user.tenant)
        return AuditLog.objects.none()


# ──────────────────────────────────────────────────────
# PERMISSIONS & TENANT  (existing, unchanged logic)
# ──────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_permissions(request):
    """GET /api/auth/permissions/"""
    permissions = Permission.objects.all().order_by('category', 'resource', 'action')
    grouped = {}
    for perm in permissions:
        if perm.category not in grouped:
            grouped[perm.category] = []
        grouped[perm.category].append({
            'id': str(perm.id),
            'category': perm.category,
            'action': perm.action,
            'resource': perm.resource,
            'description': perm.description,
        })
    return Response({'status': 'success', 'data': grouped})


class TenantViewSet(viewsets.ModelViewSet):
    """Tenant Management (with v2 fields)"""
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'upload_logo':
            return TenantLogoSerializer
        return TenantSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_master_admin:
            return Tenant.objects.all()
        elif user.is_tenant_owner and user.tenant:
            return Tenant.objects.filter(id=user.tenant.id)
        return Tenant.objects.none()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if not request.user.is_master_admin:
            restricted_fields = ['max_users', 'user_limit', 'plan', 'is_active']
            for field in restricted_fields:
                if field in request.data:
                    return Response({
                        'status': 'error',
                        'message': f'You do not have permission to update {field}.'
                    }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'status': 'success',
            'message': 'Tenant updated successfully',
            'data': serializer.data,
        })

    @action(detail=True, methods=['post'], url_path='update-user-limit')
    def update_user_limit(self, request, pk=None):
        tenant = self.get_object()
        if not request.user.is_master_admin:
            return Response({
                'status': 'error', 'message': 'Only master admin can update user limits'
            }, status=status.HTTP_403_FORBIDDEN)

        new_limit = request.data.get('user_limit') or request.data.get('max_users')
        plan = request.data.get('plan', tenant.plan)

        if new_limit is None:
            return Response({
                'status': 'error', 'message': 'user_limit / max_users is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(new_limit, int) or new_limit < 1 or new_limit > 1000:
            return Response({
                'status': 'error', 'message': 'Limit must be between 1 and 1000'
            }, status=status.HTTP_400_BAD_REQUEST)

        if new_limit < tenant.current_user_count:
            return Response({
                'status': 'error',
                'message': f'Limit cannot be less than current count ({tenant.current_user_count})'
            }, status=status.HTTP_400_BAD_REQUEST)

        tenant.max_users = new_limit
        tenant.plan = plan
        tenant.save()

        return Response({
            'status': 'success',
            'message': f'User limit updated to {new_limit}',
            'data': {
                'id': str(tenant.id),
                'tenant_id': tenant.tenant_id,
                'company_name': tenant.company_name,
                'max_users': tenant.max_users,
                'current_user_count': tenant.current_user_count,
                'available_slots': tenant.available_slots,
                'plan': tenant.plan,
            }
        })

    @action(detail=True, methods=['post'], url_path='upload-logo')
    def upload_logo(self, request, pk=None):
        tenant = self.get_object()
        if not request.user.is_master_admin and not (request.user.is_tenant_owner and request.user.tenant == tenant):
            return Response({
                'status': 'error', 'message': 'Permission denied'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = TenantLogoSerializer(tenant, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'status': 'success',
            'message': 'Logo uploaded successfully',
            'data': {'logo': tenant.logo.url if tenant.logo else None},
        })


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/auth/permissions/"""
    queryset = Permission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_permission(request, user_id, permission_id):
    """POST /api/auth/members/{user_id}/permissions/{permission_id}/toggle/"""
    if not request.user.can_create_members:
        return Response({
            'status': 'error', 'message': 'Permission denied'
        }, status=status.HTTP_403_FORBIDDEN)

    try:
        user = User.objects.get(id=user_id)
        permission = Permission.objects.get(id=permission_id)
        role_perm, created = RolePermission.objects.get_or_create(
            user=user, permission=permission,
            defaults={'granted_by': request.user}
        )
        if not created:
            role_perm.is_enabled = not role_perm.is_enabled
            role_perm.save()

        return Response({
            'status': 'success',
            'message': f'Permission {"enabled" if role_perm.is_enabled else "disabled"}',
            'data': RolePermissionSerializer(role_perm).data,
        })
    except (User.DoesNotExist, Permission.DoesNotExist):
        return Response({
            'status': 'error', 'message': 'User or Permission not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification_email(request):
    """POST /api/auth/resend-verification/"""
    email = request.data.get('email')
    if not email:
        return Response({'status': 'error', 'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        if user.email_verified:
            return Response({'status': 'error', 'message': 'Email already verified'}, status=status.HTTP_400_BAD_REQUEST)

        user.email_verification_token = secrets.token_urlsafe(32)
        user.email_verification_sent_at = timezone.now()
        user.save()
        send_verification_email(user)

        return Response({'status': 'success', 'message': 'Verification email sent'})
    except User.DoesNotExist:
        return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
