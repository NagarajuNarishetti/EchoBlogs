from django.core.management.base import BaseCommand
from django.db import connection
from tenants.models import Client, Domain
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Create a public tenant for the main domain'

    def handle(self, *args, **options):
        # Create public tenant
        public_tenant, created = Client.objects.get_or_create(
            schema_name='public',
            defaults={
                'name': 'Public',
                'paid_until': date.today() + timedelta(days=365),
                'on_trial': False,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created public tenant')
            )
        else:
            self.stdout.write('Public tenant already exists')
        
        # Create domain for public tenant
        public_domain, created = Domain.objects.get_or_create(
            domain='127.0.0.1',
            defaults={
                'tenant': public_tenant,
                'is_primary': True,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created public domain')
            )
        else:
            self.stdout.write('Public domain already exists')
        
        # Also create localhost domain
        localhost_domain, created = Domain.objects.get_or_create(
            domain='localhost',
            defaults={
                'tenant': public_tenant,
                'is_primary': False,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created localhost domain')
            )
        else:
            self.stdout.write('Localhost domain already exists')
        
        self.stdout.write(
            self.style.SUCCESS('Public tenant setup completed!')
        )
