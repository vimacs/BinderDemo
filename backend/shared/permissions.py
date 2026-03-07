"""
Shared Permission Classes - v2.0
Updated for the 5-tier role hierarchy:
  Master Admin > Admin > Manager > Supervisor > Operator
"""
from rest_framework import permissions


class IsMasterAdmin(permissions.BasePermission):
    """Only Master Admins (1st or 2nd)."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_master_admin


class IsPrimaryMasterAdmin(permissions.BasePermission):
    """Only the 1st (primary) Master Admin with absolute control."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_primary_master


class IsAdmin(permissions.BasePermission):
    """Admin or above (Admin, Master Admin)."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_master_admin or request.user.is_admin
        )


class IsTenantOwner(permissions.BasePermission):
    """Backward compat: treats Master Admin as tenant owner."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_tenant_owner


class CanManageMembers(permissions.BasePermission):
    """Master Admin or Admin can create/manage members."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.can_create_members


class CanDeleteMembers(permissions.BasePermission):
    """Only Master Admin can delete users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.can_delete_members


class IsManagerOrAbove(permissions.BasePermission):
    """Manager, Admin, or Master Admin."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (
            request.user.is_master_admin
            or request.user.is_admin
            or request.user.has_role('manager')
        )
