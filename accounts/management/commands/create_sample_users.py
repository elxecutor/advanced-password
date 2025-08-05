from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create sample users for testing'

    def handle(self, *args, **options):
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='AdminPassword123!'
            )
            self.stdout.write(
                self.style.SUCCESS('Created admin user: admin / AdminPassword123!')
            )
        else:
            self.stdout.write('Admin user already exists')

        # Create regular test user
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='TestPassword123!'
            )
            self.stdout.write(
                self.style.SUCCESS('Created test user: testuser / TestPassword123!')
            )
        else:
            self.stdout.write('Test user already exists')
            
        self.stdout.write(
            self.style.SUCCESS('\nAll sample users created successfully!')
        )
