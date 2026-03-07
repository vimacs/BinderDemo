"""
Auth Service Serializers - v2.0
Supports multi-role stacking, permission requests, and audit logs.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import (
    User, Tenant, Permission, RolePermission, UserRole,
    PermissionRequest, AuditLog, ROLE_HIERARCHY,
)


# ──────────────────────────────────────────────────────
# TENANT
# ──────────────────────────────────────────────────────
class TenantSerializer(serializers.ModelSerializer):
    available_slots = serializers.ReadOnlyField()
    can_add_users = serializers.ReadOnlyField()
    logo = serializers.ImageField(read_only=True)
    logo_url = serializers.SerializerMethodField()
    # Backward compat alias
    user_limit = serializers.IntegerField(source='max_users', read_only=True)

    class Meta:
        model = Tenant
        fields = [
            'id', 'tenant_id', 'company_name', 'owner_name',
            'company_email', 'whatsapp_number', 'company_phone',
            'company_address', 'location_city', 'location_state',
            'industry_vertical', 'plan', 'max_users', 'user_limit',
            'current_user_count', 'available_slots', 'can_add_users',
            'is_active', 'subscription_start_date', 'subscription_end_date',
            'logo', 'logo_url', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'tenant_id', 'current_user_count',
            'created_at', 'updated_at',
        ]

    def validate_max_users(self, value):
        if value < 1 or value > 1000:
            raise serializers.ValidationError("User limit must be between 1 and 1000")
        return value

    def get_logo_url(self, obj):
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None


class TenantLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['logo']

    def update(self, instance, validated_data):
        instance.logo = validated_data.get('logo', instance.logo)
        instance.save()
        return instance


# ──────────────────────────────────────────────────────
# USER ROLE  (NEW in v2)
# ──────────────────────────────────────────────────────
class UserRoleSerializer(serializers.ModelSerializer):
    assigned_by_email = serializers.CharField(source='assigned_by.email', read_only=True)

    class Meta:
        model = UserRole
        fields = [
            'id', 'user', 'role', 'department',
            'is_default_role', 'assigned_by', 'assigned_by_email',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class UserRoleCreateSerializer(serializers.ModelSerializer):
    """For creating/assigning roles to a user."""

    class Meta:
        model = UserRole
        fields = ['role', 'department', 'is_default_role']

    def validate_role(self, value):
        request = self.context.get('request')
        if request and request.user:
            if not request.user.can_create_role(value):
                raise serializers.ValidationError(
                    f"You do not have permission to assign the '{value}' role."
                )
        return value


# ──────────────────────────────────────────────────────
# USER  (basic + detail)
# ──────────────────────────────────────────────────────
class UserSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.company_name', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'name', 'full_name',
            'phone', 'role', 'highest_role', 'designation', 'tenant',
            'tenant_name', 'is_active', 'is_primary_master',
            'email_verified', 'date_joined', 'last_login',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed user serializer with multi-role info and permissions."""

    tenant_details = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    custom_role_name = serializers.CharField(read_only=True)
    # v2: multi-role data
    roles = serializers.SerializerMethodField()
    default_role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'name', 'full_name',
            'phone', 'role', 'highest_role', 'is_primary_master',
            'custom_role_name', 'designation',
            'tenant', 'tenant_details',
            'is_active', 'email_verified',
            'roles', 'default_role', 'permissions',
            'date_joined', 'last_login', 'created_at', 'updated_at',
            'created_by',
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_tenant_details(self, obj):
        if obj.tenant:
            return {
                'id': str(obj.tenant.id),
                'tenant_id': obj.tenant.tenant_id,
                'company_name': obj.tenant.company_name,
                'logo': obj.tenant.logo.url if obj.tenant.logo else None,
            }
        return None

    def get_roles(self, obj):
        """Return all assigned roles with department info."""
        user_roles = obj.user_roles.all().order_by('-created_at')
        return [
            {
                'id': str(ur.id),
                'role': ur.role,
                'department': ur.department,
                'is_default_role': ur.is_default_role,
                'assigned_by': str(ur.assigned_by_id) if ur.assigned_by_id else None,
                'created_at': ur.created_at.isoformat() if ur.created_at else None,
            }
            for ur in user_roles
        ]

    def get_default_role(self, obj):
        """Return the default role (or highest) for initial dashboard load."""
        default = obj.user_roles.filter(is_default_role=True).first()
        if default:
            return {'role': default.role, 'department': default.department}
        # Fallback to highest role
        roles = obj.user_roles.all()
        if roles.exists():
            best = max(roles, key=lambda r: ROLE_HIERARCHY.get(r.role, 0))
            return {'role': best.role, 'department': best.department}
        return {'role': obj.role, 'department': None}

    def get_permissions(self, obj):
        """Get user permissions with enabled status (legacy + v2)."""
        # Legacy permissions (linked to user directly)
        legacy_perms = obj.legacy_role_permissions.select_related('permission').all()
        results = []
        for rp in legacy_perms:
            results.append({
                'id': str(rp.permission.id),
                'permission_id': str(rp.id),
                'category': rp.permission.category,
                'action': rp.permission.action,
                'resource': rp.permission.resource,
                'description': rp.permission.description,
                'is_enabled': rp.is_enabled,
                'module': rp.module,
                'permission_level': rp.permission_level,
            })
        # v2 role-based permissions
        for ur in obj.user_roles.prefetch_related('role_permissions__permission').all():
            for rp in ur.role_permissions.all():
                results.append({
                    'id': str(rp.permission.id),
                    'permission_id': str(rp.id),
                    'category': rp.permission.category,
                    'action': rp.permission.action,
                    'resource': rp.permission.resource,
                    'description': rp.permission.description,
                    'is_enabled': rp.is_enabled,
                    'module': rp.module,
                    'permission_level': rp.permission_level,
                    'role': ur.role,
                    'department': ur.department,
                })
        return results


# ──────────────────────────────────────────────────────
# AUTH SERIALIZERS
# ──────────────────────────────────────────────────────
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True,
        validators=[validate_password], style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone', 'name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email, password=password
            )
            if not user:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.', code='authorization'
                )
            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.', code='authorization'
                )
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".', code='authorization'
            )

        attrs['user'] = user
        return attrs


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, write_only=True,
        validators=[validate_password], style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        required=True, write_only=True, style={'input_type': 'password'}
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs


# ──────────────────────────────────────────────────────
# MEMBER MANAGEMENT
# ──────────────────────────────────────────────────────
class CreateMemberSerializer(serializers.ModelSerializer):
    """
    v2: Create member with optional multi-role stacking.
    Accepts 'roles' array for multi-role assignment.
    """
    password = serializers.CharField(
        write_only=True, required=True,
        validators=[validate_password], style={'input_type': 'password'}
    )
    custom_role_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    permissions = serializers.ListField(
        child=serializers.UUIDField(), required=False, allow_empty=True,
        help_text="List of permission IDs to assign"
    )
    # v2: multi-role stacking
    roles = serializers.ListField(
        child=serializers.DictField(), required=False, allow_empty=True,
        help_text='List of {role, department?, is_default_role?} dicts'
    )

    class Meta:
        model = User
        fields = [
            'email', 'password', 'first_name', 'last_name', 'name',
            'phone', 'role', 'designation', 'custom_role_name',
            'permissions', 'roles',
        ]

    def validate(self, attrs):
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError("Authentication required")

        if not request.user.can_create_members:
            raise serializers.ValidationError("You don't have permission to create members")

        if request.user.tenant and not request.user.tenant.can_add_users:
            raise serializers.ValidationError(
                f"User limit reached. Your plan allows {request.user.tenant.max_users} users."
            )

        # Validate role hierarchy for each role being assigned
        roles_data = attrs.get('roles', [])
        for r in roles_data:
            role_name = r.get('role', '')
            if not request.user.can_create_role(role_name):
                raise serializers.ValidationError(
                    f"You cannot assign the '{role_name}' role."
                )

        # Validate single role field too
        single_role = attrs.get('role', 'operator')
        if not request.user.can_create_role(single_role):
            raise serializers.ValidationError(
                f"You cannot assign the '{single_role}' role."
            )

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        permission_ids = validated_data.pop('permissions', [])
        roles_data = validated_data.pop('roles', [])
        custom_role_name = validated_data.pop('custom_role_name', None)

        user = User.objects.create_user(**validated_data)

        if custom_role_name:
            user.custom_role_name = custom_role_name.strip()

        if request.user.tenant:
            user.tenant = request.user.tenant
            user.created_by = request.user
            request.user.tenant.increment_user_count()

        user.save()

        # v2: Create UserRole entries
        if roles_data:
            for i, r in enumerate(roles_data):
                UserRole.objects.create(
                    user=user,
                    role=r.get('role', validated_data.get('role', 'operator')),
                    department=r.get('department', None),
                    is_default_role=r.get('is_default_role', i == 0),
                    assigned_by=request.user,
                )
        else:
            # Create single UserRole from the legacy role field
            UserRole.objects.create(
                user=user,
                role=validated_data.get('role', user.role) or user.role,
                is_default_role=True,
                assigned_by=request.user,
            )

        # Compute highest role
        user.compute_highest_role()

        # Assign permissions
        if permission_ids:
            permissions = Permission.objects.filter(id__in=permission_ids)
            for perm in permissions:
                RolePermission.objects.create(
                    user=user,
                    permission=perm,
                    is_enabled=True,
                    granted_by=request.user,
                )

        return user


class UpdateMemberSerializer(serializers.ModelSerializer):
    custom_role_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'name', 'phone',
            'role', 'custom_role_name', 'designation', 'is_active',
        ]

    def validate(self, attrs):
        if attrs.get('role') == 'custom':
            if not attrs.get('custom_role_name', '').strip():
                raise serializers.ValidationError({
                    'custom_role_name': 'Custom role name is required when role is "custom"'
                })
        elif attrs.get('custom_role_name'):
            attrs['custom_role_name'] = None
        return attrs


# ──────────────────────────────────────────────────────
# PERMISSION SERIALIZERS
# ──────────────────────────────────────────────────────
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class RolePermissionSerializer(serializers.ModelSerializer):
    permission_details = PermissionSerializer(source='permission', read_only=True)
    user_email = serializers.SerializerMethodField()
    granted_by_email = serializers.CharField(source='granted_by.email', read_only=True)

    class Meta:
        model = RolePermission
        fields = [
            'id', 'user_role', 'user', 'user_email', 'permission',
            'permission_details', 'module', 'permission_level',
            'can_create_users', 'can_delete_users', 'can_create_roles_up_to',
            'is_enabled', 'granted_by', 'granted_by_email',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_user_email(self, obj):
        if obj.user_role:
            return obj.user_role.user.email
        if obj.user:
            return obj.user.email
        return None


class UserPermissionUpdateSerializer(serializers.Serializer):
    permissions = serializers.ListField(
        child=serializers.DictField(), required=True,
        help_text="List of permission objects with 'permission_id' and 'is_enabled'"
    )

    def validate_permissions(self, value):
        for perm in value:
            if 'permission_id' not in perm:
                raise serializers.ValidationError("Each permission must have 'permission_id'")
            if 'is_enabled' not in perm:
                raise serializers.ValidationError("Each permission must have 'is_enabled'")
        return value


# ──────────────────────────────────────────────────────
# PERMISSION REQUEST  (NEW in v2)
# ──────────────────────────────────────────────────────
class PermissionRequestSerializer(serializers.ModelSerializer):
    requested_by_email = serializers.CharField(source='requested_by.email', read_only=True)
    approved_by_email = serializers.CharField(source='approved_by.email', read_only=True)
    is_expired = serializers.ReadOnlyField()

    class Meta:
        model = PermissionRequest
        fields = [
            'id', 'requested_by', 'requested_by_email',
            'module_requested', 'specific_record_id', 'reason',
            'status', 'approved_by', 'approved_by_email',
            'expires_at', 'is_expired',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'status', 'approved_by',
            'created_at', 'updated_at',
        ]


class PermissionRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionRequest
        fields = ['module_requested', 'specific_record_id', 'reason']


class PermissionRequestActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    expires_in_hours = serializers.IntegerField(
        required=False, default=24, min_value=1, max_value=720,
        help_text='For approvals: how many hours the temporary access lasts'
    )


# ──────────────────────────────────────────────────────
# AUDIT LOG  (NEW in v2)
# ──────────────────────────────────────────────────────
class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_email', 'organization',
            'active_role', 'action_type', 'module',
            'record_id', 'details', 'ip_address', 'timestamp',
        ]
        read_only_fields = fields


# ──────────────────────────────────────────────────────
# ROLE SWITCH  (NEW in v2)
# ──────────────────────────────────────────────────────
class RoleSwitchSerializer(serializers.Serializer):
    """Switch the user's active role context."""
    role = serializers.ChoiceField(choices=[c[0] for c in UserRole._meta.get_field('role').choices])
    department = serializers.CharField(required=False, allow_blank=True, allow_null=True)
