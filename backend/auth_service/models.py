"""
Auth Service Models - v2.0
Multi-tenant user management with multi-role stacking,
audit logging, and cross-department permission requests.
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.validators import EmailValidator
import uuid


# ──────────────────────────────────────────────────────
# ENUMS / CHOICES  (v2 Role Hierarchy)
# ──────────────────────────────────────────────────────
ROLE_CHOICES = [
    ('master_admin', 'Master Admin'),   # Owner / Proprietor
    ('admin', 'Admin'),                 # GM / Operations Head
    ('manager', 'Manager'),             # Department Head
    ('supervisor', 'Supervisor'),       # Floor / Line Incharge
    ('operator', 'Operator'),           # Data Entry / Machine Operator
]

ROLE_HIERARCHY = {
    'master_admin': 5,
    'admin': 4,
    'manager': 3,
    'supervisor': 2,
    'operator': 1,
}

PERMISSION_LEVEL_CHOICES = [
    ('none', 'None'),
    ('view', 'View'),
    ('input', 'Input'),
    ('edit', 'Edit'),
    ('full', 'Full'),
    ('config', 'Config'),
]

MODULE_CHOICES = [
    ('production_planning', 'Production Planning'),
    ('quality_control', 'Quality Control / AQL'),
    ('raw_material_inventory', 'Raw Material / Inventory'),
    ('purchase_procurement', 'Purchase & Procurement'),
    ('sales_dispatch', 'Sales & Dispatch'),
    ('sampling_development', 'Sampling / Development'),
    ('reports_analytics', 'Reports & Analytics'),
    ('user_management', 'User Management'),
    ('billing_subscription', 'Billing & Subscription'),
    ('organization_settings', 'Organization Settings'),
    ('community', 'Community'),
    ('master_sheets', 'Master Sheets'),
]

ACTION_TYPE_CHOICES = [
    ('create', 'Create'),
    ('edit', 'Edit'),
    ('delete', 'Delete'),
    ('approve', 'Approve'),
    ('login', 'Login'),
    ('logout', 'Logout'),
    ('role_switch', 'Role Switch'),
]

PERMISSION_REQUEST_STATUS = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

PLAN_CHOICES = [
    ('basic', 'Basic Plan'),
    ('standard', 'Standard Plan'),
    ('premium', 'Premium Plan'),
    ('enterprise', 'Enterprise Plan'),
    ('custom', 'Custom Plan'),
]


# ──────────────────────────────────────────────────────
# USER MANAGER
# ──────────────────────────────────────────────────────
class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('email_verified', True)
        extra_fields.setdefault('is_primary_master', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# ──────────────────────────────────────────────────────
# TENANT / ORGANIZATION  (maps to "organizations" in v2 schema)
# ──────────────────────────────────────────────────────
class Tenant(models.Model):
    """
    Organization / Tenant
    Maps to the 'organizations' table in the v2 architecture spec.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # v2: display-friendly tenant ID  e.g. "BIND-PNP-0042"
    tenant_id = models.CharField(
        max_length=30, unique=True, blank=True,
        help_text='Display ID e.g. BIND-PNP-0042 (auto-generated if blank)'
    )

    # Company Information
    company_name = models.CharField(max_length=255, unique=True)
    owner_name = models.CharField(max_length=255, blank=True)
    company_email = models.EmailField(max_length=255)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    company_phone = models.CharField(max_length=15, blank=True)
    company_address = models.TextField(blank=True)

    # v2: location fields
    location_city = models.CharField(max_length=100, blank=True)
    location_state = models.CharField(max_length=100, blank=True)

    # v2: industry vertical
    industry_vertical = models.CharField(max_length=100, blank=True)

    # Subscription / Plan
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='standard')
    max_users = models.IntegerField(
        default=40,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        help_text="Maximum number of users allowed (1-1000)"
    )
    current_user_count = models.IntegerField(default=0)

    # Tenant Logo
    logo = models.ImageField(upload_to='tenant_logos/', blank=True, null=True)

    # Status
    is_active = models.BooleanField(default=True)
    subscription_start_date = models.DateField(default=timezone.now)
    subscription_end_date = models.DateField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tenants'
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tenant_id} - {self.company_name}" if self.tenant_id else self.company_name

    def save(self, *args, **kwargs):
        """Auto-generate tenant_id on first save if blank."""
        if not self.tenant_id:
            prefix = (self.location_city[:3] if self.location_city else 'GEN').upper()
            count = Tenant.objects.count() + 1
            self.tenant_id = f"BIND-{prefix}-{count:04d}"
        super().save(*args, **kwargs)

    # ── Compatibility aliases ──
    @property
    def user_limit(self):
        return self.max_users

    @user_limit.setter
    def user_limit(self, value):
        self.max_users = value

    @property
    def can_add_users(self):
        return self.current_user_count < self.max_users

    @property
    def available_slots(self):
        return self.max_users - self.current_user_count

    def increment_user_count(self):
        self.current_user_count += 1
        self.save()

    def decrement_user_count(self):
        if self.current_user_count > 0:
            self.current_user_count -= 1
            self.save()


# ──────────────────────────────────────────────────────
# USER
# ──────────────────────────────────────────────────────
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model  -  v2.0
    Supports multi-role stacking via the separate UserRole table.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Credentials
    email = models.EmailField(
        max_length=255, unique=True,
        validators=[EmailValidator()], db_index=True
    )
    phone = models.CharField(max_length=15, blank=True)

    # Profile
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=150, blank=True,
                            help_text='Full display name (v2)')

    # v2: computed highest role for quick lookup
    highest_role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, blank=True, default='',
        help_text='Computed from user_roles - highest assigned role'
    )

    # v2: primary master admin flag
    is_primary_master = models.BooleanField(
        default=False,
        help_text='True only for the 1st Master Admin of the org (absolute control)'
    )

    # Legacy single-role field (kept for backward compat)
    ROLE_CHOICES_LEGACY = [
        ('master_admin', 'Master Admin'),
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
        ('operator', 'Operator'),
        ('tenant_owner', 'Tenant Owner (legacy)'),
        ('employee', 'Employee (legacy)'),
        ('custom', 'Custom Role (legacy)'),
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES_LEGACY, default='operator')
    designation = models.CharField(max_length=100, blank=True)
    custom_role_name = models.CharField(max_length=100, blank=True, null=True)

    # Tenant Relationship
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE,
        related_name='members', null=True, blank=True
    )

    # Email OTP fields
    email_otp = models.CharField(max_length=6, blank=True, null=True)
    email_otp_created_at = models.DateTimeField(null=True, blank=True)
    email_otp_verified = models.BooleanField(default=False)

    # Password reset token
    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    password_reset_sent_at = models.DateTimeField(null=True, blank=True)

    # Status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Email Verification
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Metadata
    created_by = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='created_users'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['tenant', 'role']),
            models.Index(fields=['tenant', 'highest_role']),
            models.Index(fields=['email_verification_token']),
        ]

    def __str__(self):
        return self.get_display_name()

    def get_display_name(self):
        if self.name:
            return self.name
        full = f"{self.first_name} {self.last_name}".strip()
        return full or self.email

    def get_full_name(self):
        return self.get_display_name()

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        if self.name:
            return self.name.split()[0]
        return self.email.split('@')[0]

    # ── v2 role helpers ──
    def compute_highest_role(self):
        """Recompute highest_role from UserRole records and persist."""
        roles = self.user_roles.values_list('role', flat=True)
        if not roles:
            self.highest_role = self.role
            self.save(update_fields=['highest_role'])
            return self.highest_role
        best = max(roles, key=lambda r: ROLE_HIERARCHY.get(r, 0))
        if best != self.highest_role:
            self.highest_role = best
            self.save(update_fields=['highest_role'])
        return best

    def get_all_roles(self):
        return list(self.user_roles.select_related().all())

    def has_role(self, role_name):
        return self.user_roles.filter(role=role_name).exists()

    @property
    def is_tenant_owner(self):
        return self.is_primary_master or self.role == 'master_admin' or self.has_role('master_admin')

    @property
    def is_master_admin(self):
        return self.role == 'master_admin' or self.has_role('master_admin')

    @property
    def is_admin(self):
        return self.role == 'admin' or self.has_role('admin')

    @property
    def can_create_members(self):
        """v2: Master Admin and Admin can create users."""
        return self.is_master_admin or self.is_admin

    @property
    def can_delete_members(self):
        """v2: Only Master Admin can delete users."""
        return self.is_master_admin

    def can_create_role(self, target_role):
        """v2: who creates whom hierarchy."""
        if self.is_primary_master or self.is_master_admin:
            return True
        if self.is_admin:
            return target_role in ('manager', 'supervisor', 'operator')
        return False


# ──────────────────────────────────────────────────────
# USER ROLE  (NEW in v2 - multi-role stacking)
# ──────────────────────────────────────────────────────
class UserRole(models.Model):
    """
    Maps a user to one of potentially many roles.
    Enables multi-role stacking with department scoping.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(
        max_length=100, blank=True, null=True,
        help_text='Department scope (for manager / supervisor roles)'
    )
    is_default_role = models.BooleanField(default=False, help_text='Which role to load first after login')
    assigned_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='assigned_roles'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_roles'
        verbose_name = 'User Role'
        verbose_name_plural = 'User Roles'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'role', 'department'],
                name='unique_user_role_department'
            )
        ]

    def __str__(self):
        dept = f" ({self.department})" if self.department else ""
        return f"{self.user.email} -> {self.role}{dept}"


# ──────────────────────────────────────────────────────
# PERMISSION (global catalogue)
# ──────────────────────────────────────────────────────
class Permission(models.Model):
    """Global permission catalogue entries."""

    PERMISSION_CATEGORIES = MODULE_CHOICES + [
        ('members', 'Member Management'),
        ('settings', 'Settings'),
    ]

    ACTION_CHOICES = [
        ('view', 'View'),
        ('create', 'Create'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
        ('export', 'Export'),
        ('approve', 'Approve'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=50, choices=PERMISSION_CATEGORIES)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    resource = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'permissions'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
        unique_together = ['category', 'action', 'resource']

    def __str__(self):
        return f"{self.category}.{self.action}.{self.resource}"


# ──────────────────────────────────────────────────────
# ROLE PERMISSION  (v2: linked to UserRole, not User)
# ──────────────────────────────────────────────────────
class RolePermission(models.Model):
    """
    Per-role permission overrides.
    v2 links to UserRole (not directly to User).
    Legacy FK to User kept for backward compat but nullable.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # v2: primary link
    user_role = models.ForeignKey(
        UserRole, on_delete=models.CASCADE,
        related_name='role_permissions', null=True, blank=True
    )

    # Legacy link
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='legacy_role_permissions', null=True, blank=True
    )

    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    # v2: granular fields
    module = models.CharField(max_length=50, choices=MODULE_CHOICES, blank=True)
    permission_level = models.CharField(
        max_length=10, choices=PERMISSION_LEVEL_CHOICES, default='none'
    )
    can_create_users = models.BooleanField(default=False)
    can_delete_users = models.BooleanField(default=False)
    can_create_roles_up_to = models.CharField(
        max_length=20, choices=ROLE_CHOICES, blank=True, null=True,
        help_text='Highest role this permission allows creating'
    )

    is_enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    granted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, related_name='granted_permissions'
    )

    class Meta:
        db_table = 'role_permissions'
        verbose_name = 'Role Permission'
        verbose_name_plural = 'Role Permissions'

    def __str__(self):
        target = self.user_role or self.user
        return f"{target} - {self.permission}"


# ──────────────────────────────────────────────────────
# PERMISSION REQUEST  (NEW in v2)
# ──────────────────────────────────────────────────────
class PermissionRequest(models.Model):
    """Cross-department permission request."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    requested_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='permission_requests'
    )
    module_requested = models.CharField(max_length=50, choices=MODULE_CHOICES)
    specific_record_id = models.CharField(max_length=255, blank=True, null=True)
    reason = models.TextField()
    status = models.CharField(
        max_length=10, choices=PERMISSION_REQUEST_STATUS, default='pending'
    )
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='approved_permission_requests'
    )
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'permission_requests'
        verbose_name = 'Permission Request'
        verbose_name_plural = 'Permission Requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.requested_by.email} -> {self.module_requested} ({self.status})"

    @property
    def is_expired(self):
        if self.expires_at and self.status == 'approved':
            return timezone.now() > self.expires_at
        return False


# ──────────────────────────────────────────────────────
# AUDIT LOG  (NEW in v2)
# ──────────────────────────────────────────────────────
class AuditLog(models.Model):
    """
    Audit trail - every action logged with active role context.
    Role switches are also logged.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    organization = models.ForeignKey(
        Tenant, on_delete=models.CASCADE,
        related_name='audit_logs', null=True, blank=True
    )
    active_role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE_CHOICES)
    module = models.CharField(max_length=50, blank=True)
    record_id = models.CharField(max_length=255, blank=True)
    details = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_log'
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['organization', '-timestamp']),
        ]

    def __str__(self):
        return f"[{self.active_role}] {self.user.email} {self.action_type} @ {self.timestamp}"


# ──────────────────────────────────────────────────────
# LOGIN HISTORY  (enriched with active_role)
# ──────────────────────────────────────────────────────
class LoginHistory(models.Model):
    """Track user login history for security and analytics."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    login_successful = models.BooleanField(default=True)
    active_role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    login_at = models.DateTimeField(auto_now_add=True)
    logout_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'login_history'
        verbose_name = 'Login History'
        verbose_name_plural = 'Login History'
        ordering = ['-login_at']

    def __str__(self):
        return f"{self.user.email} - {self.login_at}"
