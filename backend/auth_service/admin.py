from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Tenant, Permission, RolePermission, LoginHistory,
    UserRole, PermissionRequest, AuditLog,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'name', 'highest_role', 'is_primary_master', 'tenant', 'is_active', 'email_verified']
    list_filter = ['highest_role', 'role', 'is_active', 'email_verified', 'is_primary_master', 'tenant']
    search_fields = ['email', 'first_name', 'last_name', 'name', 'custom_role_name']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'first_name', 'last_name', 'phone')}),
        ('Role & Access (v2)', {'fields': ('highest_role', 'is_primary_master', 'role', 'custom_role_name', 'designation', 'tenant')}),
        ('Status', {'fields': ('is_active', 'is_staff', 'is_superuser', 'email_verified')}),
        ('Timestamps', {'fields': ('date_joined', 'last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'custom_role_name', 'tenant'),
        }),
    )

    readonly_fields = ['created_at', 'updated_at', 'highest_role']


@admin.register(Tenant)
class TenantAdmin(ModelAdmin):
    list_display = ['tenant_id', 'company_name', 'owner_name', 'plan', 'current_user_count', 'max_users', 'is_active', 'created_at']
    search_fields = ['company_name', 'company_email', 'tenant_id', 'owner_name']
    list_filter = ['is_active', 'plan', 'industry_vertical', 'location_state', 'created_at']
    readonly_fields = ['id', 'tenant_id', 'current_user_count', 'available_slots_display', 'created_at', 'updated_at']

    fieldsets = (
        ('Company Information', {
            'fields': ('id', 'tenant_id', 'company_name', 'owner_name', 'company_email', 'whatsapp_number', 'company_phone', 'company_address')
        }),
        ('Location & Industry (v2)', {
            'fields': ('location_city', 'location_state', 'industry_vertical')
        }),
        ('Subscription & Plan', {
            'fields': ('plan', 'max_users', 'current_user_count', 'available_slots_display', 'is_active')
        }),
        ('Logo', {'fields': ('logo',)}),
        ('Subscription Dates', {
            'fields': ('subscription_start_date', 'subscription_end_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def available_slots_display(self, obj):
        slots = obj.available_slots
        return f"{slots} available" if slots > 0 else "No slots available"
    available_slots_display.short_description = 'Available Slots'


@admin.register(UserRole)
class UserRoleAdmin(ModelAdmin):
    list_display = ['user', 'role', 'department', 'is_default_role', 'assigned_by', 'created_at']
    list_filter = ['role', 'is_default_role']
    search_fields = ['user__email', 'department']


@admin.register(Permission)
class PermissionAdmin(ModelAdmin):
    list_display = ['category', 'action', 'resource']
    list_filter = ['category', 'action']


@admin.register(RolePermission)
class RolePermissionAdmin(ModelAdmin):
    list_display = ['user_role', 'user', 'permission', 'permission_level', 'is_enabled']
    list_filter = ['is_enabled', 'permission_level']


@admin.register(PermissionRequest)
class PermissionRequestAdmin(ModelAdmin):
    list_display = ['requested_by', 'module_requested', 'status', 'approved_by', 'expires_at', 'created_at']
    list_filter = ['status', 'module_requested']
    search_fields = ['requested_by__email']


@admin.register(AuditLog)
class AuditLogAdmin(ModelAdmin):
    list_display = ['user', 'active_role', 'action_type', 'module', 'timestamp']
    list_filter = ['action_type', 'active_role', 'module']
    search_fields = ['user__email']
    readonly_fields = ['id', 'user', 'organization', 'active_role', 'action_type', 'module', 'record_id', 'details', 'ip_address', 'timestamp']


@admin.register(LoginHistory)
class LoginHistoryAdmin(ModelAdmin):
    list_display = ['user', 'ip_address', 'active_role', 'login_successful', 'login_at']
    list_filter = ['login_successful', 'active_role', 'login_at']
