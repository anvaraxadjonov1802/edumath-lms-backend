import os

from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = "Create default admin user from environment variables"

    def handle(self, *args, **options):
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")
        full_name = os.getenv("ADMIN_FULL_NAME", "EduMath Admin")

        if not email or not password:
            self.stdout.write(
                self.style.WARNING(
                    "ADMIN_EMAIL or ADMIN_PASSWORD is not set. Skipping admin creation."
                )
            )
            return

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "full_name": full_name,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
                "is_email_verified": True,
                "role": "admin",
            },
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Admin user created: {email}")
            )
            return

        changed = False

        if not user.is_staff:
            user.is_staff = True
            changed = True

        if not user.is_superuser:
            user.is_superuser = True
            changed = True

        if not user.is_active:
            user.is_active = True
            changed = True

        if not user.is_email_verified:
            user.is_email_verified = True
            changed = True

        if user.role != "admin":
            user.role = "admin"
            changed = True

        reset_password = os.getenv("ADMIN_RESET_PASSWORD", "False") == "True"

        if reset_password:
            user.set_password(password)
            changed = True

        if changed:
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Admin user updated: {email}")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Admin user already exists: {email}")
            )