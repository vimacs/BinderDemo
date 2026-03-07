"""
Management command to seed 5 admin accounts for Binder ERP.
Run: python manage.py seed_admins

Safe to run multiple times — skips existing users.
"""
from django.core.management.base import BaseCommand
from auth_service.models import User, Tenant


ADMINS = [
    {
        'email': 'vikram@erpbinder.com',
        'password': 'qwerty@11',
        'first_name': 'Vikram',
        'last_name': 'Admin',
        'role': 'master_admin',
        'is_primary_master': True,
    },
    {
        'email': 'shubh.saxena@erpbinder.com',
        'password': 'qwerty@22',
        'first_name': 'Shubh',
        'last_name': 'Saxena',
        'role': 'master_admin',
    },
    {
        'email': 'azeem@erpbinder.com',
        'password': 'qwerty@33',
        'first_name': 'Azeem',
        'last_name': 'Admin',
        'role': 'master_admin',
    },
    {
        'email': 'vaibhav@erpbinder.com',
        'password': 'qwerty@44',
        'first_name': 'Vaibhav',
        'last_name': 'Admin',
        'role': 'master_admin',
    },
    {
        'email': 'ravinder@erpbinder.com',
        'password': 'qwerty@55',
        'first_name': 'Ravinder',
        'last_name': 'Admin',
        'role': 'master_admin',
    },
]


class Command(BaseCommand):
    help = 'Create 5 admin accounts for Binder ERP (idempotent — safe to run multiple times)'

    def handle(self, *args, **options):
        # 1. Create or get the Binder tenant
        tenant, created = Tenant.objects.get_or_create(
            company_name='Binder ERP',
            defaults={
                'company_email': 'admin@erpbinder.com',
                'company_phone': '+910000000000',
                'company_address': 'Chandigarh, India',
                'location_city': 'CHD',
                'location_state': 'Chandigarh',
                'industry_vertical': 'Textile Manufacturing',
                'plan': 'enterprise',
                'max_users': 50,
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ Created tenant: {tenant}'))
        else:
            self.stdout.write(f'ℹ️  Tenant already exists: {tenant}')

        # 2. Create each admin user
        for admin_data in ADMINS:
            email = admin_data['email']
            password = admin_data.pop('password')
            is_primary = admin_data.pop('is_primary_master', False)

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': admin_data.get('first_name', ''),
                    'last_name': admin_data.get('last_name', ''),
                    'name': f"{admin_data.get('first_name', '')} {admin_data.get('last_name', '')}".strip(),
                    'role': admin_data.get('role', 'master_admin'),
                    'highest_role': 'master_admin',
                    'tenant': tenant,
                    'is_active': True,
                    'is_staff': True,
                    'is_superuser': is_primary,
                    'is_primary_master': is_primary,
                    'email_verified': True,
                }
            )

            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(
                    f'✅ Created admin: {email} (primary={is_primary})'
                ))
            else:
                self.stdout.write(f'ℹ️  Admin already exists: {email}')

        # 3. Update tenant user count
        tenant.current_user_count = User.objects.filter(tenant=tenant).count()
        tenant.save(update_fields=['current_user_count'])

        self.stdout.write(self.style.SUCCESS(
            f'\n🎉 Done! {User.objects.filter(tenant=tenant).count()} users in tenant "{tenant.company_name}"'
        ))