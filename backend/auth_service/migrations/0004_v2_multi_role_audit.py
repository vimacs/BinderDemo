"""
Migration for Auth Service v2.0
- Tenant: add tenant_id, owner_name, whatsapp_number, location_city, location_state,
  industry_vertical; rename user_limit -> max_users
- User: add name, highest_role, is_primary_master
- NEW: UserRole (multi-role stacking)
- RolePermission: add user_role FK, module, permission_level, can_create_users,
  can_delete_users, can_create_roles_up_to; make user nullable
- NEW: PermissionRequest
- NEW: AuditLog
- LoginHistory: add active_role
"""
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth_service', '0003_tenant_logo_tenant_plan_user_custom_role_name_and_more'),
    ]

    operations = [
        # ── TENANT UPDATES ──
        migrations.AddField(
            model_name='tenant',
            name='tenant_id',
            field=models.CharField(blank=True, help_text='Display ID e.g. BIND-PNP-0042', max_length=30, unique=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tenant',
            name='owner_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='tenant',
            name='whatsapp_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='tenant',
            name='location_city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='tenant',
            name='location_state',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='tenant',
            name='industry_vertical',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.RenameField(
            model_name='tenant',
            old_name='user_limit',
            new_name='max_users',
        ),

        # ── USER UPDATES ──
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, help_text='Full display name (v2)', max_length=150),
        ),
        migrations.AddField(
            model_name='user',
            name='highest_role',
            field=models.CharField(blank=True, choices=[
                ('master_admin', 'Master Admin'), ('admin', 'Admin'),
                ('manager', 'Manager'), ('supervisor', 'Supervisor'),
                ('operator', 'Operator'),
            ], default='', help_text='Computed from user_roles - highest assigned role', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='is_primary_master',
            field=models.BooleanField(default=False, help_text='True only for the 1st Master Admin of the org'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['tenant', 'highest_role'], name='users_tenant__b8f2d3_idx'),
        ),

        # ── USER ROLE (NEW) ──
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[
                    ('master_admin', 'Master Admin'), ('admin', 'Admin'),
                    ('manager', 'Manager'), ('supervisor', 'Supervisor'),
                    ('operator', 'Operator'),
                ], max_length=20)),
                ('department', models.CharField(blank=True, help_text='Department scope', max_length=100, null=True)),
                ('is_default_role', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_roles', to=settings.AUTH_USER_MODEL)),
                ('assigned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_roles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_roles',
                'verbose_name': 'User Role',
                'verbose_name_plural': 'User Roles',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='userrole',
            constraint=models.UniqueConstraint(fields=('user', 'role', 'department'), name='unique_user_role_department'),
        ),

        # ── ROLE PERMISSION UPDATES ──
        migrations.AddField(
            model_name='rolepermission',
            name='user_role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='role_permissions', to='auth_service.userrole'),
        ),
        migrations.AddField(
            model_name='rolepermission',
            name='module',
            field=models.CharField(blank=True, choices=[
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
            ], max_length=50),
        ),
        migrations.AddField(
            model_name='rolepermission',
            name='permission_level',
            field=models.CharField(choices=[
                ('none', 'None'), ('view', 'View'), ('input', 'Input'),
                ('edit', 'Edit'), ('full', 'Full'), ('config', 'Config'),
            ], default='none', max_length=10),
        ),
        migrations.AddField(
            model_name='rolepermission',
            name='can_create_users',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rolepermission',
            name='can_delete_users',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rolepermission',
            name='can_create_roles_up_to',
            field=models.CharField(blank=True, choices=[
                ('master_admin', 'Master Admin'), ('admin', 'Admin'),
                ('manager', 'Manager'), ('supervisor', 'Supervisor'),
                ('operator', 'Operator'),
            ], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='rolepermission',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='legacy_role_permissions', to=settings.AUTH_USER_MODEL),
        ),

        # ── PERMISSION REQUEST (NEW) ──
        migrations.CreateModel(
            name='PermissionRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('module_requested', models.CharField(choices=[
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
                ], max_length=50)),
                ('specific_record_id', models.CharField(blank=True, max_length=255, null=True)),
                ('reason', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permission_requests', to=settings.AUTH_USER_MODEL)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_permission_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'permission_requests',
                'verbose_name': 'Permission Request',
                'verbose_name_plural': 'Permission Requests',
                'ordering': ['-created_at'],
            },
        ),

        # ── AUDIT LOG (NEW) ──
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active_role', models.CharField(blank=True, choices=[
                    ('master_admin', 'Master Admin'), ('admin', 'Admin'),
                    ('manager', 'Manager'), ('supervisor', 'Supervisor'),
                    ('operator', 'Operator'),
                ], max_length=20)),
                ('action_type', models.CharField(choices=[
                    ('create', 'Create'), ('edit', 'Edit'), ('delete', 'Delete'),
                    ('approve', 'Approve'), ('login', 'Login'), ('logout', 'Logout'),
                    ('role_switch', 'Role Switch'),
                ], max_length=20)),
                ('module', models.CharField(blank=True, max_length=50)),
                ('record_id', models.CharField(blank=True, max_length=255)),
                ('details', models.JSONField(blank=True, default=dict)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit_logs', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='audit_logs', to='auth_service.tenant')),
            ],
            options={
                'db_table': 'audit_log',
                'verbose_name': 'Audit Log',
                'verbose_name_plural': 'Audit Logs',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['user', '-timestamp'], name='audit_log_user_id_ts_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['organization', '-timestamp'], name='audit_log_org_id_ts_idx'),
        ),

        # ── LOGIN HISTORY: add active_role ──
        migrations.AddField(
            model_name='loginhistory',
            name='active_role',
            field=models.CharField(blank=True, choices=[
                ('master_admin', 'Master Admin'), ('admin', 'Admin'),
                ('manager', 'Manager'), ('supervisor', 'Supervisor'),
                ('operator', 'Operator'),
            ], max_length=20),
        ),
    ]
