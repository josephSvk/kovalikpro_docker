from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Displays a list of user accounts"

    def handle(self, *args, **kwargs):
        user = get_user_model()
        users = user.objects.all()
        for user in users:
            self.stdout.write(
                f"User: {user.email}, Joined: {user.date_joined}, "
                f"Active: {user.is_active}",
            )
