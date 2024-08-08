from allauth.socialaccount.models import SocialApp
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with sample data"

    def handle(self, *args, **options):
        self.create_users()
        self.create_customers()
        self.create_superuser()
        self.create_google_social_app()
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))

    def create_users(self):
        User.objects.create_user(
            username="admin_user",
            email="admin_user@example.com",
            password="password123",
            is_admin=True,
        )
        User.objects.create_user(
            username="normal_user",
            email="normal_user@example.com",
            password="password123",
            is_admin=False,
        )

    def create_customers(self):
        User.objects.create_user(
            username="customer1", email="customer1@example.com", password="password123"
        )
        User.objects.create_user(
            username="customer2", email="customer2@example.com", password="password123"
        )
        User.objects.create_user(
            username="customer3", email="customer3@example.com", password="password123"
        )

    def create_superuser(self):
        User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password123"
        )

    def create_google_social_app(self):
        site = Site.objects.get_current()
        SocialApp.objects.create(
            provider="google",
            name="Google",
            client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
            secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
            sites=[site],
        )
